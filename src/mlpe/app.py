from fastapi import FastAPI

from mlpe.api.router import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Methane Leak Prioritization Engine",
        description=(
            "Service skeleton for ingesting methane leak signals, "
            "scoring events, and exposing ranked outputs via REST."
        ),
        version="0.1.0",
    )
    app.include_router(api_router)
    return app


app = create_app()
