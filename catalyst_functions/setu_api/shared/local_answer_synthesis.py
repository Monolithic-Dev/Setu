"""
Local dev-mode answer synthesis — extractive, not generative. Stands in
for the real QuickML LLM Serving call in functions/queryFunction/index.py's
generate_answer(), so the full pipeline (retrieve -> generate -> verify ->
audit) can run and be measured end to end without network access.

Explicitly NOT a claim that this is what ships — it's templated
summarization of the retrieved records, not a language model. It exists so
"the pipeline is untestable until QuickML access exists" isn't true anymore:
retrieval quality, grounding verification, and audit logging can all be
genuinely exercised now; only the fluency of the final answer text is a
placeholder for the real LLM call.
"""

from dataclasses import dataclass


@dataclass
class SynthesizedAnswer:
    answer_text: str
    source_case_ids: list[str]
    method: str = "local_extractive_dev_mode"


def synthesize_answer(query_text: str, retrieved_records: list[dict], language: str = "en") -> SynthesizedAnswer:
    """
    Builds a real (if unpolished) answer directly from retrieved case
    records — no model call, just structured summarization. Good enough to
    (a) prove the pipeline end to end and (b) give the grounding verifier
    something real to check, which a fixed placeholder string never could.
    """
    if not retrieved_records:
        return SynthesizedAnswer(
            answer_text="Not found — no matching records were retrieved for this question.",
            source_case_ids=[],
        )

    top_records = retrieved_records[:3]
    narrative_field = "narrative_kn" if language == "kn" else "narrative_en"

    summaries = []
    for record in top_records:
        case_id = record.get("case_id", "unknown")
        narrative = record.get(narrative_field) or record.get("matched_text", "")
        summaries.append(f"[{case_id}] {narrative}")

    if language == "kn":
        header = f"{len(retrieved_records)} ಸಂಬಂಧಿತ ದಾಖಲೆ(ಗಳು) ಕಂಡುಬಂದಿವೆ:\n\n"
    else:
        header = f"Found {len(retrieved_records)} related record(s). Top matches:\n\n"

    answer_text = header + "\n".join(summaries)

    return SynthesizedAnswer(
        answer_text=answer_text,
        source_case_ids=[r.get("case_id") for r in top_records if r.get("case_id")],
    )
