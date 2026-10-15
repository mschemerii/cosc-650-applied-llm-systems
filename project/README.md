# COSC 650 Capstone — Meeting-to-Action Assistant

## Project Overview

The capstone project is a **Meeting-to-Action Assistant** that takes a meeting transcript and converts it into a structured operational brief. The goal is to build one small, measurable system that combines techniques from earlier COSC 650 assignments into a realistic end-to-end workflow.

The system identifies and organizes the parts of a meeting that are most useful after the call is over:

- executive summary
- decisions made
- action items
- owners
- blockers
- follow-up questions

The project is intentionally focused. It is not a general-purpose meeting platform, autonomous agent, transcription service, or enterprise workflow system. The capstone concentrates on the quality of extracting operational information from already available transcript text.

## Problem

Meeting transcripts are usually much longer than the information someone needs to act on. Decisions may be stated indirectly, action items may be spread across multiple speakers, owners may be implied rather than named in the same sentence, and suggestions can easily be mistaken for confirmed decisions.

The project tests whether a small retrieval-and-reasoning pipeline can turn that noisy transcript into a reliable operational brief while preserving enough evidence to evaluate where the system succeeds or fails.

A central failure case is distinguishing a **confirmed decision** from a suggestion, possibility, or discussion point.

## Architecture

```text
Meeting transcript
       |
       v
Transcript preparation
       |
       v
MiniLM + FAISS semantic retrieval
       |
       v
Cross-encoder reranking
       |
       +---- optional dynamic few-shot examples
       |
       v
Gemini Flash structured extraction and synthesis
       |
       v
Deterministic schema validation
       |
       v
Structured operational brief
       |
       v
Evaluation, failure trace, and mitigation
```

## Integration by Reuse

The project reuses prior course components instead of rebuilding them.

### Week 3 — Structured prompting/output

The capstone reuses the versioned-prompt and structured-output discipline from Week 3. Gemini is instructed to return a fixed JSON representation rather than unconstrained prose.

### Week 4 — Schema validation and structured failures

Python validation checks required fields and output types. Invalid output is recorded as a measurable system failure instead of being silently accepted.

### Week 5 — Retrieval-Augmented Generation

The project reuses local `sentence-transformers/all-MiniLM-L6-v2` embeddings and FAISS retrieval to select operational guidance relevant to the current transcript.

### Week 6 — Reranking

The retrieved candidates are reranked with the local `cross-encoder/ms-marco-MiniLM-L-6-v2` cross-encoder before they are added to the prompt.

### Week 7 — Dynamic few-shot prompting

The system experimentally retrieves semantically similar labeled examples and adds them as demonstrations. This is measured as an ablation rather than assumed to improve performance.

## Models and Responsibilities

### Gemini Flash

Gemini Flash handles the reasoning-heavy parts of the workflow:

- distinguishing confirmed decisions from suggestions
- identifying action items expressed indirectly
- resolving owners across speakers
- interpreting blockers and unresolved questions
- generating the executive summary
- producing the structured operational brief

Gemini Flash also acts as the LLM judge for the held-out evaluation on three named dimensions: correctness, grounding, and operational usefulness.

### Local retrieval models

Generative models are not used for retrieval when smaller local models are sufficient:

- `all-MiniLM-L6-v2` for embeddings
- FAISS for nearest-neighbor retrieval
- `ms-marco-MiniLM-L-6-v2` cross-encoder for reranking

### Optional small local model

Qwen3.5-0.8B can be evaluated on the narrow five-label span-classification task (`decision`, `action_item`, `blocker`, `follow_up_question`, `context`). The integrated capstone does not depend on this comparison. It should only be reported if it is actually executed and measured.

## Held-Out Evaluation

The evaluation set contains **12 held-out meeting examples**, within the required 10–20 range. The cases include ambiguous suggestions, cross-speaker owner references, blockers mixed with status updates, explicit follow-up questions, and meetings where no decision should be extracted.

The notebook reports:

- decision precision, recall, and F1
- action-item precision, recall, and F1
- owner accuracy
- blocker F1
- follow-up-question F1
- structured-output validity rate
- evidence-support rate
- latency
- LLM-as-judge scores for correctness, grounding, and operational usefulness

## Ablation

The same 12 held-out cases are evaluated under three configurations:

1. **A — transcript only**
2. **B — transcript + retrieved/reranked operational context**
3. **C — transcript + retrieved/reranked context + dynamic few-shot examples**

This directly measures whether retrieval and dynamic demonstrations improve the system enough to justify their additional complexity.

## Required Failure Mode

The declared failure is:

> A suggestion or discussion point is incorrectly reported as a confirmed decision.

The notebook traces the failure using the A/B/C comparison and retrieval logs. If C regresses relative to B, the dynamic few-shot component is implicated. If B regresses relative to A, the retrieved context is implicated. Otherwise the lowest-scoring case is attributed to the generation stage rather than inventing a retrieval failure.

A deterministic mitigation then rejects a predicted decision when its own evidence contains suggestion/hedging language without a commitment cue. The mitigation is measured against the same held-out cases.

## Free-Tier and Reproducibility Controls

The capstone is designed for Jupyter or Google Colab without a GPU.

Gemini API usage is capped and cached:

- maximum 36 live synthesis calls for a completely uncached A/B/C run
- maximum 36 live judge calls for a completely uncached judge pass
- persistent cache: `project/data/response_cache.json`

Once a response has been measured, later runs reuse the cache instead of repeatedly consuming the free-tier quota. The populated cache should be committed with the final executed submission artifacts.

## Repository Artifacts

- [`week8_meeting_to_action_capstone.ipynb`](week8_meeting_to_action_capstone.ipynb) — main executable capstone notebook
- [`capstone_core.py`](capstone_core.py) — retrieval, reranking, validation, scoring, failure-trace, mitigation, and optional local-model functions
- [`capstone_cached.py`](capstone_cached.py) — persistent Gemini caching and live-call limits
- [`data/eval_cases.json`](data/eval_cases.json) — 12 held-out evaluation examples
- [`data/response_cache.json`](data/response_cache.json) — persisted synthesis/judge responses
- [`research-note.md`](research-note.md) — research question, hypotheses, experiment design, and measured conclusions

## Exact Scope

The capstone includes:

- existing text meeting transcripts as input
- local semantic retrieval
- local reranking
- optional dynamic few-shot example selection
- Gemini structured extraction and synthesis
- deterministic output validation
- 12-case held-out evaluation
- quantitative metrics
- LLM-as-judge evaluation
- an A/B/C ablation
- one traced failure mode
- one measured mitigation
- an executable notebook and HTML submission artifact

## Explicitly Out of Scope

To keep the project small enough to finish and evaluate properly, the following are not part of the capstone:

- audio transcription or speech-to-text
- live meeting capture
- Zoom or Microsoft Teams integration
- calendar integration
- email sending
- automatic task creation
- autonomous multi-agent workflows
- hosted vector databases
- fine-tuning
- training a custom embedding model
- production authentication or user accounts
- graphical web application development
- cloud deployment
- long-term conversational memory
- automatic execution of extracted action items

The final system stops after producing and evaluating the structured operational brief.

## Submission Status

The implementation is committed on the capstone branch and pull request. The notebook must still be executed with `GEMINI_API_KEY` before submission so that the repository contains real measurements rather than assumed results.

Before submitting to Canvas:

1. Run `week8_meeting_to_action_capstone.ipynb` from top to bottom.
2. Confirm the final cell reports `READY FOR SUBMISSION`.
3. Commit the executed notebook with outputs.
4. Commit the populated `data/response_cache.json`.
5. Update `research-note.md` with the measured results and final architecture decision.
6. Export the executed notebook to HTML and commit it.
7. Submit the capstone pull-request URL and repository URL in Canvas.

## AI Use

AI assistance was used for scaffolding, debugging, evaluation-harness design, and documentation. The specific usage is documented in the repository-level [`GEMINI.md`](../GEMINI.md). Final analysis, measurements, and architecture decisions must be based on the executed notebook results.
