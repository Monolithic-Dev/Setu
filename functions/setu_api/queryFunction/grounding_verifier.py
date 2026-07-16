from dataclasses import dataclass
from typing import List
import re

@dataclass
class VerificationResult:
    is_grounded: bool
    checks_passed: List[str]
    checks_failed: List[str]

def verify_answer(answer_text: str, source_texts: List[str]) -> VerificationResult:
    """
    Lightweight check that factual claims in the answer are present in the source text.
    For this prototype, it checks if all sentences in the answer have substantial overlap
    with the source text, acting as a proxy for grounding.
    """
    if not answer_text or not source_texts:
        return VerificationResult(False, [], ["Missing answer or sources"])

    # Basic string overlap checking
    answer_lower = answer_text.lower()
    combined_source = " ".join(source_texts).lower()

    # Split into rough sentences or clauses
    sentences = [s.strip() for s in re.split(r'[.!?\n]', answer_lower) if len(s.strip()) > 10]

    if not sentences:
        return VerificationResult(True, ["No substantive claims to verify"], [])

    checks_passed = []
    checks_failed = []

    for sentence in sentences:
        # Check if most of the words in the sentence exist in the source
        words = set(re.findall(r'\b\w+\b', sentence))
        if not words:
            continue
            
        source_words = set(re.findall(r'\b\w+\b', combined_source))
        overlap = len(words.intersection(source_words)) / len(words)
        
        if overlap > 0.5:  # Require at least 50% word overlap for the sentence
            checks_passed.append(f"Sentence supported (overlap {overlap:.2f}): {sentence[:30]}...")
        else:
            checks_failed.append(f"Sentence unsupported (overlap {overlap:.2f}): {sentence[:30]}...")
            
    is_grounded = len(checks_failed) == 0
    return VerificationResult(is_grounded, checks_passed, checks_failed)
