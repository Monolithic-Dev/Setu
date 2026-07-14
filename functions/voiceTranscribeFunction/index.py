"""
Voice Transcribe Function — implements POST /api/voice/transcribe from
docs/APISpec.md. Thin wrapper around functions/shared/speech_adapter.py's
SpeechService — the fallback logic it depends on is real and unit-tested
(tests/unit/test_speech_adapter.py); only the actual provider API calls
are stubbed pending real API keys.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "shared"))

from speech_adapter import SpeechService, BhashiniProvider, SarvamProvider


def build_speech_service(config: dict) -> SpeechService:
    return SpeechService([
        BhashiniProvider(api_key=config.get("BHASHINI_API_KEY", "")),
        SarvamProvider(api_key=config.get("SARVAM_API_KEY", "")),
    ])


def handle_request(audio_bytes: bytes, language_hint: str, config: dict) -> dict:
    service = build_speech_service(config)
    result = service.transcribe(audio_bytes, language_hint)
    if result is None:
        return {"status": "error", "error_code": "SERVICE_UNAVAILABLE",
                "message": "Speech services unavailable — fall back to text input."}
    return {"text": result.text, "language": result.language, "provider": result.provider}
