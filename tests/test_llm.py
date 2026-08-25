from __future__ import annotations

from types import SimpleNamespace

import pytest

from src.app.llm import LLMClient, OpenAIResponsesProvider
from src.app.settings import load_settings


class FakeProvider:
    def __init__(self, text: str = "Generated draft"):
        self.text = text
        self.calls = []

    def generate(self, **kwargs):
        self.calls.append(kwargs)
        return self.text


class FakeResponses:
    def __init__(self):
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(output_text="Provider draft")


class FakeOpenAIClient:
    def __init__(self):
        self.responses = FakeResponses()


def test_llm_client_uses_injected_provider_without_network():
    provider = FakeProvider()
    client = LLMClient(
        model="test-model",
        temperature=0.25,
        provider=provider,
    )

    result = client.call("system rules", "user request", response_json=True)

    assert result == {"text": "Generated draft"}
    assert provider.calls == [
        {
            "model": "test-model",
            "system": "system rules",
            "user": "user request",
            "temperature": 0.25,
        }
    ]


def test_live_client_fails_closed_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    client = LLMClient(model="test-model", api_key=None)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        client.call("system", "user")


def test_openai_adapter_uses_responses_api_without_storage():
    fake_client = FakeOpenAIClient()
    provider = OpenAIResponsesProvider(client=fake_client)

    text = provider.generate(
        model="test-model",
        system="system rules",
        user="user request",
        temperature=0.4,
    )

    assert text == "Provider draft"
    assert fake_client.responses.calls == [
        {
            "model": "test-model",
            "instructions": "system rules",
            "input": "user request",
            "temperature": 0.4,
            "store": False,
        }
    ]


def test_settings_support_current_and_legacy_model_env_names():
    current = load_settings({"LLM_MODEL": "current-model", "LLM_TIMEOUT_S": "30"})
    legacy = load_settings({"MODEL_NAME": "legacy-model"})

    assert current.llm_model == "current-model"
    assert current.llm_timeout_s == 30.0
    assert legacy.llm_model == "legacy-model"
    assert legacy.llm_timeout_s == 60.0
