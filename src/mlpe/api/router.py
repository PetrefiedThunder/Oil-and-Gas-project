from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from mlpe.audit.assurance import AuditLog
from mlpe.explainability.rationale import RationaleBuilder
from mlpe.feedback.manager import FeedbackManager
from mlpe.ingestion.pipeline import IngestionPipeline
from mlpe.models import DetectionSource, FeedbackItem, LeakEvent, Location, RankedLeakResponse
from mlpe.normalization.fusion import FusionEngine
from mlpe.scoring.engine import ScoreEngine


class IngestPayload(BaseModel):
    leak_id: str
    location: Location
    detections: List[DetectionSource]


api_router = APIRouter()
ingestion_pipeline = IngestionPipeline()
fusion_engine = FusionEngine()
scoring_engine = ScoreEngine()
feedback_manager = FeedbackManager()
audit_log = AuditLog()
rationale_builder = RationaleBuilder()
leak_events: List[LeakEvent] = []


@api_router.get("/health")
def healthcheck() -> dict:
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@api_router.post("/ingest/scada", response_model=LeakEvent)
def ingest_scada(payload: IngestPayload) -> LeakEvent:
    valid_detections = ingestion_pipeline.process_batch(payload.detections)
    event = fusion_engine.merge_sources(payload.leak_id, payload.location, valid_detections)
    leak_events.append(event)
    audit_log.record("ingested scada payload", event.leak_id)
    return event


@api_router.get("/leaks/ranked", response_model=RankedLeakResponse)
def ranked_leaks(site_id: Optional[str] = None) -> RankedLeakResponse:
    events = leak_events or _seed_demo_events()
    ranked = scoring_engine.rank_leaks(events, site_id=site_id)
    for leak in ranked.leaks:
        rationale_text = rationale_builder.build(leak)
        audit_log.record(f"generated rationale: {rationale_text}", leak.leak_id)
    return ranked


@api_router.post("/feedback")
def submit_feedback(item: FeedbackItem) -> FeedbackItem:
    audit_log.record("feedback received", item.leak_id)
    return feedback_manager.record(item)


def _seed_demo_events() -> List[LeakEvent]:
    sample_location = Location(latitude=29.7604, longitude=-95.3698, geohash="9vk8p")
    sources = [
        DetectionSource(
            source_type="sensor",
            confidence=0.82,
            observed_at=datetime.utcnow(),
            metadata={"coordinates": sample_location.dict()},
        ),
        DetectionSource(
            source_type="satellite",
            confidence=0.71,
            observed_at=datetime.utcnow(),
            metadata={"coordinates": sample_location.dict()},
        ),
    ]
    return [fusion_engine.merge_sources("demo-1", sample_location, sources)]
