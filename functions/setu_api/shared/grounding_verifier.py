"""
Grounding verification — added in the Phase 7 Judge Review specifically
because prompting an LLM to "only answer from context" is a real but leaky
control on its own (docs/AIArchitecture.md §1). This module is what
actually enforces FR-3.3, not the prompt instruction alone.

v1 here is a cheap lexical-overlap heuristic: good enough to catch the
worst case (an answer citing a source that shares almost no content with
the claim) without an extra paid model call for every response. TODO
(Phase 8, Week 2 per SprintPlan.md): replace or supplement with a real
entailment check — a second, cheaper QuickML call asking "is this claim
supported by this source, yes/no" — once real QuickML access exists to
benchmark whether the heuristic below is actually good enough on its own.
"""

import re
from dataclasses import dataclass


@dataclass
class VerificationResult:
    is_grounded: bool
    overlap_score: float
    reason: str


_STOPWORDS = {
    "the", "a", "an", "is", "was", "were", "in", "on", "at", "to", "of",
    "and", "or", "for", "with", "this", "that", "it", "as", "by",
}


def _tokenize(text: str) -> set:
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 2}


def verify_claim(claim: str, source_texts: list[str], min_overlap: float = 0.25) -> VerificationResult:
    """
    Checks whether `claim` (a sentence or short span from a generated
    answer) shares enough vocabulary with at least one of `source_texts`
    to be plausibly grounded. This is a necessary-but-not-sufficient check —
    it catches unsupported claims, it does not prove correctness.
    """
    claim_tokens = _tokenize(claim)
    if not claim_tokens:
        return VerificationResult(is_grounded=True, overlap_score=1.0, reason="Claim has no checkable content.")

    best_overlap = 0.0
    for source in source_texts:
        source_tokens = _tokenize(source)
        if not source_tokens:
            continue
        overlap = len(claim_tokens & source_tokens) / len(claim_tokens)
        best_overlap = max(best_overlap, overlap)

    is_grounded = best_overlap >= min_overlap
    reason = (
        f"Best source overlap {best_overlap:.0%} "
        f"{'meets' if is_grounded else 'falls below'} the {min_overlap:.0%} threshold."
    )
    return VerificationResult(is_grounded=is_grounded, overlap_score=best_overlap, reason=reason)


def verify_answer(answer_text: str, source_texts: list[str]) -> VerificationResult:
    """
    Verifies a full answer (may be multiple sentences) against all cited
    sources combined. Per docs/AIArchitecture.md §1: an answer that fails
    this check should be regenerated once or returned as "not found" —
    never shown to the user as-is.
    """
    return verify_claim(answer_text, source_texts)
