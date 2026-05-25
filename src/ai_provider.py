import json
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - exercised when optional dependency is absent.
    load_dotenv = None


class AIProviderError(Exception):
    """Base exception for normalized AI provider failures."""


class AIConfigurationError(AIProviderError):
    """Raised when a provider cannot be used because configuration is missing."""


class AIResponseError(AIProviderError):
    """Raised when a provider returns unusable or malformed content."""


@dataclass
class AIProviderResponse:
    provider: str
    model: str
    raw_text: str
    parsed_json: Dict[str, Any]


class AIProvider:
    provider_name = "base"
    model_name = "unknown"

    def is_configured(self) -> bool:
        raise NotImplementedError

    def generate_text(self, prompt: str, timeout_seconds: int = 60) -> str:
        raise NotImplementedError

    def generate_json(self, prompt: str, timeout_seconds: int = 60) -> AIProviderResponse:
        raw_text = self.generate_text(prompt, timeout_seconds=timeout_seconds)
        return AIProviderResponse(
            provider=self.provider_name,
            model=self.model_name,
            raw_text=raw_text,
            parsed_json=parse_json_response(raw_text),
        )


class GeminiProvider(AIProvider):
    provider_name = "gemini"

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-flash"):
        if load_dotenv:
            load_dotenv()
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def generate_text(self, prompt: str, timeout_seconds: int = 60) -> str:
        if not self.is_configured():
            raise AIConfigurationError("GEMINI_API_KEY is not configured.")

        try:
            import google.generativeai as genai
        except ImportError as exc:
            raise AIConfigurationError("google-generativeai is not installed.") from exc

        try:
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.2,
                    "response_mime_type": "application/json",
                },
                request_options={"timeout": timeout_seconds},
            )
        except Exception as exc:
            raise AIProviderError(f"Gemini request failed: {exc}") from exc

        text = getattr(response, "text", None)
        if not text:
            raise AIResponseError("Gemini returned an empty response.")
        return text


def parse_json_response(raw_text: str) -> Dict[str, Any]:
    if not raw_text or not raw_text.strip():
        raise AIResponseError("AI response was empty.")

    cleaned = _strip_markdown_fence(raw_text.strip())
    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise AIResponseError(f"AI response was not valid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise AIResponseError("AI response JSON must be an object.")

    return payload


def _strip_markdown_fence(text: str) -> str:
    match = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else text
