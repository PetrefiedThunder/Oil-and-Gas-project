"""API surface for audit and assurance operations."""
from fastapi import APIRouter, Depends

from app.core.config import settings
from app.modules.audit.interfaces import AssuranceChecker, AuditTrail, MockAuditTrail


router = APIRouter(tags=["audit"])


def get_audit_trail() -> AuditTrail:
    if settings.enable_mock_services:
        return MockAuditTrail()
    raise NotImplementedError("Configure a concrete audit trail")


def get_assurance_checker() -> AssuranceChecker:
    if settings.enable_mock_services:
        return MockAuditTrail()
    raise NotImplementedError("Configure a concrete assurance checker")


@router.post("/audit")
def audit_event(event: dict, trail: AuditTrail = Depends(get_audit_trail)) -> dict:
    return trail.record(event)


@router.post("/assure")
def assure_records(
    records: list[dict], checker: AssuranceChecker = Depends(get_assurance_checker)
) -> dict:
    return {"status": "validated", "records": checker.validate(records)}
