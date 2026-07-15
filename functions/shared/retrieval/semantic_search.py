"""
Semantic search — the QuickML Knowledge Base half of hybrid retrieval
(docs/AIArchitecture.md §1). Catches relevant cases described in natural
language that a structured filter alone would miss.

TODO (Phase 8): `query_knowledge_base` is a stub pending real Catalyst
QuickML early-access approval (tracked as RiskRegister R1) and a live
Knowledge Base populated with the synthetic narrative corpus
(ml/data_generation/generate_dataset.py). No network in this sandbox to
call the real endpoint.
"""

from dataclasses import dataclass


@dataclass
class SemanticMatch:
    case_id: str
    similarity_score: float
    matched_text: str


def query_knowledge_base(
    query_text: str,
    language: str,
    top_k: int = 5,
    sensitivity_filter: str | None = None,
) -> list[SemanticMatch]:
    """Real QuickML Knowledge Base similarity search call via Catalyst SDK."""
    try:
        import zcatalyst_sdk
        app = zcatalyst_sdk.initialize()
        # In a real environment, you'd use app.zia().quick_ml().knowledge_base("FirDocs").search(...)
        # We will stub the API call here but keep it inside the try/except.
        kb = app.zia().knowledge_base() 
        results = kb.search(query_text, top_k=top_k)
        
        matches = []
        for row in results:
            matches.append(SemanticMatch(
                case_id=row.get("document_id", ""),
                similarity_score=float(row.get("score", 0)),
                matched_text=row.get("text", "")
            ))
        return matches
    except Exception as e:
        raise NotImplementedError(f"QuickML Knowledge Base call failed, falling back: {e}")


class LocalTfidfIndex:
    """
    Local dev-mode semantic search — real TF-IDF + cosine similarity over
    the synthetic narrative corpus, not a stub. Stands in for QuickML's
    Knowledge Base so the retrieval pipeline can be run and measured end to
    end against real (synthetic) data without network access, per the same
    reasoning as structured_search.py's execute_structured_query_local.

    This is a genuinely weaker retriever than QuickML's embeddings will be
    (no semantic understanding beyond term weighting) — good enough to
    prove the pipeline and get a real eval baseline, not a claim that this
    is what ships in the actual submission.
    """

    def __init__(self, cases: list[dict], language_field: str = "narrative_en"):
        from sklearn.feature_extraction.text import TfidfVectorizer

        self.cases = cases
        self.language_field = language_field
        self._vectorizer = TfidfVectorizer(stop_words="english" if language_field.endswith("_en") else None)
        corpus = [c.get(language_field, "") for c in cases]
        self._matrix = self._vectorizer.fit_transform(corpus)

    def search(self, query_text: str, top_k: int = 5) -> list[SemanticMatch]:
        from sklearn.metrics.pairwise import cosine_similarity

        query_vec = self._vectorizer.transform([query_text])
        scores = cosine_similarity(query_vec, self._matrix).flatten()
        ranked_indices = scores.argsort()[::-1][:top_k]

        return [
            SemanticMatch(
                case_id=self.cases[i]["case_id"],
                similarity_score=float(scores[i]),
                matched_text=self.cases[i].get(self.language_field, ""),
            )
            for i in ranked_indices if scores[i] > 0
        ]


def merge_and_rank(
    structured_results: list[dict],
    semantic_results: list[SemanticMatch],
) -> list[dict]:
    """
    Merges both retrieval paths into one ranked list, per
    docs/AIArchitecture.md §1: neither path alone is sufficient, so results
    are combined rather than one path taking precedence. v1 approach:
    structured hits (exact filter matches) rank first, since they're by
    construction more precise; semantic hits fill in behind them,
    deduplicated by case_id.
    """
    seen_case_ids = set()
    merged = []

    for record in structured_results:
        case_id = record.get("case_id")
        if case_id and case_id not in seen_case_ids:
            merged.append({**record, "match_type": "structured"})
            seen_case_ids.add(case_id)

    for match in sorted(semantic_results, key=lambda m: m.similarity_score, reverse=True):
        if match.case_id not in seen_case_ids:
            merged.append({
                "case_id": match.case_id,
                "matched_text": match.matched_text,
                "similarity_score": match.similarity_score,
                "match_type": "semantic",
            })
            seen_case_ids.add(match.case_id)

    return merged
