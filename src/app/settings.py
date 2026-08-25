from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    llm_model: str
    llm_timeout_s: float
    env: str


def _positive_float(raw: str | None, *, default: float, name: str) -> float:
    if raw is None or not raw.strip():
        return default
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number") from exc
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return value


def load_settings(environ: Mapping[str, str] | None = None) -> Settings:
    env = os.environ if environ is None else environ
    api_key = (env.get("OPENAI_API_KEY") or "").strip() or None
    model = (env.get("LLM_MODEL") or env.get("MODEL_NAME") or "gpt-4.1-mini").strip()
    if not model:
        raise ValueError("LLM_MODEL must not be empty")

    return Settings(
        openai_api_key=api_key,
        llm_model=model,
        llm_timeout_s=_positive_float(
            env.get("LLM_TIMEOUT_S"),
            default=60.0,
            name="LLM_TIMEOUT_S",
        ),
        env=(env.get("APP_ENV") or "dev").strip() or "dev",
    )


settings = load_settings()
