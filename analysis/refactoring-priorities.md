# Refactoring Priorities - Technical Debt Ranking

**Generated**: 2026-01-13
**Project**: MLPE - Methane Leak Prioritization Engine

---

## Technical Debt Score: 28/100 (LOW)

The codebase is relatively clean with a few areas needing attention.

---

## Priority Matrix

| Priority | Issue | Severity | Effort | ROI |
|----------|-------|----------|--------|-----|
| **P0** | Memory leak - unbounded list | High | Low | Critical |
| **P1** | Pydantic v2 deprecation | Medium | Low | High |
| **P2** | Global mutable state | Medium | Medium | High |
| **P3** | Hub file coupling | Low | Medium | Medium |
| **P4** | Documentation link mismatch | Low | Low | Low |

---

## P0: CRITICAL - Fix Memory Leak

### Issue
`leak_events: List[LeakEvent] = []` in `router.py:29` grows unbounded.

### Evidence
```python
# router.py:29
leak_events: List[LeakEvent] = []

# router.py:41 - appends without limit
leak_events.append(event)
```

### Impact
- Server memory grows with each ingestion request
- No cleanup mechanism
- Production crash risk under load

### Fix Options

**Option A: Add cleanup endpoint (Recommended for MVP)**
```python
@api_router.delete("/leaks")
def clear_leaks() -> dict:
    global leak_events
    count = len(leak_events)
    leak_events = []
    return {"cleared": count}
```

**Option B: Add persistence layer (Recommended for production)**
```python
# Use database or cache (Redis) for leak storage
# Replace list with repository pattern
```

**Option C: Add max size limit (Quick fix)**
```python
MAX_EVENTS = 10000
if len(leak_events) >= MAX_EVENTS:
    leak_events = leak_events[-MAX_EVENTS//2:]  # Keep recent half
```

---

## P1: Pydantic v2 Deprecation Warning

### Issue
Using deprecated `.dict()` method instead of `.model_dump()`.

### Evidence
```python
# router.py:69
metadata={"coordinates": sample_location.dict()},

# router.py:75
metadata={"coordinates": sample_location.dict()},
```

### Fix
```python
# Replace:
sample_location.dict()
# With:
sample_location.model_dump()
```

### Files Affected
- `src/mlpe/api/router.py` (2 occurrences)

---

## P2: Global Mutable State

### Issue
Module-level service instantiation prevents clean testing.

### Evidence
```python
# router.py:23-29
ingestion_pipeline = IngestionPipeline()
fusion_engine = FusionEngine()
scoring_engine = ScoreEngine()
feedback_manager = FeedbackManager()
audit_log = AuditLog()
rationale_builder = RationaleBuilder()
```

### Impact
- Cannot inject mocks for unit testing
- Services share state across requests
- Difficult to test in isolation

### Recommended Fix
Use FastAPI dependency injection:

```python
# services.py (new file)
from functools import lru_cache

@lru_cache()
def get_ingestion_pipeline() -> IngestionPipeline:
    return IngestionPipeline()

# router.py
from fastapi import Depends

@api_router.post("/ingest/scada")
def ingest_scada(
    payload: IngestPayload,
    pipeline: IngestionPipeline = Depends(get_ingestion_pipeline)
) -> LeakEvent:
    ...
```

---

## P3: Hub File Coupling

### Issue
`router.py` imports 7 internal modules, creating high afferent coupling.

### Current State
```
router.py imports:
├── mlpe.audit.assurance
├── mlpe.explainability.rationale
├── mlpe.feedback.manager
├── mlpe.ingestion.pipeline
├── mlpe.models
├── mlpe.normalization.fusion
└── mlpe.scoring.engine
```

### Recommended Refactoring
Split into domain routers:

```
src/mlpe/api/
├── __init__.py
├── routes/
│   ├── health.py      # /health
│   ├── ingest.py      # /ingest/*
│   ├── ranking.py     # /leaks/*
│   └── feedback.py    # /feedback
└── router.py          # Aggregates sub-routers
```

### Implementation
```python
# router.py (after refactoring)
from fastapi import APIRouter
from mlpe.api.routes import health, ingest, ranking, feedback

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(ingest.router, prefix="/ingest", tags=["ingestion"])
api_router.include_router(ranking.router, prefix="/leaks", tags=["ranking"])
api_router.include_router(feedback.router, tags=["feedback"])
```

---

## P4: Documentation Link Mismatch

### Issue
README.md references non-existent file path.

### Evidence
```markdown
# README.md line 23
- [QA & Delivery](docs/qa_assurance.md)
```

### Fix
```markdown
- [QA & Delivery](docs/qa-assurance.md)
```

---

## Architecture Improvements (Future)

### 1. Add Configuration Layer
Currently no runtime configuration. Consider:
```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    max_leak_events: int = 10000
    enable_demo_data: bool = False

    class Config:
        env_file = ".env"
```

### 2. Add Logging
No logging instrumentation. Add structured logging:
```python
import structlog
logger = structlog.get_logger()

# In endpoints
logger.info("leak_ingested", leak_id=event.leak_id, source_count=len(sources))
```

### 3. Add Input Validation
Current validation is minimal. Consider:
- Geohash format validation
- Coordinate bounds checking
- Source type enumeration

---

## Estimated Refactoring Effort

| Task | Story Points | Sprint |
|------|--------------|--------|
| P0: Memory leak fix | 1 | Current |
| P1: Pydantic deprecation | 0.5 | Current |
| P2: Dependency injection | 3 | Next |
| P3: Router split | 5 | Next |
| P4: Doc fix | 0.5 | Current |
| Config layer | 2 | Future |
| Logging | 2 | Future |

**Total backlog**: ~14 story points
