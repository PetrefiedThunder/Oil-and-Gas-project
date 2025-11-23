"""API surface for ingestion operations."""
from fastapi import APIRouter, Depends

from app.core.config import settings
from app.modules.ingestion.interfaces import IngestionPipeline, MockIngestionPipeline


router = APIRouter(tags=["ingestion"])


def get_pipeline() -> IngestionPipeline:
    """Provide an ingestion pipeline implementation."""

    if settings.enable_mock_services:
        return MockIngestionPipeline()
    raise NotImplementedError("Configure a concrete ingestion pipeline")


@router.post("/ingest")
def trigger_ingestion(pipeline: IngestionPipeline = Depends(get_pipeline)) -> dict:
    """Trigger ingestion and return summary."""

    records = pipeline.run()
    return {"status": "ingested", "record_count": len(records)}
