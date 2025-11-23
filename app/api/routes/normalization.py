"""API surface for normalization and fusion operations."""
from fastapi import APIRouter, Depends

from app.core.config import settings
from app.modules.normalization.interfaces import FusionEngine, MockNormalizationPipeline, Normalizer


router = APIRouter(tags=["normalization"])


def get_normalization_pipeline() -> Normalizer:
    """Provide a normalization engine implementation."""

    if settings.enable_mock_services:
        return MockNormalizationPipeline()
    raise NotImplementedError("Configure a concrete normalization pipeline")


def get_fusion_engine() -> FusionEngine:
    if settings.enable_mock_services:
        return MockNormalizationPipeline()
    raise NotImplementedError("Configure a concrete fusion engine")


@router.post("/normalize")
def normalize_records(
    records: list[dict], normalizer: Normalizer = Depends(get_normalization_pipeline)
) -> dict:
    normalized = normalizer.normalize(records)
    return {"status": "normalized", "records": normalized}


@router.post("/fuse")
def fuse_records(records: list[dict], fusion_engine: FusionEngine = Depends(get_fusion_engine)) -> dict:
    fused = fusion_engine.fuse(records)
    return {"status": "fused", "records": fused}
