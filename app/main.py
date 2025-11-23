"""FastAPI application entrypoint."""
from fastapi import FastAPI

from .api.routes import router as api_router
from .core.config import settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(title=settings.app_name)

    application.include_router(api_router, prefix=settings.api_prefix)
    return application


app = create_app()
