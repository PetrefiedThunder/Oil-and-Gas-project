# Normalization & Fusion

## Goals
- Align detections across sources in both space and time.
- Reduce duplicate alerts by clustering nearby detections.
- Emit composite leak events with traceable source metadata.

## Techniques
- **Spatial clustering**: Geohash or H3 indexing to group detections within a configurable radius.
- **Temporal bucketing**: ±60 minute windows to associate time-adjacent detections.
- **Merging logic**: Combine source metadata, confidence scores, and timestamps into a single normalized event object.

## Output Event Metadata
- Leak ID (geo-temporal hash)
- Geo location (centroid and bounds)
- Detection sources and counts
- Confidence scores and aggregation strategy
- Timestamp range and event duration
- Source latency and signal age
- Audit trail of transformations

## Validation & Integrity
- Reject or flag events with insufficient geospatial precision.
- Ensure consistent coordinate reference systems.
- Record lineage for each merged detection to support explainability and audit.
