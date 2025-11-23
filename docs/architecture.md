# Methane Leak Prioritization Engine (MLPE) Architecture

## System Overview
The MLPE orchestrates data ingestion, normalization, scoring, and delivery to rank methane leak events for operational response. Core services are containerized and deployable on AWS ECS/Fargate or GCP Cloud Run with persistent storage on Postgres and S3.

## Module Map
- **Ingestion Layer**: Collects satellite, sensor MQTT, SCADA, and aerial uploads, stores raw payloads, and validates schemas and confidence.
- **Normalization & Fusion Engine**: Aligns detections across space and time using geospatial hashing and time-window bucketing to produce composite leak events with full audit traces.
- **Scoring Engine**: Ranks leak events via ML or rule-based logic, emitting scores, ranks, confidence bands, and rationales.
- **Output API Layer**: Exposes REST endpoints and webhooks for CMMS integrations and export formats (CSV/JSON/PDF).
- **Feedback Module**: Captures field-confirmed statuses to improve scoring and retraining loops.
- **Explainability Layer**: Generates SHAP-based and rule-backed rationales for transparency.
- **Audit & Assurance Layer**: Tracks data lineage, integrity, QA benchmarks, and model drift.

## Data Flow Summary
1. Raw payloads are validated, timestamp-normalized to UTC, and assigned geo-temporal event IDs.
2. Fusion clusters detections by H3/geohash and ±60 minute windows, merging metadata into composite events.
3. Scoring consumes normalized events plus facility criticality to produce ranked outputs with rationale vectors.
4. Feedback records updates (confirmed, false positive, repaired) that feed retraining pipelines.
5. Output APIs deliver ranked leaks to CMMS webhooks or exports, while audit logging maintains traceability.

## Deployment & Operations
- Containerized services with CI/CD (GitHub Actions/GitLab CI) and orchestration via Airflow/Prefect.
- ML lifecycle tracked with MLflow or Weights & Biases, including drift detection and monthly performance reports.
- Stress testing and red-team validation ensure resilience under high event volumes.

## Delivery Milestones
1. **Phase 1 (Weeks 1–2)**: Bootstrap schemas, ingest mock data, seed test datasets.
2. **Phase 2 (Weeks 3–4)**: Finalize fusion algorithms and validate signal alignment.
3. **Phase 3 (Weeks 5–7)**: Implement scoring (ML + rules) and explainability.
4. **Phase 4 (Weeks 8–10)**: Enable feedback inputs and QA dashboards.
5. **Phase 5 (Weeks 11–12)**: Integrate CMMS outputs and run end-to-end simulations with performance reviews.
