"""Application configuration using Pydantic settings."""
from functools import lru_cache
from pathlib import Path
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Runtime configuration for the service."""

    app_name: str = Field("OG Data Platform", description="Human readable application name")
    environment: str = Field(
        "development",
        description="Deployment environment indicator (development, staging, production).",
    )
    data_dir: Path = Field(Path("data"), description="Root directory for data staging.")
    model_dir: Path = Field(Path("models"), description="Location for scoring models.")
    api_prefix: str = Field("/api", description="Prefix for all application routes.")
    enable_mock_services: bool = Field(
        True, description="Toggle to enable mock implementations during early development."
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Return a cached instance of application settings."""

    return Settings()


settings = get_settings()
