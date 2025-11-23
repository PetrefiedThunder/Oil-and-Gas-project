from typing import Iterable, List

from mlpe.models import DetectionSource


class IngestionPipeline:
    """Placeholder ingestion pipeline to validate and forward detections."""

    def __init__(self) -> None:
        self._quarantine: List[DetectionSource] = []

    def validate(self, source: DetectionSource) -> bool:
        is_valid_confidence = 0.0 <= source.confidence <= 1.0
        has_coordinates = "coordinates" in source.metadata if source.metadata else False
        if not (is_valid_confidence and has_coordinates):
            self._quarantine.append(source)
            return False
        return True

    def process_batch(self, sources: Iterable[DetectionSource]) -> List[DetectionSource]:
        return [source for source in sources if self.validate(source)]

    @property
    def quarantined(self) -> List[DetectionSource]:
        return list(self._quarantine)
