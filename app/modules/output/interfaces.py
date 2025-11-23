"""Interfaces for delivering pipeline outputs to downstream systems."""
from abc import ABC, abstractmethod
from typing import Iterable, List, Mapping


class OutputAdapter(ABC):
    """Sends scored and validated payloads to external APIs or storage."""

    @abstractmethod
    def dispatch(self, records: Iterable[Mapping]) -> List[Mapping]:
        """Send records to the configured destination."""


class MockOutputAdapter(OutputAdapter):
    """Development-only adapter that echoes dispatches."""

    def dispatch(self, records: Iterable[Mapping]) -> List[Mapping]:
        return [dict(record, delivered=True) for record in records]
