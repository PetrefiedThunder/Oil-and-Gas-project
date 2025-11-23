# Methane Leak Prioritization Engine (MLPE)

This repository contains the early scaffolding for the Methane Leak Prioritization Engine, a FastAPI-based service that ingests methane leak detections, normalizes and fuses events, scores and ranks leaks, and exposes ranked outputs with feedback and audit hooks.

## Project Structure
- `docs/`: System design notes covering architecture, ingestion, fusion, scoring, QA/audit, and output APIs.
- `src/mlpe/`: Service skeleton with modular packages for ingestion, fusion, scoring, feedback, explainability, audit, and API routing.
- `requirements.txt`: Minimal runtime dependencies for the FastAPI service.

## Local Development
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Start the API for local testing:
   ```bash
   uvicorn mlpe.app:app --reload
   ```
3. Hit the health check:
   ```bash
   curl http://localhost:8000/health
   ```

## Documentation
- [Architecture](docs/architecture.md)
- [Ingestion](docs/ingestion.md)
- [Normalization & Fusion](docs/fusion.md)
- [Scoring & Explainability](docs/scoring.md)
- [Audit, QA, and Assurance](docs/qa_assurance.md)
- [Output APIs](docs/output_apis.md)
