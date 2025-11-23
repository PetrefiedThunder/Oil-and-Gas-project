"""Interfaces for generating explanations for scored records."""
from abc import ABC, abstractmethod
from typing import Mapping


class ExplanationGenerator(ABC):
    """Produces human-readable or machine-consumable explanations."""

    @abstractmethod
    def explain(self, record: Mapping) -> Mapping:
        """Return an explanation artifact for a record."""


class MockExplanationGenerator(ExplanationGenerator):
    """Returns static explanation payloads for prototypes."""

    def explain(self, record: Mapping) -> Mapping:
        return {
            "explanation": "Mock feature attributions",
            "inputs": record,
            "rationale": "Placeholder explanation for development",
        }
