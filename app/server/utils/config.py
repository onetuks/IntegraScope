from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field, FieldValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[3]
ENV_PATH = BASE_DIR / ".env"

class Config(BaseSettings):
    """Application configuration loaded from environment or .env."""

    sap_is_base_url: str
    sap_is_token_url: str
    sap_is_client_id: str
    sap_is_client_secret: str

    google_api_key: str
    gemini_model: str = Field(default="gemini-1.5-pro")
    temperature: float = Field(default=0.2)

    chroma_host: Optional[str] = Field(default="127.0.0.1")
    chroma_port: int = Field(default=8000)

    log_level: str = Field(default="INFO")

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator(
        "sap_is_base_url",
        "sap_is_token_url",
        "sap_is_client_id",
        "sap_is_client_secret",
        "google_api_key",
        "gemini_model",
        "chroma_host",
    )
    @classmethod
    def required_non_empty(cls, value: str, info: FieldValidationInfo):
        if not value or not str(value).strip():
            raise ValueError(f"{info.field_name} is required and cannot be empty")
        return value

    @field_validator("chroma_port", "temperature")
    @classmethod
    def valid_port(cls, value: int) -> int:
        if value < 0:
            raise ValueError("chroma_port must be a positive integer")
        return value

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        return value.upper()


@lru_cache(maxsize=1)
def get_config() -> Config:
    """Return a cached Config instance."""
    return Config()
