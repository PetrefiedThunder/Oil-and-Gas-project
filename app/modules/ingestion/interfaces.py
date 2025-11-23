"""Interfaces and stubs for ingestion workflows."""
from abc import ABC, abstractmethod
from typing import Iterable, List, Mapping


class IngestionSource(ABC):
    """Defines how to fetch records from a source system."""

    @abstractmethod
    def fetch(self) -> Iterable[Mapping]:
        """Retrieve records from a source."""


class IngestionPipeline(ABC):
    """High level ingestion pipeline orchestrator."""

    @abstractmethod
    def run(self) -> List[Mapping]:
        """Run ingestion and return staged records."""


class MockIngestionPipeline(IngestionPipeline):
    """Development-only pipeline that emits sample records."""

    def run(self) -> List[Mapping]:
        return [
            {"source": "mock", "payload": "synthetic sensor reading", "quality": "draft"}
        ]
