"""Root API router including all module-specific routes."""
from fastapi import APIRouter

from . import audit, explainability, feedback, health, ingestion, normalization, output, scoring

router = APIRouter()
router.include_router(health.router)
router.include_router(ingestion.router)
router.include_router(normalization.router)
router.include_router(scoring.router)
router.include_router(feedback.router)
router.include_router(explainability.router)
router.include_router(audit.router)
router.include_router(output.router)

__all__ = ["router"]
