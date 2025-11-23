# Ingestion Plan

## Sources and Connectors
| Source Type | Examples | Frequency | Connector | Notes |
| --- | --- | --- | --- | --- |
| Relational DBs | Production operations, maintenance logs | Hourly | CDC pipeline (Debezium) | Schema versioning enforced at registry |
| Object Storage | Historical sensor dumps, lab reports | Daily | Batch pull via signed URLs | Size-aware chunking with retries |
| Streaming | Real-time sensors, telemetry | Sub-minute | Kafka topics (Protobuf) | Exactly-once semantics with checkpoints |
| Third-Party APIs | Market/price feeds | 15 minutes | REST with OAuth | Rate-limit aware retry/backoff |

## Validation & Normalization
- Schema validation (Avro/Protobuf) with automatic rejection queues and alerting.
- Standardization of units, timestamps (UTC), and well IDs to canonical identifiers.
- PII stripping/masking before persistence; hashed identifiers for joins.

## Landing & Curation
| Layer | Storage | Purpose | Retention | Access |
| --- | --- | --- | --- | --- |
| Raw Landing | Object storage (gzip Parquet) | Immutable snapshots | 30 days | Restricted to platform admins |
| Staging | Append-only tables | QA replay, backfills | 90 days | Data engineering, QA |
| Curated | Partitioned tables | Feature-ready datasets | 400 days | Feature, model, and analytics consumers |

## Fusion & Feature Readiness
- Deterministic joins on well ID + time windows.
- Rules-based enrichment (e.g., geology attributes) with audit fields.
- Late-arriving data triggers partial recompute via incremental DAG runs.

## Operational Controls
- Idempotent ingestion jobs with watermarking and DLQs for malformed records.
- Observability via metrics (lag, throughput), structured logs, and lineage events.
- Runbooks for connector rotation, credential refresh, and backfill procedures.

See `docs/architecture.md` for upstream/downstream context.
