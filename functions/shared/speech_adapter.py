"""
Indic speech adapter — implements docs/Design.md §3's Adapter pattern so
the Conversation Service never talks to Bhashini or Sarvam directly, and
docs/Security.md §3's fallback-chain mitigation for "over-reliance on a
single external speech provider."

TODO (Phase 8): BhashiniProvider and SarvamProvider below have real method
signatures but stubbed HTTP calls — this sandbox has no network access, so
they can't be exercised against the live APIs here. Wire in the actual
endpoints once API keys exist (see .env.example at repo root), and delete
the `raise NotImplementedError` lines. The fallback/orchestration logic in
SpeechService is real and unit-tested (see tests/unit/test_speech_adapter.py)
against mocked providers — that part doesn't change when the stubs are filled in.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


class SpeechProviderError(Exception):
    """Raised when a provider fails or times out — triggers fallback."""


@dataclass
class TranscriptionResult:
    text: str
    language: str
    provider: str


@dataclass
class SynthesisResult:
    audio_bytes: bytes
    provider: str


class SpeechProvider(ABC):
    """Common interface both Bhashini and Sarvam implementations satisfy."""

    name: str

    @abstractmethod
    def transcribe(self, audio_bytes: bytes, language_hint: str) -> TranscriptionResult:
        ...

    @abstractmethod
    def synthesize(self, text: str, language: str) -> SynthesisResult:
        ...


class BhashiniProvider(SpeechProvider):
    """
    Bhashini (National Language Translation Mission) — free tier is
    proof-of-concept only per docs/TechStack.md; fine for the prototype,
    revisit for production per docs/ProductStrategy.md §5.
    """
    name = "bhashini"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def transcribe(self, audio_bytes: bytes, language_hint: str) -> TranscriptionResult:
        # TODO(Phase 8): real Bhashini ASR pipeline call. No network in this
        # sandbox to implement/test against the live endpoint.
        raise NotImplementedError("Wire in real Bhashini ASR call once API access is confirmed.")

    def synthesize(self, text: str, language: str) -> SynthesisResult:
        # TODO(Phase 8): real Bhashini TTS pipeline call.
        raise NotImplementedError("Wire in real Bhashini TTS call once API access is confirmed.")


class SarvamProvider(SpeechProvider):
    """Sarvam AI — verified (docs/AIArchitecture.md §2) to handle Kannada-English code-switching."""
    name = "sarvam"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def transcribe(self, audio_bytes: bytes, language_hint: str) -> TranscriptionResult:
        raise NotImplementedError("Wire in real Sarvam AI STT call once API access is confirmed.")

    def synthesize(self, text: str, language: str) -> SynthesisResult:
        raise NotImplementedError("Wire in real Sarvam AI TTS call once API access is confirmed.")


class SpeechService:
    """
    Orchestrates providers with fallback, per docs/Design.md §3 and
    FR-2.3 (graceful degradation to text-only). This is the part that's
    actually real logic, not a stub — fully covered by
    tests/unit/test_speech_adapter.py using fake providers.
    """

    def __init__(self, providers: list[SpeechProvider]):
        if not providers:
            raise ValueError("SpeechService needs at least one provider.")
        self.providers = providers

    def transcribe(self, audio_bytes: bytes, language_hint: str = "auto") -> TranscriptionResult | None:
        for provider in self.providers:
            try:
                return provider.transcribe(audio_bytes, language_hint)
            except SpeechProviderError:
                continue
        return None  # caller falls back to text-only mode, per FR-2.3

    def synthesize(self, text: str, language: str) -> SynthesisResult | None:
        for provider in self.providers:
            try:
                return provider.synthesize(text, language)
            except SpeechProviderError:
                continue
        return None  # caller falls back to text-only response, per FR-2.3
