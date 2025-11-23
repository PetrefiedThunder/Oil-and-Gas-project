from datetime import datetime
from typing import Iterable, List

from mlpe.models import DetectionSource, LeakEvent, Location


class FusionEngine:
    """Stub fusion engine for grouping detections into composite leak events."""

    def merge_sources(self, leak_id: str, location: Location, sources: Iterable[DetectionSource]) -> LeakEvent:
        sources_list: List[DetectionSource] = list(sources)
        timestamps = sorted(source.observed_at for source in sources_list)
        timestamp_range = [timestamps[0], timestamps[-1]] if timestamps else None
        return LeakEvent(
            leak_id=leak_id,
            location=location,
            detection_sources=sources_list,
            timestamp_range=timestamp_range,
            facility_criticality=None,
            signal_age_seconds=self._calculate_signal_age(timestamps),
        )

    @staticmethod
    def _calculate_signal_age(timestamps: List[datetime]) -> int:
        if not timestamps:
            return 0
        latest = max(timestamps)
        return int((datetime.utcnow() - latest).total_seconds())
