# Circular Dependencies Analysis

**Generated**: 2026-01-13
**Project**: MLPE - Methane Leak Prioritization Engine

## Executive Summary

**Status**: NO CIRCULAR DEPENDENCIES DETECTED

The codebase follows a clean layered architecture with unidirectional dependency flow.

---

## Dependency Flow Analysis

### Layer Architecture (Top to Bottom)

```
┌─────────────────────────────────────────────┐
│                  TESTS                       │
│              tests/test_app.py               │
└────────────────────┬────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│              APPLICATION ENTRY               │
│               src/mlpe/app.py                │
└────────────────────┬────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│                API LAYER                     │
│            src/mlpe/api/router.py            │
└────────────────────┬────────────────────────┘
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
┌─────────────────┐   ┌─────────────────────────┐
│  SERVICE LAYER  │   │      DATA MODELS        │
│  - ingestion/   │   │   src/mlpe/models.py    │
│  - normalization│   │                         │
│  - scoring/     │   │                         │
│  - feedback/    │   │                         │
│  - audit/       │   │                         │
│  - explainability│  │                         │
└────────┬────────┘   └─────────────────────────┘
         │                      ▲
         └──────────────────────┘
```

### Dependency Matrix (Verified No Cycles)

| Module | Imports From | Imported By |
|--------|--------------|-------------|
| `models.py` | (none internal) | 6 modules |
| `audit/assurance.py` | (none internal) | router.py |
| `ingestion/pipeline.py` | models.py | router.py |
| `normalization/fusion.py` | models.py | router.py |
| `scoring/engine.py` | models.py | router.py |
| `feedback/manager.py` | models.py | router.py |
| `explainability/rationale.py` | models.py | router.py |
| `api/router.py` | 7 modules above | app.py |
| `app.py` | api/router.py | test_app.py |

---

## Potential Future Risks

### Risk 1: Model Dependency Expansion
**Current State**: All service modules depend on `models.py`
**Risk**: If `models.py` starts importing from service modules (e.g., for validation logic), circular dependency would occur.

**Mitigation**: Keep `models.py` as pure data transfer objects (DTOs) with no business logic.

### Risk 2: Cross-Service Dependencies
**Current State**: Service modules (ingestion, scoring, etc.) do not import from each other
**Risk**: If `scoring/engine.py` needs `ingestion/pipeline.py` for preprocessing, a cycle could form through router.py.

**Mitigation**: Extract shared logic to dedicated utility modules if needed.

---

## Verification Method

Dependency graph traversal using depth-first search confirmed no back-edges exist:

```
Entry points scanned:
  - tests/test_app.py → mlpe.app → mlpe.api.router → [6 service modules] → mlpe.models

All paths terminate at models.py (leaf node with no internal imports)
No module imports any of its ancestors in the import tree.
```

---

## Recommendations

1. **Maintain current architecture** - The star topology with `router.py` as hub and `models.py` as foundation is clean
2. **Add linting rule** - Consider adding `import-linter` to CI to prevent future circular imports
3. **Monitor router.py** - As the orchestration hub, this file will grow; consider splitting by domain if it exceeds 200 lines
