import re
from typing import Tuple, Dict, Any

# English and Kannada pronouns/anaphora
_CONTEXT_TRIGGERS = {
    "he", "him", "his", "she", "her", "hers", "they", "them", "their", 
    "that", "those", "this", "these", 
    "associate", "associates", "suspect", "suspects", "case", "cases",
    "ಅವನು", "ಅವಳ", "ಅವರ", "ಅದರ", "ಆ", "ಈ", "ಕೇಸ್"
}

def resolve_context(session_id: str, current_query: str, last_turns: list[dict]) -> Tuple[str, dict]:
    """
    Lightweight rule-based coreference resolution.
    If the current query contains a pronoun/anaphora, we extract the context
    from the last turn and append it to the current query so retrieval uses it.
    
    Returns (modified_query_text, inherited_filters)
    """
    if not last_turns:
        return current_query, {}
        
    query_lower = current_query.lower()
    words = set(re.findall(r'\b\w+\b', query_lower))
    
    # Check if any trigger word is in the query (or Kannada substring match)
    triggered = False
    for t in _CONTEXT_TRIGGERS:
        if t in words or (len(t) > 3 and t in query_lower): # Simple heuristic for agglutinative languages
            triggered = True
            break
            
    if not triggered:
        return current_query, {}
        
    last_turn = last_turns[-1]
    inherited_filters = last_turn.get("filters", {})
    
    # Build context string to append
    context_parts = []
    if inherited_filters.get("district"):
        context_parts.append(inherited_filters["district"])
    if inherited_filters.get("modus_operandi_keyword"):
        context_parts.append(inherited_filters["modus_operandi_keyword"])
        
    if context_parts:
        context_str = " ".join(context_parts)
        modified_query = f"{current_query} (Context: {context_str})"
        return modified_query, inherited_filters
        
    return current_query, {}
