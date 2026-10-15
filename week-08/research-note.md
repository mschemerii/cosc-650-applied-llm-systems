# Week 8 Capstone Research Note — Meeting-to-Action Assistant

## Research question

Can a small integrated meeting-analysis pipeline improve extraction of confirmed decisions, action items, owners, blockers, and follow-up questions from meeting transcripts without adding unnecessary complexity?

## System under evaluation

The capstone compares three configurations over the same held-out meeting cases:

1. transcript only
2. transcript plus retrieved and reranked operational guidance
3. transcript plus retrieved/reranked guidance and dynamically selected few-shot examples

The final architecture is selected from measured results rather than assumed model capability.

## Reused course techniques

- Week 3: structured prompting and output discipline
- Week 4: deterministic schema validation and failure handling
- Week 5: MiniLM embeddings plus FAISS retrieval
- Week 6: local cross-encoder reranking
- Week 7: dynamic few-shot retrieval and held-out evaluation discipline

## Models and responsibilities

Gemini Flash handles reasoning-heavy extraction, owner/coreference interpretation, executive synthesis, and the LLM-as-judge pass. MiniLM and the cross-encoder run locally for retrieval and reranking. Python handles orchestration, validation, metrics, matching, logging, and the targeted mitigation.

## Held-out evaluation

The self-contained notebook embeds **10 held-out synthetic meeting transcript cases**. Each case has gold references for decisions, action items and owners, blockers, and follow-up questions.

Deterministic metrics include decision precision/recall/F1, action-item precision/recall/F1, owner accuracy, blocker F1, follow-up-question F1, structured-output validity, and latency.

The LLM-as-judge pass scores exactly three named dimensions on all held-out outputs:

- correctness
- grounding
- operational usefulness

## Required failure mode

The primary failure under investigation is a suggestion or discussion point being incorrectly promoted to a confirmed decision.

The A/B/C ablation is used to trace whether a failure is most likely caused by dynamic few-shot context, retrieved context, or the generation/extraction stage.

## Mitigation

A narrow deterministic evidence filter removes a predicted decision when its cited evidence contains hedging/suggestion language without a clear commitment cue. The mitigation is evaluated against decision F1 to determine whether it reduces false positives without creating excessive false negatives.

## Free-tier and reproducibility controls

A completely uncached 10-case, three-configuration run is capped at 30 synthesis calls and 30 judge calls. The notebook keeps responses in an in-memory cache and prints a `CACHE_EXPORT` JSON string at the end. That string can be pasted back into the notebook's `PRELOADED_CACHE_JSON` variable before a later clean rerun, preserving a single-file, self-contained submission.

## Measured results

Complete this section only after executing `week8_meeting_to_action_capstone.ipynb` top to bottom with a real Gemini API key.

Record:

- the A/B/C deterministic metric table
- the three judge-dimension averages
- the identified failure case and responsible component
- mitigation before/after results
- the final architecture decision and why the measurements support it

No result should be claimed before it appears in the executed notebook output.
