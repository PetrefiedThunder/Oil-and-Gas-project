# High-Risk Modules Analysis

**Generated**: 2026-01-13
**Project**: MLPE - Methane Leak Prioritization Engine

---

## Risk Ranking Summary

| Rank | Module | Coupling Score | Risk Level | Primary Concern |
|------|--------|---------------|------------|-----------------|
| 1 | `api/router.py` | 85 | **CRITICAL** | Hub file, shared mutable state |
| 2 | `models.py` | 75 | **HIGH** | Central dependency, 6 importers |
| 3 | `app.py` | 15 | MEDIUM | Entry point side effects |
| 4 | All service modules | 10-15 | LOW | Minimal coupling |

---

## CRITICAL RISK: `src/mlpe/api/router.py`

### Metrics
- **Lines**: 78
- **Imports**: 7 internal modules
- **Imported by**: 1 module (app.py)
- **Coupling Score**: 85/100
- **Risk Level**: CRITICAL

### Issues Identified

#### Issue 1: Hub File Anti-Pattern
**Evidence** (router.py:7-13):
```python
from mlpe.audit.assurance import AuditLog
from mlpe.explainability.rationale import RationaleBuilder
from mlpe.feedback.manager import FeedbackManager
from mlpe.ingestion.pipeline import IngestionPipeline
from mlpe.models import DetectionSource, FeedbackItem, LeakEvent, Location, RankedLeakResponse
from mlpe.normalization.fusion import FusionEngine
from mlpe.scoring.engine import ScoreEngine
```
**Impact**: Any change to any of these 7 modules requires router.py regression testing.

#### Issue 2: Shared Mutable Global State (Common Coupling)
**Evidence** (router.py:23-29):
```python
ingestion_pipeline = IngestionPipeline()
fusion_engine = FusionEngine()
scoring_engine = ScoreEngine()
feedback_manager = FeedbackManager()
audit_log = AuditLog()
rationale_builder = RationaleBuilder()
leak_events: List[LeakEvent] = []
```
**Impact**:
- Module-level instantiation prevents dependency injection for testing
- `leak_events` is mutable global state shared across requests
- Memory leak potential: list grows unbounded during server lifetime

#### Issue 3: Mixed Concerns
**Evidence**: Same file handles:
- Health checks (line 32-34)
- Data ingestion (line 37-43)
- Leak ranking (line 46-53)
- Feedback submission (line 56-59)
- Demo data seeding (line 62-78)

**Recommendation**: Split into domain-specific routers (`health_router`, `ingest_router`, `ranking_router`, `feedback_router`)

### Blast Radius
- **Direct dependents**: 1 (app.py)
- **Transitive dependents**: 2 (app.py → test_app.py)
- **Affected tests**: ALL tests in test_app.py (3 tests)

---

## HIGH RISK: `src/mlpe/models.py`

### Metrics
- **Lines**: 48
- **Imports**: 0 internal modules
- **Imported by**: 6 modules
- **Coupling Score**: 75/100
- **Risk Level**: HIGH

### Issues Identified

#### Issue 1: High Fan-Out (Afferent Coupling)
**Evidence**: Imported by:
1. `api/router.py`
2. `ingestion/pipeline.py`
3. `normalization/fusion.py`
4. `scoring/engine.py`
5. `explainability/rationale.py`
6. `feedback/manager.py`

**Impact**: Any schema change cascades to 6+ modules.

#### Issue 2: Deprecated API Usage
**Evidence** (router.py:69 using models):
```python
metadata={"coordinates": sample_location.dict()},
```
**Impact**: Pydantic v2 deprecates `.dict()` in favor of `.model_dump()`. Will cause warnings.

### Blast Radius
- **Direct dependents**: 6 modules
- **Transitive dependents**: 8 modules (including tests)
- **Affected tests**: ALL tests

### Mitigations
1. Current design is intentional (shared DTOs) - acceptable coupling
2. Add migration to replace `.dict()` with `.model_dump()`
3. Consider versioned model namespaces for future breaking changes

---

## MEDIUM RISK: `src/mlpe/app.py`

### Metrics
- **Lines**: 19
- **Coupling Score**: 15/100
- **Risk Level**: MEDIUM

### Issues Identified

#### Issue 1: Module-Level Side Effect
**Evidence** (app.py:19):
```python
app = create_app()
```
**Impact**: FastAPI app instantiated on import, not on demand. Affects test isolation.

### Blast Radius
- **Direct dependents**: 1 (test_app.py)
- **Transitive dependents**: 0

---

## LOW RISK: Service Modules

All modules in `ingestion/`, `normalization/`, `scoring/`, `feedback/`, `explainability/`, `audit/` have:
- Coupling score: 10-15
- Single dependency (models.py)
- Single importer (router.py)
- No internal state sharing

**Status**: Well-isolated, low risk.

---

## Risk Mitigation Priority Queue

| Priority | Action | Effort | Impact |
|----------|--------|--------|--------|
| P0 | Fix global `leak_events` list - add persistence or per-request scope | Low | Prevents memory leak |
| P1 | Replace `.dict()` with `.model_dump()` | Low | Removes deprecation warning |
| P2 | Add dependency injection for services in router.py | Medium | Improves testability |
| P3 | Split router.py into domain routers | Medium | Reduces coupling |
