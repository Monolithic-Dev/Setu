import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from tests._helpers import load_function_module

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")


def test_english_export_produces_a_valid_pdf_with_correct_text():
    """Proves generate_pdf_local produces a real, readable PDF — not just a
    file that exists, but one whose text survives extraction correctly."""
    import pypdf

    export_index = load_function_module("exportFunction", REPO_ROOT)
    conversation = {
        "query_text": "chain snatching market",
        "answer": "Found 1 related record. [KA-2026-00001] chain snatching near market.",
        "sources": ["KA-2026-00001"],
        "audit_id": "test-audit-en",
    }
    result = export_index.handle_request("test-en", conversation, auth_context={}, output_dir="/tmp")

    assert os.path.exists(result["path"])
    reader = pypdf.PdfReader(result["path"])
    text = reader.pages[0].extract_text()
    assert "chain snatching market" in text
    assert "KA-2026-00001" in text
    assert "test-audit-en" in text


def test_kannada_export_is_currently_broken_pending_unicode_font():
    """
    Documents a CONFIRMED bug, not a hypothetical one: Kannada text
    currently renders as unreadable boxes in the exported PDF, because no
    Kannada-capable font was available in this build environment to
    register with reportlab (only CJK and Latin fonts were present — see
    functions/exportFunction/index.py's comment). This test asserts the
    CURRENT broken behavior on purpose, so that once a real Kannada font
    is wired in (Phase 8, with network access), this test will start
    FAILING — which is the signal to update it to assert correct Kannada
    text extraction instead. A test that silently stayed green through
    that fix would be worse than no test at all.
    """
    import pypdf

    export_index = load_function_module("exportFunction", REPO_ROOT)
    conversation = {
        "query_text": "ಚೈನ್ ಸ್ನ್ಯಾಚಿಂಗ್",
        "answer": "ಮಾರುಕಟ್ಟೆ ಬಳಿ ಘಟನೆ ವರದಿಯಾಗಿದೆ.",
        "sources": ["KA-2026-00001"],
        "audit_id": "test-audit-kn",
    }
    result = export_index.handle_request("test-kn", conversation, auth_context={}, output_dir="/tmp")

    reader = pypdf.PdfReader(result["path"])
    text = reader.pages[0].extract_text()

    # This is the bug: the real Kannada characters are NOT present in the
    # extracted text (they became replacement boxes instead). Asserting
    # their absence, not their presence — see docstring.
    assert "ಚೈನ್" not in text, (
        "Kannada text now extracts correctly — a Unicode font must have been "
        "wired in. Update this test to assert correct extraction instead of "
        "documenting the bug; this is good news, not a new failure."
    )
