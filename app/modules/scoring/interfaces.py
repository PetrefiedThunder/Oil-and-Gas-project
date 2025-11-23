"""Interfaces and stubs for scoring pipelines."""
from abc import ABC, abstractmethod
from typing import Iterable, List, Mapping


class ScoringEngine(ABC):
    """Scores fused records against a risk or quality model."""

    @abstractmethod
    def score(self, records: Iterable[Mapping]) -> List[Mapping]:
        """Generate scores for provided records."""


class MockScoringEngine(ScoringEngine):
    """Lightweight scoring engine that assigns deterministic scores."""

    def score(self, records: Iterable[Mapping]) -> List[Mapping]:
        scored = []
        for idx, record in enumerate(records):
            scored.append({**record, "score": 0.75 + idx * 0.01})
        return scored
