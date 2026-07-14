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


def test_kannada_export_produces_a_valid_pdf_with_correct_text():
    """
    Proves generate_pdf_local produces a real, readable PDF with Kannada
    Unicode text, correctly extracted using NotoSansKannada.
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

    # Asserting the Kannada text is present and correctly extracted
    assert "ಚೈನ್" in text
    assert "ಮಾರುಕಟ್ಟೆ" in text
