from functools import lru_cache
from typing import Optional

from pydantic import FieldValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
  """Application configuration loaded from environment or .env."""

  sap_is_api_base_url: str
  sap_is_api_key: str
  sap_is_test_api_url: Optional[str] = None
  google_api_key: str
  gemini_model: str = "gemini-1.5-pro"
  chroma_host: Optional[str] = None
  chroma_port: int = 8000
  log_level: str = "INFO"

  model_config = SettingsConfigDict(
      env_file=".env",
      env_file_encoding="utf-8",
      extra="ignore",
  )

  @field_validator("sap_is_api_base_url", "sap_is_api_key", "google_api_key")
  @classmethod
  def required_non_empty(cls, value: str, info: FieldValidationInfo):
    if not value or not str(value).strip():
      raise ValueError(
          f"{info.field_name} is required and cannot be empty")
    return value

  @field_validator("sap_is_test_api_url")
  @classmethod
  def empty_optional_to_none(cls, value: Optional[str]) -> Optional[str]:
    if value is None:
      return None
    value = value.strip()
    return value or None

  @field_validator("chroma_port")
  @classmethod
  def valid_port(cls, value: int) -> int:
    if value <= 0:
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
