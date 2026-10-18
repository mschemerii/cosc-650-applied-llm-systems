# Week 8 — Integrated LLM System

## Capstone: Meeting-to-Action Assistant

The Week 8 capstone is a **Meeting-to-Action Assistant** that takes an existing meeting transcript and produces a structured operational brief containing:

- executive summary
- decisions made
- action items
- owners
- blockers
- follow-up questions

The project is intentionally small and measurable. It reuses earlier course work rather than rebuilding the same techniques from scratch:

- **Week 3 — structured prompting/output:** the capstone uses a stable JSON-oriented operational-brief contract.
- **Week 4 — deterministic validation:** Python validates required fields and exposes malformed outputs instead of silently accepting them.
- **Week 5 — retrieval-augmented generation:** local MiniLM embeddings and FAISS retrieve task-relevant operational guidance.
- **Week 6 — reranking:** a local cross-encoder reranks retrieved guidance and candidate examples before they are added to the prompt.
- **Week 7 — dynamic few-shot prompting:** semantically similar examples are selected dynamically and evaluated as a separate ablation condition.

### Architecture

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
metrics + judge + failure trace
```

Gemini is used only for the reasoning-heavy parts of the workflow: interpreting ambiguous meeting language, resolving owners from context, synthesizing the operational brief, and judging the final selected configuration. Retrieval, reranking, validation, matching, metrics, caching, and the targeted mitigation are local or deterministic.

### Submission notebook

[`week8_meeting_to_action_capstone.ipynb`](week8_meeting_to_action_capstone.ipynb) is the **self-contained capstone notebook** and the primary submission artifact. The held-out evaluation cases, retrieval corpus, few-shot examples, prompts, Gemini calls, retry/backoff logic, in-notebook cache, deterministic validation, evaluation, failure trace, mitigation, local-model comparison, and final research note are all defined directly inside the notebook.

It does not require a project-local Python module, external dataset, or separate research-note file.

### Evaluation

The notebook evaluates three configurations over the same **10 held-out meeting cases**:

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

The configuration with the highest deterministic aggregate extraction score is then evaluated by Gemini-as-judge across all 10 held-out cases on three named dimensions:

- **correctness**
- **grounding**
- **operational usefulness**

This keeps the judge set inside the required 10–20 case range while avoiding unnecessary free-tier calls.

### Small local Qwen comparison

The notebook also measures a small local Qwen model, **`Qwen/Qwen2.5-0.5B-Instruct`**, on a narrower 20-span classification task using these labels:

- `decision`
- `action_item`
- `blocker`
- `follow_up_question`
- `context`

Gemini classifies the same 20 spans in one batched call. The comparison reports accuracy and latency for both models, while Qwen has no API cost. The purpose is not to force the local model into the final architecture; it is to measure whether it is good enough for a limited local role.

### Required failure mode

The target failure is a suggestion or discussion point being incorrectly promoted to a confirmed decision. The notebook uses the A/B/C comparison and retrieval logs to trace the failure to one of three places:

- dynamic few-shot context
- retrieved/reranked context
- generation/extraction

A narrow deterministic filter then removes a predicted decision when its evidence contains suggestion language without a commitment cue. Decision F1 is measured before and after the mitigation.

### Free-tier reliability

The notebook caps an uncached run at:

- 30 synthesis calls — 10 cases × 3 ablations
- 10 judge calls — selected configuration × 10 held-out cases
- 1 Gemini batch-classification call for the Qwen comparison

Completed Gemini responses are cached in notebook memory and can be copied back into `PRELOADED_CACHE_JSON` for a later clean rerun. Gemini calls use exponential retry/backoff for transient 429/5xx errors, including temporary 503 high-demand failures.

### Research note

The research note is generated **at the end of the notebook from the actual measured variables**. After execution it reports and answers:

- the A/B/C deterministic metric table
- which configuration performed best and why
- whether retrieval improved the system
- whether dynamic few-shot prompting improved the system
- the three judge-dimension averages
- the identified failure case and responsible component
- mitigation before/after results
- how the local Qwen model compared with Gemini
- the final architecture decision supported by the measurements

No result is claimed before it appears in the executed notebook output.

### Scope boundaries

The capstone stops after producing and evaluating the operational brief. It does not include audio transcription, live Teams/Zoom integration, automatic email/task execution, fine-tuning, deployment, a web UI, or multi-agent orchestration.

---

## Discussion — External Dependency Threat Model

The external dependency I would threat-model for my capstone is the Google Gemini API. My project relies on Gemini for response synthesis and for the LLM-as-judge evaluation required by the capstone. The retrieval and ranking pieces can run locally, but the final generated answer and judge scores still depend on a service I do not control.

Several concrete changes could break the system. Google could retire or rename the model I configured, change free-tier rate limits, reduce daily quotas, or modify API behavior around structured output. A request that works today could begin returning quota errors, unsupported-model errors, or output that no longer matches the expected schema. Even an SDK update could change how responses or tool results are represented.

I would detect those failures in a few ways. First, I would keep a small smoke test that sends a known prompt to the configured model and verifies that the response is valid. Second, the capstone evaluation set would double as a regression test: if parsing failures increase or judge scores suddenly collapse, that signals a dependency problem. I would also log API errors separately from retrieval or application errors so the source of the failure is visible instead of being mistaken for a bad prompt or bad retriever.

My mitigation is to keep the Gemini model name configurable, validate every structured response, cache completed evaluation calls, and use retry/backoff for temporary service or rate-limit failures. Synthesis and judging stay isolated enough that the configured Gemini model can be changed without rewriting the retrieval pipeline.

That mitigation adds some code and can add latency during retries, but it is appropriate for a free-tier course project. I would not build a full multi-provider abstraction because that would add complexity without materially improving the capstone.
