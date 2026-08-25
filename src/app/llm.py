from __future__ import annotations

from typing import Any, Protocol

from .settings import load_settings


class TextGenerationProvider(Protocol):
    def generate(
        self,
        *,
        model: str,
        system: str,
        user: str,
        temperature: float,
    ) -> str: ...


class OpenAIResponsesProvider:
    """OpenAI Responses API adapter.

    The SDK import and client creation are lazy so unit tests and other callers
    can construct the pipeline without network credentials. A real generation
    call fails clearly when provider configuration is missing; it never returns
    placeholder prose.
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        timeout_s: float = 60.0,
        client: Any | None = None,
    ):
        self.api_key = api_key
        self.timeout_s = timeout_s
        self._client = client

    def _resolve_client(self) -> Any:
        if self._client is not None:
            return self._client

        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is required for live LinkedIn generation. "
                "Inject a test provider for offline verification."
            )

        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - exercised in deployment environments
            raise RuntimeError(
                "The openai package is required for live LinkedIn generation. "
                "Install project requirements before calling the live provider."
            ) from exc

        self._client = OpenAI(api_key=self.api_key, timeout=self.timeout_s)
        return self._client

    def generate(
        self,
        *,
        model: str,
        system: str,
        user: str,
        temperature: float,
    ) -> str:
        client = self._resolve_client()
        response = client.responses.create(
            model=model,
            instructions=system,
            input=user,
            temperature=temperature,
            store=False,
        )
        text = getattr(response, "output_text", "")
        if not isinstance(text, str) or not text.strip():
            raise RuntimeError("The configured LLM provider returned no text output.")
        return text.strip()


class LLMClient:
    def __init__(
        self,
        model: str | None = None,
        temperature: float = 0.5,
        seed: int | None = None,
        *,
        provider: TextGenerationProvider | None = None,
        api_key: str | None = None,
        timeout_s: float | None = None,
    ):
        cfg = load_settings()
        self.model = model or cfg.llm_model
        self.temperature = temperature
        self.seed = seed  # retained for compatibility; Responses API adapter does not depend on it
        self.timeout_s = float(timeout_s if timeout_s is not None else cfg.llm_timeout_s)
        self._api_key = api_key if api_key is not None else cfg.openai_api_key
        self._provider = provider

    def _resolve_provider(self) -> TextGenerationProvider:
        if self._provider is None:
            self._provider = OpenAIResponsesProvider(
                api_key=self._api_key,
                timeout_s=self.timeout_s,
            )
        return self._provider

    def call(self, system: str, user: str, response_json: bool = True) -> dict[str, Any] | str:
        content = self._resolve_provider().generate(
            model=self.model,
            system=system,
            user=user,
            temperature=self.temperature,
        )
        if response_json:
            return {"text": content}
        return content
