# Scoring & Explainability

## Inputs
- Source type (satellite, sensor, SCADA, aerial)
- Confidence levels and detection strength
- Detection frequency/persistence
- Facility type and criticality score (customer provided)
- Signal age and source latency

## Model Approach
- **Primary**: LightGBM/XGBoost ranking model trained on historical leak/repair data.
- **Fallback**: Rule-based scorer for sparse data or edge cases.
- **Preprocessing**: Feature scaling, encoding, and thresholding for robustness.
- **Validation**: Enforce score range [0,1], uniqueness of ranks, and drift detection on inputs.

## Outputs
- Score (0–1)
- Priority rank
- Confidence band (e.g., high/medium/low)
- Rationale vector for explainability

## Explainability Layer
- SHAP values for ML predictions.
- Rule-based rationale strings for fallback paths.
- UI-ready explanations, e.g., “Persistent high-confidence leak near compressor station.”

## Feedback Loop
- REST endpoint and batch CSV upload to collect feedback: confirmed leak, false positive, already repaired.
- Feedback entries include reviewer ID, timestamp, and status updates.
- Signals feed retraining and threshold adjustments.
