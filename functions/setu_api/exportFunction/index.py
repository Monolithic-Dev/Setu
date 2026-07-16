"""
Export Function — implements POST /api/export/pdf from docs/APISpec.md.
Exports a conversation (question, answer, sources, audit trail) as a PDF.

Has a genuine local dev-mode PDF generation path using reportlab (real,
not a stub) — produces an actual readable PDF file, standing in for the
real Stratus upload step (which needs live Catalyst credentials and isn't
locally testable the same way file generation is).
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "shared"))


def build_pdf_content(conversation: dict) -> str:
    """Assembles the text content that goes into the exported PDF, per FR-8.1."""
    lines = [
        f"Query: {conversation.get('query_text', '')}",
        f"Answer: {conversation.get('answer', '')}",
        f"Sources: {', '.join(conversation.get('sources', []))}",
        f"Audit ID: {conversation.get('audit_id', '')}",
        f"Exported: {conversation.get('timestamp', datetime.utcnow().isoformat())}",
    ]
    return "\n".join(lines)


def generate_pdf_local(conversation: dict, output_path: str) -> str:
    """
    Real local dev-mode PDF generation using reportlab — genuinely produces
    a readable PDF file on disk, not a placeholder. Standing in for the
    real Stratus upload (functions/exportFunction's production path),
    which needs live Catalyst credentials this sandbox doesn't have.

    Wraps long text properly (reportlab's canvas doesn't do this for you)
    since an answer or Kannada narrative can easily exceed one line width.
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import simpleSplit
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    font_path = os.path.join(os.path.dirname(__file__), "NotoSansKannada-Regular.ttf")
    pdfmetrics.registerFont(TTFont("NotoSansKannada", font_path))

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    margin = 2 * cm
    y = height - margin
    max_width = width - 2 * margin

    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Setu — Conversation Export")
    y -= 1.2 * cm

    c.setFont("Helvetica", 10)
    fields = [
        ("Query", conversation.get("query_text", "")),
        ("Answer", conversation.get("answer", "")),
        ("Sources", ", ".join(conversation.get("sources", [])) or "(none)"),
        ("Audit ID", conversation.get("audit_id", "")),
        ("Exported", conversation.get("timestamp", datetime.utcnow().isoformat())),
    ]

    for label, value in fields:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin, y, f"{label}:")
        y -= 0.5 * cm
        
        val_str = str(value)
        has_kannada = any('\u0C80' <= c <= '\u0CFF' for c in val_str)
        val_font = "NotoSansKannada" if has_kannada else "Helvetica"
        
        c.setFont(val_font, 10)
        for line in simpleSplit(val_str, val_font, 10, max_width):
            c.drawString(margin, y, line)
            y -= 0.45 * cm
        y -= 0.3 * cm

        if y < margin:
            c.showPage()
            y = height - margin

    c.save()
    return output_path


def handle_request(session_id: str, conversation: dict, auth_context: dict, output_dir: str = "/tmp") -> dict:
    output_path = os.path.join(output_dir, f"export_{session_id}.pdf")
    try:
        # TODO(Phase 8): real Stratus upload path — raises here until wired in,
        # since there's no live Catalyst credential in this sandbox to test against.
        raise NotImplementedError("Wire in real Stratus upload once Catalyst credentials exist.")
    except NotImplementedError:
        generate_pdf_local(conversation, output_path)
        return {"status": "generated_locally", "path": output_path,
                "note": "Dev-mode local file, not a real Stratus URL — see PHASE8_STATUS.md."}
