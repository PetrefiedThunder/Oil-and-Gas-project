# Methane Leak Prioritization Engine (MLPE)

A machine learning production environment for ingesting, normalizing, scoring, and ranking methane leak detections from multiple sources (satellites, sensors, SCADA, aerial surveys) in oil and gas operations.

## Overview

The MLPE platform orchestrates:
- **Data Ingestion**: Multi-source connectors (streaming, batch, APIs) with validation
- **Normalization & Fusion**: Spatial-temporal clustering to merge duplicate detections
- **Scoring & Ranking**: ML-based prioritization with explainability
- **Output APIs**: REST endpoints for querying ranked leaks and dispatching to CMMS
- **Feedback Loop**: Field validation capture to improve future model performance
- **QA & Audit**: Lineage tracking, compliance guardrails, and quality gates

## Documentation

Comprehensive documentation for the MLPE platform lives in the `docs/` directory:
- [Architecture](docs/architecture.md) - System overview and component diagram
- [Ingestion](docs/ingestion.md) - Data sources, validation, and curation
- [Normalization & Fusion](docs/fusion.md) - Spatial-temporal clustering logic
- [Scoring & Model Serving](docs/scoring.md) - Ranking engine and serving topology
- [Output APIs](docs/output_apis.md) - REST endpoints and integrations
- [QA & Delivery](docs/qa_assurance.md) - Testing strategy and deployment pipeline

## Quick Start

```bash
# Install dependencies
pip install -e ".[dev]"

# Run the API server
uvicorn mlpe.app:app --reload

# Run tests
pytest tests/
```

## Project Structure

```
mlpe/
├── src/mlpe/          # Main application code
│   ├── api/           # FastAPI routers and endpoints
│   ├── ingestion/     # Data ingestion pipelines
│   ├── normalization/ # Fusion and clustering logic
│   ├── scoring/       # Ranking engine
│   ├── feedback/      # Field validation tracking
│   ├── explainability/# Rationale generation
│   ├── audit/         # Lineage and compliance
│   └── models.py      # Pydantic data models
├── tests/             # Test suite
├── docs/              # Architecture and design docs
└── config/            # Configuration templates
```
