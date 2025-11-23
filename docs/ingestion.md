# Ingestion Layer

## Sources & Formats
- **Satellite**: Periodic batch JSON (e.g., GHGSat, Carbon Mapper)
- **Sensors**: MQTT streams from on-site devices
- **SCADA**: REST webhooks or batch JSON payloads
- **Aerial**: GeoJSON or CSV uploads (field or contractor provided)

## Functional Requirements
- Normalize timestamps to UTC across all payloads.
- Assign deterministic geo-temporal event IDs (geohash/H3 + time bucket).
- Validate schemas and enforce minimum confidence thresholds.
- Persist raw and normalized payloads for audit and replay.

## Processing Steps
1. **Schema Validation**: Pydantic models enforce structure; reject or quarantine invalid payloads.
2. **Timestamp Normalization**: Convert source timestamps to UTC and record source timezone.
3. **ID Assignment**: Compute geospatial hash and combine with time bucket for stable event IDs.
4. **Storage**: Write raw payloads to object storage (S3) and normalized records to Postgres; enqueue to Kafka for downstream fusion.

## Data Contracts
- Payloads must include coordinates, observed time, source ID, confidence score, and facility/site reference where available.
- Optional metadata (sensor health, orbital pass, flight ID) is preserved in the audit trail.

## Interfaces (Planned)
- **MQTT client** subscribes to sensor topics, forwards to ingestion pipeline.
- **REST endpoint** for SCADA webhooks (`/ingest/scada`).
- **Upload endpoint** for aerial CSV/GeoJSON with schema validation and preview responses.
- **Batch loader** for satellite JSON drops with idempotent processing.
