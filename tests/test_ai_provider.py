import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ai_provider import AIConfigurationError, AIProvider, AIResponseError, GeminiProvider, parse_json_response


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
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    provider = GeminiProvider(api_key=None)

    assert provider.is_configured() is False
    with pytest.raises(AIConfigurationError):
        provider.generate_text("prompt")
