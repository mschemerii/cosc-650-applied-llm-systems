# Week 8 — Integrated LLM System

## Capstone: Meeting-to-Action Assistant

The Week 8 capstone is a **Meeting-to-Action Assistant** that takes an existing meeting transcript and produces a structured operational brief containing:

- executive summary
- decisions made
- action items
- owners
- blockers
- follow-up questions

The implementation is intentionally small and measurable. It reuses techniques from earlier course weeks instead of rebuilding them:

- **Week 3:** structured prompting and structured output
- **Week 4:** deterministic schema validation and failure handling
- **Week 5:** MiniLM embeddings + FAISS retrieval
- **Week 6:** local cross-encoder reranking
- **Week 7:** dynamic few-shot example selection and held-out evaluation discipline

### Submission notebook

[`week8_meeting_to_action_capstone.ipynb`](week8_meeting_to_action_capstone.ipynb) is the **self-contained capstone notebook** and the primary submission artifact. The held-out evaluation cases, retrieval corpus, few-shot examples, prompts, validation, metrics, Gemini calls, judge pass, failure tracing, mitigation, and final research note are all defined inside the notebook. It does not require a project-local Python module, external dataset file, or separate research-note file.

The notebook evaluates three configurations over **10 held-out cases**:

1. transcript only
2. transcript + retrieved/reranked operational guidance
3. transcript + retrieved/reranked guidance + dynamic few-shot examples

Concrete metrics include decision/action extraction quality, owner accuracy, blocker and follow-up-question accuracy, structured-output validity, and latency. Gemini also judges all held-out outputs on **correctness, grounding, and operational usefulness**.

The required failure mode is a suggestion/discussion point being incorrectly promoted to a confirmed decision. The notebook uses the A/B/C comparison to trace the error to dynamic few-shot context, retrieved context, or the generation stage, then measures a narrow deterministic mitigation.

### Research note

The research note is generated **at the end of the notebook from the actual measured variables**. After execution it records:

- the A/B/C deterministic metric table
- the three judge-dimension averages
- the identified failure case and responsible component
- mitigation before/after results
- the final architecture decision and why the measurements support it

No result is claimed before it appears in the executed notebook output.

### Scope boundaries

The capstone stops after producing and evaluating the operational brief. It does not include audio transcription, live Teams/Zoom integration, automatic email/task execution, fine-tuning, deployment, a web UI, or multi-agent orchestration.

---

## Discussion — External Dependency Threat Model

The external dependency I would threat-model for my capstone is the Google Gemini API. My project relies on Gemini for response synthesis and for the LLM-as-judge evaluation required by the capstone. The retrieval and ranking pieces can run locally, but the final generated answer and judge scores still depend on a service I do not control.

Several concrete changes could break the system. Google could retire or rename the model I configured, change free-tier rate limits, reduce daily quotas, or modify API behavior around structured output. A request that works today could begin returning quota errors, unsupported-model errors, or output that no longer matches the expected schema. Even an SDK update could change how responses or tool results are represented.

I would detect those failures in a few ways. First, I would keep a small smoke test that sends a known prompt to the configured model and verifies that the response is valid. Second, the capstone evaluation set would double as a regression test: if parsing failures increase or judge scores suddenly collapse, that signals a dependency problem. I would also log API errors separately from retrieval or application errors so the source of the failure is visible instead of being mistaken for a bad prompt or bad retriever.

My mitigation would be to keep the Gemini model name configurable, validate every structured response, cache completed evaluation calls, and add retry/backoff for temporary rate-limit failures. I would also keep synthesis and judging isolated enough that I could switch to another supported Gemini model without rewriting the retrieval pipeline.

That mitigation adds some code and can add latency during retries, but I think it is worth the cost. I would not build a full multi-provider abstraction for this capstone because that would add complexity without improving the assignment. The smaller safeguards address the failures that are most likely to affect a free-tier course project.
