"""FastAPI application initialization for DeployAgent."""
from fastapi import FastAPI
from .routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="DeployAgent FDE Platform API",
        description="Forward-Deployed AI Agent for Enterprise Customer Workflows and Integration",
        version="1.0.0"
    )
    app.include_router(router, prefix="/api/v1")
    return app


app = create_app()
