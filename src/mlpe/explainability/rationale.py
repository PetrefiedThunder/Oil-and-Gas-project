from typing import List

from mlpe.models import RankedLeak


class RationaleBuilder:
    """Placeholder rationale builder combining signals into human-readable strings."""

    def build(self, ranked_leak: RankedLeak) -> str:
        reasons: List[str] = ranked_leak.rationale
        return "; ".join(reasons) if reasons else "No rationale available"
