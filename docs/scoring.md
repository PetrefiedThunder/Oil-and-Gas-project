# Scoring & Model Serving

## Inputs & Outputs
| Stage | Inputs | Outputs | Storage | Notes |
| --- | --- | --- | --- | --- |
| Feature Load | Curated tables, feature store snapshots | In-memory feature vectors | Scoring nodes | Time-windowed joins applied at load |
| Model Execution | Feature vectors, model artifacts | Raw predictions, intermediate tensors | Scoring nodes | Batch and streaming runners share codepaths |
| Post-Processing | Raw predictions | Calibrated scores, thresholds, explanations | Results store (Parquet + OLTP) | Conformal calibration + rule-based overrides |
| Publication | Calibrated scores, metadata | API/gRPC responses, Kafka events | API gateway, topics | SLA-backed responses with tracing IDs |

## Fusion Logic
- Rule priority: deterministic joins (well ID + time), then enrichment, then conflict resolution via freshness + trust scores.
- Feature derivations logged with versioned transformation specs to enable replay.
- Data drift detection hooks emit signals to QA/audit layer when feature distributions shift.

## Serving Topology
- **Batch:** scheduled DAGs reading curated partitions, writing scored Parquet and warehouse tables.
- **Streaming:** low-latency microservice consuming Kafka, stateless per-request feature lookup cache.
- **Canarying:** subset of traffic scored with new models; dual-write outputs for comparison.
- **Failover:** multi-AZ deployments with health-checked load balancers; circuit breakers around model RPC calls.

## Feedback Mechanisms
| Source | Mechanism | Usage |
| --- | --- | --- |
| User labels / overrides | API feedback endpoint | Rapid correction of mis-scored entities |
| Downstream system errors | Dead-letter topics + dashboards | Identify systemic feature gaps |
| Data quality findings | QA alerts routed to scoring backlog | Prioritize feature fixes and retraining |
| Business KPI shifts | Weekly review with product stakeholders | Adjust thresholds and calibration |

## Observability
- Metrics: latency p50/p95, throughput, queue depth, model accuracy by segment.
- Tracing: distributed tracing IDs propagated from ingestion through scoring to outputs.
- Logging: structured, PII-scrubbed logs with request IDs; searchable in SIEM.
