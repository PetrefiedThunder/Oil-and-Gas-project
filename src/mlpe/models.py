from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Location(BaseModel):
    latitude: float
    longitude: float
    geohash: Optional[str] = Field(None, description="Geospatial hash for clustering")


class DetectionSource(BaseModel):
    source_type: str = Field(..., description="satellite|sensor|scada|aerial")
    confidence: float = Field(..., ge=0.0, le=1.0)
    observed_at: datetime
    metadata: Optional[dict] = Field(default_factory=dict)


class LeakEvent(BaseModel):
    leak_id: str
    location: Location
    detection_sources: List[DetectionSource]
    timestamp_range: Optional[List[datetime]] = None
    facility_criticality: Optional[float] = Field(None, ge=0.0, le=1.0)
    signal_age_seconds: Optional[int] = None


class RankedLeak(BaseModel):
    leak_id: str
    score: float = Field(..., ge=0.0, le=1.0)
    rank: int
    confidence_band: str
    rationale: List[str]


class RankedLeakResponse(BaseModel):
    site_id: Optional[str]
    generated_at: datetime
    leaks: List[RankedLeak]


class FeedbackItem(BaseModel):
    leak_id: str
    status: str = Field(..., description="confirmed|false_positive|repaired")
    reviewer_id: str
    submitted_at: datetime
    notes: Optional[str] = None
