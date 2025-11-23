"""API surface for output delivery operations."""
from fastapi import APIRouter, Depends

from app.core.config import settings
from app.modules.output.interfaces import MockOutputAdapter, OutputAdapter


router = APIRouter(tags=["output"])


def get_output_adapter() -> OutputAdapter:
    if settings.enable_mock_services:
        return MockOutputAdapter()
    raise NotImplementedError("Configure a concrete output adapter")


@router.post("/dispatch")
def dispatch_records(records: list[dict], adapter: OutputAdapter = Depends(get_output_adapter)) -> dict:
    dispatched = adapter.dispatch(records)
    return {"status": "dispatched", "records": dispatched}
