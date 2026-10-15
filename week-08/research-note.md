# Week 8 Capstone Research Note — Meeting-to-Action Assistant

## Research question

Can a small integrated meeting-analysis pipeline improve extraction of confirmed decisions, action items, owners, blockers, and follow-up questions from meeting transcripts without adding unnecessary complexity?

## System under evaluation

The capstone compares three configurations over the same held-out meeting cases:

1. Transcript only.
2. Transcript plus retrieved and reranked operational guidance.
3. Transcript plus retrieved/reranked guidance and dynamically selected few-shot examples.

The final architecture is selected from measured results rather than assumed model capability.

## Reused course techniques

- Week 3: structured prompting and output discipline.
- Week 4: deterministic schema validation and structured failure handling.
- Week 5: MiniLM embeddings plus FAISS retrieval.
- Week 6: local cross-encoder reranking.
- Week 7: dynamic few-shot retrieval and held-out evaluation discipline.

## Models and responsibilities

Gemini Flash handles reasoning-heavy extraction, owner/coreference interpretation, executive synthesis, and the LLM-as-judge pass. MiniLM and the cross-encoder run locally for retrieval and reranking. Python handles orchestration, validation, metrics, logging, caching, and the targeted mitigation.

A small local model such as Qwen3.5-0.8B may be evaluated on narrow span classification, but it is not forced into the final architecture unless measured results support that role.

## Held-out evaluation

The project uses 12 held-out synthetic meeting transcript cases. Each case has gold references for decisions, actions, owners, blockers, and follow-up questions.

Deterministic metrics include decision precision/recall/F1, action-item precision/recall/F1, owner accuracy, blocker F1, follow-up-question F1, structured-output validity, evidence support, and latency.

The LLM-as-judge pass scores three named dimensions on all held-out cases:

- correctness
- grounding
- operational usefulness

## Required failure mode

The primary failure under investigation is a suggestion or discussion point being incorrectly promoted to a confirmed decision.

The A/B/C ablation and retrieval logs are used to trace whether a failure is most likely caused by dynamic few-shot context, retrieved context, or the generation/extraction stage.

## Mitigation

A narrow deterministic evidence filter removes a predicted decision when its cited evidence contains hedging/suggestion language without a clear commitment cue. The mitigation is evaluated against decision F1 and recall to determine whether it reduces false positives without creating excessive false negatives.

## Free-tier and reproducibility controls

Gemini responses are cached in `data/response_cache.json`. The uncached evaluation is capped at 36 synthesis calls and 36 judge calls for the 12-case, three-configuration evaluation. Subsequent runs reuse cached responses.

## Measured results

Complete this section only after executing `week8_meeting_to_action_capstone.ipynb` top to bottom with a real Gemini API key.

Record:

- the A/B/C deterministic metric table;
- the three judge-dimension averages;
- the identified failure case and responsible component;
- mitigation before/after results;
- local-model results if that optional experiment is run;
- the final architecture decision and why the measurements support it.

No result should be claimed before it appears in the executed notebook output.
