# Research Note — Meeting-to-Action Assistant

## Research question

Can a small integrated LLM system turn an existing meeting transcript into a reliable operational brief, and which parts of that workflow actually benefit from retrieval, reranking, dynamic few-shot prompting, and a stronger cloud model?

The project is intentionally narrow. It does not attempt transcription, meeting capture, task automation, email delivery, a user interface, deployment, or multi-agent orchestration. The system ends after producing and evaluating a structured brief.

## System under test

The final system combines prior COSC 650 techniques rather than rebuilding them:

- **Week 3:** structured prompt/output discipline
- **Week 4:** deterministic schema validation and structured failure handling
- **Week 5:** MiniLM embeddings and FAISS retrieval
- **Week 6:** local cross-encoder reranking
- **Week 7:** dynamic few-shot example retrieval and held-out evaluation discipline

Gemini is reserved for the reasoning-heavy extraction and synthesis step. Local deterministic components handle retrieval, reranking, validation, scoring, logging, and the targeted mitigation. Qwen3.5-0.8B is evaluated separately on a narrow classification task to determine whether a small local model is sufficient for any limited role.

## Hypotheses

1. Structured prompting plus deterministic validation should produce a high valid-output rate.
2. Retrieved operational rules may improve ambiguous cases, especially suggestion-versus-decision distinctions.
3. Dynamic few-shot examples may help some cases but can also introduce retrieval-induced label bias, as observed in Week 7.
4. A small local 0.8B model may be adequate for narrow span classification but is likely to be less reliable for full transcript interpretation, owner resolution, and executive synthesis.

## Held-out evaluation

The project uses **12 held-out transcript cases** that are not used as few-shot demonstrations. The cases include:

- explicit decisions
- suggestions that must not be promoted to decisions
- action items with named owners
- cross-speaker owner references
- blockers mixed with ordinary status
- answered versus unresolved questions
- meetings with no confirmed decision

Gold labels are defined before model execution.

## Ablation

Three configurations are evaluated on the same held-out set:

1. **A — transcript only**
2. **B — transcript + retrieved/reranked operational rules**
3. **C — transcript + retrieved/reranked rules + dynamic few-shot examples**

This isolates whether retrieval and dynamic examples materially improve the system instead of assuming that added context is beneficial.

## Metrics

Deterministic metrics include:

- decision precision, recall, and F1
- action-item precision, recall, and F1
- owner accuracy
- blocker F1
- follow-up-question F1
- structured-output validity rate
- transcript-evidence support rate
- latency

The LLM-as-judge pass scores every held-out case on three named dimensions:

- **correctness**
- **grounding**
- **operational usefulness**

Each judge dimension uses a 1–5 scale.

## Required failure mode

The primary expected failure is:

> A suggestion, possibility, or discussion point is incorrectly reported as a confirmed decision.

The notebook automatically searches for a decision-F1 regression between the ablations. It first tests whether dynamic few-shot context caused the regression, then whether retrieved context caused it. If neither retrieval stage regresses, it attributes the lowest-scoring case to the generation/extraction stage rather than inventing a retrieval failure.

The trace records the transcript, gold answer, outputs for A/B/C, retrieved rules, retrieved examples, and reranker scores.

## Mitigation

A small deterministic evidence filter targets the known failure mode. A predicted decision is removed when its supporting evidence contains suggestion/hedging language but no commitment cue.

The mitigation is evaluated separately so that any gain in decision precision can be weighed against possible recall loss.

## Model comparison

Qwen3.5-0.8B is not forced into the final architecture. It is evaluated on 20 short held-out-style spans across five labels:

- `decision`
- `action_item`
- `blocker`
- `follow_up_question`
- `context`

The comparison records classification accuracy and local inference latency. The final model choice is based on measured performance rather than an assumption that either local or cloud inference is inherently better.

## Results status

The implementation and evaluation harness are complete, but measured Gemini and judge results must come from an actual notebook execution with `GEMINI_API_KEY`. The notebook intentionally does **not** substitute fabricated or gold-derived outputs when the API is unavailable.

Before submission, the executed notebook should contain:

- A/B/C metric tables for all 12 cases
- the three-dimension judge pass
- the selected failure trace
- the mitigation comparison
- the final system-selection conclusion
- the optional local-model result if the llama.cpp comparison is run

The measured results from that execution should be summarized here before the final merge.
