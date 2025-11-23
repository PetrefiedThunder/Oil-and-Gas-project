# Output API Layer

## Endpoints (Planned)
- `GET /leaks/ranked?site_id=&date_range=`: Retrieve ranked leaks for a site and optional date range.
- `POST /dispatch/ticket`: Send ranked events to CMMS/webhook targets (SAP PM, IBM Maximo, ProntoForms).
- `POST /feedback`: Capture field validation (confirmed, false positive, repaired).
- Export utilities for CSV, JSON, and PDF summaries.

## Security & Operations
- OAuth2 or JWT authentication with tenant-aware filters.
- Scoped API keys for integrators; rate limiting and usage analytics.
- Error logging with correlation IDs for traceability.

## Delivery Formats
- **Webhook payloads**: Ranked leak list with score, rank, confidence band, rationale, and lineage references.
- **Exports**: CSV/JSON for batch workflows; PDF summaries for field teams.
- **Alerts**: Email or Slack notifications for MVP users.
