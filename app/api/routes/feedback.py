"""API surface for collecting feedback."""
from fastapi import APIRouter, Depends

from app.core.config import settings
from app.modules.feedback.interfaces import FeedbackSink, MockFeedbackSink


router = APIRouter(tags=["feedback"])


def get_feedback_sink() -> FeedbackSink:
    if settings.enable_mock_services:
        return MockFeedbackSink()
    raise NotImplementedError("Configure a concrete feedback sink")


@router.post("/feedback")
def submit_feedback(payload: dict, sink: FeedbackSink = Depends(get_feedback_sink)) -> dict:
    return sink.record(payload)
