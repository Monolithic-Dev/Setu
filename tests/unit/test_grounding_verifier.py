import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "functions", "shared"))

from grounding_verifier import verify_answer, verify_claim


def test_well_grounded_claim_passes():
    claim = "The case involved a residential break-in via forced door lock in Mysuru."
    sources = ["A case of residential break-in via forced door lock was registered in Mysuru."]
    result = verify_claim(claim, sources)
    assert result.is_grounded is True


def test_unsupported_claim_fails():
    """This is the scenario the Phase 7 review flagged: a claim the model
    generated that isn't actually backed by what was retrieved."""
    claim = "The suspect was previously convicted of armed robbery in Delhi."
    sources = ["A case of residential break-in via forced door lock was registered in Mysuru."]
    result = verify_claim(claim, sources)
    assert result.is_grounded is False


def test_verify_answer_checks_against_all_sources_combined():
    answer = "Complainant reported a two-wheeler theft in Tumakuru."
    sources = [
        "Unrelated case about cyber fraud in Ballari.",
        "A case of two-wheeler theft was registered in Tumakuru.",
    ]
    result = verify_answer(answer, sources)
    assert result.is_grounded is True


def test_empty_claim_is_trivially_grounded():
    result = verify_claim("   ", ["some source text"])
    assert result.is_grounded is True
