# Week 8 — Integrated LLM System

## Capstone: Meeting-to-Action Assistant

The Week 8 capstone is a **Meeting-to-Action Assistant** that turns an existing meeting transcript into a structured operational brief containing:

- executive summary
- decisions made
- action items
- owners
- blockers
- follow-up questions

The project is intentionally small, measurable, and portfolio-ready. It integrates techniques from earlier weeks into one working system instead of treating them as separate exercises.

## Architecture

```text
meeting transcript
      ↓
MiniLM + FAISS retrieval
      ↓
cross-encoder reranking
      ↓
optional dynamic few-shot examples
      ↓
Gemini Flash structured extraction
      ↓
deterministic validation
      ↓
metrics + judge + failure trace + mitigation
      ↓
measured architecture decision
```

Gemini is reserved for reasoning-heavy work: interpreting ambiguous meeting language, resolving owners from context, synthesizing the brief, and performing the LLM-as-judge pass. Retrieval, reranking, validation, matching, metrics, caching, and the targeted mitigation are local or deterministic.

## Integration by reuse

The capstone directly reuses prior course components:

- **Week 3 — structured prompting/output:** stable JSON-oriented output contract and prompt discipline.
- **Week 4 — deterministic validation:** required-field checks and explicit handling of malformed output.
- **Week 5 — retrieval-augmented generation:** `all-MiniLM-L6-v2` embeddings with FAISS retrieval.
- **Week 6 — reranking:** local cross-encoder reranking before context is added to the prompt.
- **Week 7 — dynamic few-shot selection:** semantically similar examples are selected dynamically and tested as a separate condition.

This satisfies the assignment requirement to combine at least three prior techniques while reusing earlier work rather than rebuilding it from scratch.

## Submission notebook

[`week8_meeting_to_action_capstone.ipynb`](week8_meeting_to_action_capstone.ipynb) is the **self-contained capstone notebook** and the authoritative implementation.

The notebook embeds:

- the held-out evaluation set
- retrieval guidance
- few-shot examples
- MiniLM/FAISS retrieval
- cross-encoder reranking
- Gemini prompting
- retry/backoff handling
- in-notebook caching
- deterministic validation
- evaluation metrics
- LLM-as-judge logic
- failure tracing
- mitigation
- Gemini-vs-Qwen comparison
- the dynamically generated research note

It does not depend on project-local Python modules, an external dataset, or a separate research-note file.

## Evaluation

The same **10 held-out meeting cases** are evaluated under three configurations:

1. **A — transcript only**
2. **B — transcript + retrieved/reranked operational guidance**
3. **C — transcript + retrieved/reranked guidance + dynamic few-shot examples**

Concrete metrics include:

- decision precision, recall, and F1
- action-item precision, recall, and F1
- owner accuracy
- blocker F1
- follow-up-question F1
- structured-output validity
- latency

The best deterministic configuration is then evaluated by Gemini-as-judge across all 10 held-out cases on three named dimensions:

- **correctness**
- **grounding**
- **operational usefulness**

This keeps the judge set within the required 10–20 cases while limiting unnecessary free-tier calls.

## Small local-model comparison

The notebook also compares Gemini with **`Qwen/Qwen2.5-0.5B-Instruct`** on a narrower 20-span classification benchmark with these labels:

- `decision`
- `action_item`
- `blocker`
- `follow_up_question`
- `context`

Both models classify the same spans. The notebook reports accuracy and latency for each. Qwen runs locally on CPU with no API cost; Gemini performs the same benchmark in one batched API call.

The purpose of this comparison is not to force the smaller model into the final architecture. It tests whether a small local model is performant enough for a narrow classification role while Gemini remains responsible for ambiguous reasoning and synthesis.

## Required failure mode

The target failure is a suggestion or discussion point being incorrectly promoted to a confirmed decision.

The notebook traces the failure using evidence from the A/B/C comparison and retrieval logs. It attributes the failure to one of three components:

- dynamic few-shot context
- retrieved/reranked context
- generation/extraction

A narrow deterministic filter then removes a predicted decision when its supporting evidence contains suggestion language without a commitment cue. Decision F1 is measured before and after mitigation.

## Reliability and free-tier limits

A fully uncached run is capped at:

- **30 synthesis calls** — 10 held-out cases × 3 configurations
- **10 judge calls** — selected configuration × 10 cases
- **1 Gemini batch classification call** — small-model comparison

Gemini calls use exponential retry/backoff for transient 429 and 5xx errors, including temporary 503 high-demand failures. Completed responses are cached in notebook memory and can be copied into `PRELOADED_CACHE_JSON` before a later clean rerun.

## Research note

The research note is generated **at the end of the notebook from the actual measured variables**. After execution it records and answers:

- the A/B/C deterministic metric table
- which configuration performed best and why
- whether retrieval improved the system
- whether dynamic few-shot prompting improved the system
- the three judge-dimension averages
- the identified failure case and responsible component
- mitigation before/after results
- how local Qwen compared with Gemini
- the final architecture decision and why the measurements support it

No result is claimed before it appears in the executed notebook output.

## Rubric alignment

| Rubric area | Evidence in this project |
| --- | --- |
| Integration by Reuse | Weeks 3–7 components combined into one working system |
| Evaluation | 10 held-out cases, concrete metrics, and Gemini judge on three named dimensions |
| Required Failure Mode | A/B/C comparison, traced component, evidence, and mitigation |
| README and Architecture | This README documents architecture, techniques, rationale, scope, and evaluation |
| Portfolio Curation | Root README prominently links the project and preserves the eight-week story |

## Scope boundaries

The capstone stops after producing and evaluating the operational brief. It does **not** include:

- audio transcription
- live Teams/Zoom integration
- automatic email or task creation
- fine-tuning
- deployment
- a web UI
- multi-agent orchestration

Those capabilities may be reasonable extensions later, but they are intentionally excluded so the submitted system remains small, working, and measured.

---

## Discussion — External Dependency Threat Model

The external dependency I would threat-model for my capstone is the Google Gemini API. My project relies on Gemini for response synthesis and for the LLM-as-judge evaluation required by the capstone. The retrieval and ranking pieces can run locally, but the final generated answer and judge scores still depend on a service I do not control.

Several concrete changes could break the system. Google could retire or rename the model I configured, change free-tier rate limits, reduce daily quotas, or modify API behavior around structured output. A request that works today could begin returning quota errors, unsupported-model errors, or output that no longer matches the expected schema. Even an SDK update could change how responses or tool results are represented.

I would detect those failures in a few ways. First, I would keep a small smoke test that sends a known prompt to the configured model and verifies that the response is valid. Second, the capstone evaluation set would double as a regression test: if parsing failures increase or judge scores suddenly collapse, that signals a dependency problem. I would also log API errors separately from retrieval or application errors so the source of the failure is visible instead of being mistaken for a bad prompt or bad retriever.

My mitigation is to keep the Gemini model name configurable, validate every structured response, cache completed evaluation calls, and use retry/backoff for temporary service or rate-limit failures. Synthesis and judging stay isolated enough that the configured Gemini model can be changed without rewriting the retrieval pipeline.

That mitigation adds some code and can add latency during retries, but it is appropriate for a free-tier course project. I would not build a full multi-provider abstraction because that would add complexity without materially improving the capstone.
