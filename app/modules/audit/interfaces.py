"""Interfaces for audit and assurance workflows."""
from abc import ABC, abstractmethod
from typing import Iterable, List, Mapping


class AuditTrail(ABC):
    """Captures pipeline events for traceability."""

    @abstractmethod
    def record(self, event: Mapping) -> Mapping:
        """Persist a structured audit event."""


class AssuranceChecker(ABC):
    """Validates data and model quality."""

    @abstractmethod
    def validate(self, records: Iterable[Mapping]) -> List[Mapping]:
        """Return validation results for fused records."""


class MockAuditTrail(AuditTrail, AssuranceChecker):
    """Lightweight implementations for pipeline prototyping."""

    def record(self, event: Mapping) -> Mapping:
        return {"status": "logged", **event}

    def validate(self, records: Iterable[Mapping]) -> List[Mapping]:
        return [dict(record, validation_passed=True) for record in records]
