# Dead Code Candidates Analysis

**Generated**: 2026-01-13
**Project**: MLPE - Methane Leak Prioritization Engine

---

## Executive Summary

**Orphan Files Found**: 7 (all are empty `__init__.py` package markers)
**True Dead Code Files**: 0
**Unused Exports**: 5

---

## Empty Package Markers (Not True Dead Code)

These files exist to mark directories as Python packages:

| File | Status | Notes |
|------|--------|-------|
| `src/mlpe/__init__.py` | Empty | Root package marker |
| `src/mlpe/api/__init__.py` | Empty | Package marker |
| `src/mlpe/audit/__init__.py` | Empty | Package marker |
| `src/mlpe/explainability/__init__.py` | Empty | Package marker |
| `src/mlpe/feedback/__init__.py` | Empty | Package marker |
| `src/mlpe/ingestion/__init__.py` | Empty | Package marker |
| `src/mlpe/normalization/__init__.py` | Empty | Package marker |
| `src/mlpe/scoring/__init__.py` | Empty | Package marker |

**Recommendation**: Keep these files. They are necessary for Python package structure.

---

## Unused Exports (Within Codebase)

### 1. `IngestionPipeline.quarantined` property
**Location**: `src/mlpe/ingestion/pipeline.py:23-25`
```python
@property
def quarantined(self) -> List[DetectionSource]:
    return list(self._quarantine)
```
**Analysis**: Property exists but is never called anywhere in the codebase.
**Recommendation**:
- If this is API surface for external consumers: Document and keep
- If internal only: Consider removing or adding monitoring endpoint

### 2. `FeedbackManager.list_feedback()` method
**Location**: `src/mlpe/feedback/manager.py:16-17`
```python
def list_feedback(self) -> List[FeedbackItem]:
    return list(self._items)
```
**Analysis**: Method exists but no API endpoint exposes it.
**Recommendation**: Add `/feedback` GET endpoint or remove if not needed.

### 3. `AuditLog.all()` method
**Location**: `src/mlpe/audit/assurance.py:16-17`
```python
def all(self) -> List[Dict[str, str]]:
    return list(self._entries)
```
**Analysis**: Method exists but no API endpoint exposes it.
**Recommendation**: Add `/audit` GET endpoint for compliance requirements or remove.

### 4. `_seed_demo_events()` function
**Location**: `src/mlpe/api/router.py:62-78`
```python
def _seed_demo_events() -> List[LeakEvent]:
    ...
```
**Analysis**: Called conditionally when `leak_events` is empty. Useful for demo but not production.
**Recommendation**:
- Move to separate demo/fixtures module
- Add configuration flag to disable in production

### 5. `create_app()` factory function return value
**Location**: `src/mlpe/app.py:6-16`
**Analysis**: Function exists but is called once at module level. The `app` global is used directly.
**Recommendation**: Keep - factory pattern is correct for testing flexibility.

---

## Files With No Importers (Leaf Analysis)

| File | Has Importers | Has Imports | Status |
|------|---------------|-------------|--------|
| `tests/test_app.py` | No | Yes | Test file - expected |
| `models.py` | Yes (6) | No | Foundation - expected |
| `audit/assurance.py` | Yes (1) | No | Leaf service - OK |

**Result**: No orphan source files found.

---

## Documentation Files Analysis

| File | Linked From | Status |
|------|-------------|--------|
| `docs/architecture.md` | README.md | Referenced |
| `docs/ingestion.md` | README.md | Referenced |
| `docs/fusion.md` | README.md | Referenced |
| `docs/scoring.md` | README.md | Referenced |
| `docs/output_apis.md` | README.md | Referenced |
| `docs/qa-assurance.md` | README.md (as qa_assurance.md) | **MISMATCH** |

**Issue Found**: README.md references `docs/qa_assurance.md` but file is named `docs/qa-assurance.md` (hyphen vs underscore).

---

## Recommendations

### Immediate Actions
1. **Fix documentation link**: Update README.md line 23 to reference `qa-assurance.md`

### Low Priority
2. **Add API endpoints** for `list_feedback()` and `all()` audit methods if compliance requires
3. **Extract demo fixtures** to separate module with configuration guard

### No Action Required
- Empty `__init__.py` files are necessary
- Test files having no importers is expected
- `create_app()` factory pattern is correct
