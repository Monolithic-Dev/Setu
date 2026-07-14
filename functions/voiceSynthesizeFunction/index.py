"""
Voice Synthesize Function — implements POST /api/voice/synthesize from
docs/APISpec.md. Mirrors voiceTranscribeFunction's structure exactly.
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


def handle_request(text: str, language: str, config: dict) -> dict:
    service = build_speech_service(config)
    result = service.synthesize(text, language)
    if result is None:
        return {"status": "error", "error_code": "SERVICE_UNAVAILABLE",
                "message": "Speech services unavailable — fall back to text-only response."}
    return {"audio_available": True, "provider": result.provider}
