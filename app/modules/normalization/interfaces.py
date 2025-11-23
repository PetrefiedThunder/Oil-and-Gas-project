"""Interfaces and stubs for normalization and fusion."""
from abc import ABC, abstractmethod
from typing import Iterable, List, Mapping


class Normalizer(ABC):
    """Standardizes incoming records."""

    @abstractmethod
    def normalize(self, records: Iterable[Mapping]) -> List[Mapping]:
        """Normalize raw records into a canonical schema."""


class FusionEngine(ABC):
    """Combines multiple normalized records into cohesive entities."""

    @abstractmethod
    def fuse(self, records: Iterable[Mapping]) -> List[Mapping]:
        """Fuse related records together."""


class MockNormalizationPipeline(Normalizer, FusionEngine):
    """Simplistic normalization and fusion for early testing."""

    def normalize(self, records: Iterable[Mapping]) -> List[Mapping]:
        return [dict(record, normalized=True) for record in records]

    def fuse(self, records: Iterable[Mapping]) -> List[Mapping]:
        return [
            {**record, "fusion_key": record.get("source", "unknown"), "fused": True}
            for record in records
        ]
