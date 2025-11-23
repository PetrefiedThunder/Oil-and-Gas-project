"""API surface for explainability operations."""
from fastapi import APIRouter, Depends

from app.core.config import settings
from app.modules.explainability.interfaces import ExplanationGenerator, MockExplanationGenerator


router = APIRouter(tags=["explainability"])


def get_explanation_generator() -> ExplanationGenerator:
    if settings.enable_mock_services:
        return MockExplanationGenerator()
    raise NotImplementedError("Configure a concrete explanation generator")


@router.post("/explain")
def generate_explanation(
    record: dict, generator: ExplanationGenerator = Depends(get_explanation_generator)
) -> dict:
    return generator.explain(record)
