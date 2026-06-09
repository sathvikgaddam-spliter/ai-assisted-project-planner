import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ai_provider import (
    DEFAULT_GEMINI_MODEL,
    AIConfigurationError,
    AIProvider,
    AIResponseError,
    GeminiProvider,
    parse_json_response,
)


class FakeProvider(AIProvider):
    provider_name = "fake"
    model_name = "fake-model"

    def __init__(self, text):
        self.text = text

    def is_configured(self):
        return True

    def generate_text(self, prompt, timeout_seconds=60):
        return self.text


def test_parse_json_response_accepts_plain_json():
    payload = parse_json_response('{"status": "ok"}')

    assert payload == {"status": "ok"}


def test_parse_json_response_accepts_markdown_fenced_json():
    payload = parse_json_response('```json\n{"status": "ok"}\n```')

    assert payload == {"status": "ok"}


def test_parse_json_response_rejects_invalid_json():
    with pytest.raises(AIResponseError):
        parse_json_response("not json")


def test_provider_generate_json_returns_normalized_response():
    provider = FakeProvider('{"hello": "world"}')

    response = provider.generate_json("prompt")

    assert response.provider == "fake"
    assert response.parsed_json == {"hello": "world"}


def test_gemini_provider_requires_api_key(monkeypatch):
    monkeypatch.setattr("ai_provider.load_dotenv", lambda: None)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    provider = GeminiProvider(api_key=None)

    assert provider.is_configured() is False
    with pytest.raises(AIConfigurationError):
        provider.generate_text("prompt")


def test_gemini_provider_defaults_to_supported_model(monkeypatch):
    monkeypatch.setattr("ai_provider.load_dotenv", lambda: None)
    monkeypatch.delenv("GEMINI_MODEL", raising=False)

    provider = GeminiProvider(api_key="test-key")

    assert provider.model_name == DEFAULT_GEMINI_MODEL
    assert provider.model_name == "gemini-2.0-flash"


def test_gemini_provider_uses_model_from_environment(monkeypatch):
    monkeypatch.setattr("ai_provider.load_dotenv", lambda: None)
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.0-flash-lite")

    provider = GeminiProvider(api_key="test-key")

    assert provider.model_name == "gemini-2.0-flash-lite"


def test_gemini_provider_constructor_model_overrides_environment(monkeypatch):
    monkeypatch.setattr("ai_provider.load_dotenv", lambda: None)
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.0-flash-lite")

    provider = GeminiProvider(api_key="test-key", model_name="gemini-2.0-flash")

    assert provider.model_name == "gemini-2.0-flash"


def test_gemini_provider_logs_model_without_api_key(monkeypatch, capsys):
    monkeypatch.setattr("ai_provider.load_dotenv", lambda: None)
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.0-flash")

    GeminiProvider(api_key="AIzaSecretValue123456789")

    output = capsys.readouterr().out
    assert "Using Gemini model: gemini-2.0-flash" in output
    assert "AIzaSecretValue" not in output
