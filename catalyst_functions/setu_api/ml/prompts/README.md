# QuickML Prompt Templates

System and few-shot prompts for the QuickML LLM Serving calls in
`functions/queryFunction/index.py`'s `generate_answer()`.

Per `docs/AIArchitecture.md` §1, the core prompt must instruct the model to:
1. Answer only from the retrieved context provided
2. Say "not found" rather than fabricate when context is insufficient
3. Cite which retrieved record(s) support each claim

Remember: `functions/shared/grounding_verifier.py` is a backstop for when this
prompt-level instruction doesn't hold (it's a known-leaky control on its own,
per the Phase 7 review) — write the prompt well, but don't rely on it alone.
