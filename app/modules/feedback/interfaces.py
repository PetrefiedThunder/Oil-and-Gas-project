"""Interfaces for capturing and acting on feedback."""
from abc import ABC, abstractmethod
from typing import Mapping


class FeedbackSink(ABC):
    """Destination for storing user or system feedback."""

    @abstractmethod
    def record(self, payload: Mapping) -> Mapping:
        """Persist feedback payload."""


class MockFeedbackSink(FeedbackSink):
    """Feedback sink that echoes the payload for development."""

    def record(self, payload: Mapping) -> Mapping:
        return {"status": "recorded", "payload": payload}
