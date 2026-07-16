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


import re

def synthesize_answer(query_text: str, retrieved_records: list[dict], language: str = "en") -> SynthesizedAnswer:
    """
    Builds a smarter extracted answer by reading the narratives and
    ranking sentences by keyword overlap with the query. Demonstrates
    meaningful intelligence synthesis without relying on an external API.
    """
    if not retrieved_records:
        return SynthesizedAnswer(
            answer_text="Not found — no matching records were retrieved for this question.",
            source_case_ids=[],
        )

    top_records = retrieved_records[:3]
    narrative_field = "narrative_kn" if language == "kn" else "narrative_en"

    # Heuristic text scoring
    query_words = set(re.findall(r"\b[a-zA-Z]+\b", query_text.lower()))
    stopwords = {"show", "me", "recent", "cases", "in", "using", "a", "the", "of", "and", "or", "what", "where", "how", "who", "with"}
    query_words = {w for w in query_words if w not in stopwords and len(w) > 2}

    ranked_sentences = []
    for record in top_records:
        case_id = record.get("case_id", "unknown")
        narrative = record.get(narrative_field) or record.get("matched_text", "")
        # Simple sentence split
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', narrative) if len(s.strip()) > 5]
        
        for idx, sentence in enumerate(sentences):
            sent_words = set(re.findall(r"\b[a-zA-Z]+\b", sentence.lower()))
            overlap = len(query_words & sent_words)
            # Boost first sentence as it often has the main subject
            score = overlap + (0.5 if idx == 0 else 0)
            if score > 0:
                ranked_sentences.append((score, case_id, sentence))
            
    if not ranked_sentences:
        # Fallback if no overlap found, just return first sentences
        for record in top_records:
            case_id = record.get("case_id", "unknown")
            narrative = record.get(narrative_field) or record.get("matched_text", "")
            first_sent = narrative.split(".")[0] + "."
            ranked_sentences.append((1.0, case_id, first_sent))

    # Take the top 4 most relevant sentences across all docs
    ranked_sentences.sort(key=lambda x: x[0], reverse=True)
    best_sentences = ranked_sentences[:4]
    
    # Group them back by case ID for a cohesive output
    grouped = {}
    for _, case_id, sent in best_sentences:
        if case_id not in grouped:
            grouped[case_id] = []
        grouped[case_id].append(sent)

    summaries = []
    for case_id, sents in grouped.items():
        summaries.append(f"[{case_id}] {' '.join(sents)}")

    if language == "kn":
        header = f"{len(retrieved_records)} ಸಂಬಂಧಿತ ದಾಖಲೆ(ಗಳು) ಕಂಡುಬಂದಿವೆ:\n\n"
    else:
        header = f"Found {len(retrieved_records)} related record(s). Extracted key insights:\n\n"

    answer_text = header + "\n\n".join(summaries)

    return SynthesizedAnswer(
        answer_text=answer_text,
        source_case_ids=[r.get("case_id") for r in top_records if r.get("case_id")],
        method="local_extractive_smart"
    )
