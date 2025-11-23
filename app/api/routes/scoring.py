"""API surface for scoring operations."""
from fastapi import APIRouter, Depends

from app.core.config import settings
from app.modules.scoring.interfaces import MockScoringEngine, ScoringEngine


router = APIRouter(tags=["scoring"])


def get_scoring_engine() -> ScoringEngine:
    if settings.enable_mock_services:
        return MockScoringEngine()
    raise NotImplementedError("Configure a concrete scoring engine")


@router.post("/score")
def score_records(records: list[dict], scorer: ScoringEngine = Depends(get_scoring_engine)) -> dict:
    scored = scorer.score(records)
    return {"status": "scored", "records": scored}
