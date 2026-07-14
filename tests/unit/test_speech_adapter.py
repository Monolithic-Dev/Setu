import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "functions", "shared"))

from speech_adapter import (
    SpeechService, SpeechProvider, SpeechProviderError,
    TranscriptionResult, SynthesisResult,
)


class FakeFailingProvider(SpeechProvider):
    name = "failing"

    def transcribe(self, audio_bytes, language_hint):
        raise SpeechProviderError("simulated timeout")

    def synthesize(self, text, language):
        raise SpeechProviderError("simulated timeout")


class FakeWorkingProvider(SpeechProvider):
    name = "working"

    def transcribe(self, audio_bytes, language_hint):
        return TranscriptionResult(text="ನಮಸ್ಕಾರ", language="kn", provider=self.name)

    def synthesize(self, text, language):
        return SynthesisResult(audio_bytes=b"fake-audio", provider=self.name)


def test_uses_primary_provider_when_healthy():
    service = SpeechService([FakeWorkingProvider()])
    result = service.transcribe(b"audio", "kn")
    assert result is not None
    assert result.provider == "working"


def test_falls_back_to_secondary_when_primary_fails():
    """This is the exact scenario docs/Design.md §3 and docs/Security.md §3 describe:
    Bhashini times out, Sarvam takes over, the caller never sees a hard failure."""
    service = SpeechService([FakeFailingProvider(), FakeWorkingProvider()])
    result = service.transcribe(b"audio", "kn")
    assert result is not None
    assert result.provider == "working"


def test_returns_none_when_all_providers_fail():
    """Caller falls back to text-only mode (FR-2.3) — this is what makes that possible."""
    service = SpeechService([FakeFailingProvider(), FakeFailingProvider()])
    result = service.transcribe(b"audio", "kn")
    assert result is None


def test_synthesize_falls_back_too():
    service = SpeechService([FakeFailingProvider(), FakeWorkingProvider()])
    result = service.synthesize("hello", "en")
    assert result is not None
    assert result.audio_bytes == b"fake-audio"
