# GEMINI.md

This repository contains coursework for COSC-650 Applied LLM Systems.

## General workflow

Course work is developed on dedicated branches and submitted through pull requests. Executed notebook outputs are the source of truth for reported measurements. Do not invent or pre-fill metrics, judge scores, failure cases, or architecture conclusions before execution.

The Week 8 capstone uses AI assistance for scaffolding, debugging, and repository documentation. The analysis, measurements, and final decisions must come from the executed notebook results.

## Week 6

Week 6 extends the Week 5 retrieval pipeline with Gemini Flash-Lite multi-query transformation and local cross-encoder reranking. The notebook keeps the Week 5 corpus and frozen 10-query evaluation set, measures baseline retrieval, transformation-only retrieval, and final reranked retrieval, and reports per-query deltas plus a transformation-specific failure case.

The Week 6 notebook is self-contained. Gemini query rewrites are cached in an in-notebook dictionary during execution and printed into notebook output; no external JSON cache file is required. The executed notebook is exported to HTML for Canvas submission.

Gemini Flash-Lite is used for the measured query transformations. The analysis, measurements, and final decisions are based on the executed notebook results.

## Week 7

Week 7 evaluates no-GPU adaptation for a five-label meeting-transcript classification task: `decision`, `action_item`, `blocker`, `follow_up_question`, and `context`.

The deterministic synthetic dataset contains **250 balanced training examples** and **50 balanced held-out evaluation examples**. The notebook validates format, duplicates, train/evaluation leakage, label balance, and token-length distribution. A predeclared `contrastive_challenge` slice tests whether retrieval-selected few-shot examples can introduce negative transfer.

Dynamic few-shot selection runs locally with `sentence-transformers/all-MiniLM-L6-v2`. Gemini Flash-Lite is used for both the zero-shot baseline and dynamic few-shot condition.

The final results and decision memo are generated from measured notebook outputs. No fine-tuning is performed; fine-tuning is evaluated only as an engineering decision.

## Week 8 Capstone

The Week 8 capstone is the **Meeting-to-Action Assistant** in `week-08/`.

The authoritative implementation is:

`week-08/week8_meeting_to_action_capstone.ipynb`

The notebook is self-contained and is the primary submission artifact.

### Problem

The system accepts an existing meeting transcript and produces a structured operational brief containing:

- executive summary
- decisions
- action items and owners
- blockers
- follow-up questions

The project scope intentionally stops at transcript text in and an evaluated operational brief out. It does not include transcription, live Teams/Zoom integration, automatic email/task execution, fine-tuning, deployment, a web UI, or multi-agent orchestration.

### Reused course components

The capstone reuses prior course techniques rather than rebuilding them:

- **Week 3:** structured prompting/output
- **Week 4:** deterministic validation and explicit failure handling
- **Week 5:** MiniLM + FAISS retrieval
- **Week 6:** local cross-encoder reranking
- **Week 7:** dynamic few-shot retrieval and held-out evaluation discipline

### Model responsibilities

**Gemini Flash** is used for reasoning-heavy work:

- meeting-brief synthesis
- ambiguous decision interpretation
- owner/context resolution
- LLM-as-judge evaluation
- one batched narrow-classification comparison against Qwen

**Qwen/Qwen2.5-0.5B-Instruct** is evaluated locally on CPU for a narrow five-label span-classification task:

- `decision`
- `action_item`
- `blocker`
- `follow_up_question`
- `context`

Qwen is not automatically included in the final architecture. Its role is decided from measured accuracy and latency.

**Local/deterministic components** include:

- MiniLM embeddings
- FAISS retrieval
- cross-encoder reranking
- schema/field validation
- deterministic metric calculation
- targeted mitigation

### Evaluation design

The same **10 held-out meeting cases** are run through three configurations:

- **A:** transcript only
- **B:** transcript + retrieved/reranked operational guidance
- **C:** transcript + retrieved/reranked guidance + dynamic few-shot examples

Concrete metrics include decision/action precision, recall and F1, owner accuracy, blocker F1, follow-up-question F1, structured-output validity, and latency.

The best deterministic configuration is then judged on all 10 held-out cases using Gemini across three named dimensions:

- correctness
- grounding
- operational usefulness

The notebook also runs a shared 20-span Gemini-vs-Qwen classification benchmark and reports accuracy and latency.

### Required failure mode

The declared failure is a suggestion or discussion point being incorrectly promoted to a confirmed decision.

The notebook traces the failure using A/B/C comparison evidence and retrieval logs, attributing it to one of:

- dynamic few-shot context
- retrieved/reranked context
- generation/extraction

A deterministic evidence filter is then applied and decision F1 is measured before and after mitigation.

### Reliability and free-tier controls

A completely uncached run is capped at:

- **30 synthesis calls** — 10 cases × 3 configurations
- **10 judge calls** — selected configuration × 10 cases
- **1 Gemini batch classification call** — Qwen comparison

Gemini calls use exponential retry/backoff for transient 429 and 5xx responses, including temporary 503 high-demand failures.

The notebook maintains an in-memory cache and can print/export cache content for reuse in a later clean run while keeping the implementation self-contained.

### Research note

The research note is generated dynamically at the end of the notebook from the actual measured variables. It reports:

- the A/B/C metric table
- best configuration
- retrieval effect
- dynamic few-shot effect
- judge averages
- identified failure and responsible component
- mitigation before/after result
- Gemini-vs-Qwen comparison
- final architecture decision

No capstone result should be claimed until it appears in the executed notebook output.

### AI-use documentation

AI assistance was used to scaffold and debug:

- notebook structure
- retrieval/reranking integration
- deterministic validation
- retry/backoff behavior
- caching
- local-model comparison
- failure-trace logic
- repository and README documentation

The measured results, interpretation of those measurements, and final architecture decision remain based on the student's executed notebook outputs.
