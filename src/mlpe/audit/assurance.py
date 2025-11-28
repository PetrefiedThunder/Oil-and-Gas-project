from datetime import datetime, timezone
from typing import Dict, List


class AuditLog:
    """Minimal audit log to demonstrate lineage capture."""

    def __init__(self) -> None:
        self._entries: List[Dict[str, str]] = []

    def record(self, message: str, event_id: str) -> Dict[str, str]:
        entry = {"event_id": event_id, "message": message, "recorded_at": datetime.now(timezone.utc).isoformat()}
        self._entries.append(entry)
        return entry

    def all(self) -> List[Dict[str, str]]:
        return list(self._entries)
