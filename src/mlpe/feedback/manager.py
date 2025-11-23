from typing import List

from mlpe.models import FeedbackItem


class FeedbackManager:
    """In-memory feedback registry for API prototyping."""

    def __init__(self) -> None:
        self._items: List[FeedbackItem] = []

    def record(self, item: FeedbackItem) -> FeedbackItem:
        self._items.append(item)
        return item

    def list_feedback(self) -> List[FeedbackItem]:
        return list(self._items)
