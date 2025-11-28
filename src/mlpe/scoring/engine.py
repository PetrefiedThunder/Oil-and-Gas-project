from datetime import datetime, timezone
from typing import List, Optional

from mlpe.models import LeakEvent, RankedLeak, RankedLeakResponse


class ScoreEngine:
    """Lightweight placeholder scorer to unblock API development."""

    def rank_leaks(self, leaks: List[LeakEvent], site_id: Optional[str] = None) -> RankedLeakResponse:
        ranked: List[RankedLeak] = []
        for index, leak in enumerate(leaks, start=1):
            source_count = len(leak.detection_sources)
            base_score = min(1.0, 0.5 + 0.1 * source_count)
            facility_weight = leak.facility_criticality or 0.5
            score = min(1.0, base_score * (0.6 + 0.4 * facility_weight))
            confidence_band = "high" if score >= 0.75 else "medium" if score >= 0.4 else "low"
            rationale = [
                f"{source_count} corroborating detections",
                f"facility criticality weight={facility_weight}",
            ]
            ranked.append(
                RankedLeak(
                    leak_id=leak.leak_id,
                    score=round(score, 3),
                    rank=index,
                    confidence_band=confidence_band,
                    rationale=rationale,
                )
            )

        return RankedLeakResponse(site_id=site_id, generated_at=datetime.now(timezone.utc), leaks=ranked)
