from __future__ import annotations
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    openai_api_key: str | None = Field(default=None, env="OPENAI_API_KEY")
    llm_model: str = Field(default="gpt-4o-mini", env="LLM_MODEL")
    llm_timeout_s: int = Field(default=60, env="LLM_TIMEOUT_S")
    env: str = Field(default="dev", env="APP_ENV")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
