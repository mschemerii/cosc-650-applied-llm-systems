# COSC 650 Capstone — Meeting-to-Action Assistant

The **Meeting-to-Action Assistant** converts an existing meeting transcript into a structured operational brief containing:

- executive summary
- decisions made
- action items
- owners
- blockers
- follow-up questions

The goal is not to build a meeting platform. The capstone is one small, measurable LLM system that integrates techniques from earlier COSC 650 work and tests whether each added component actually improves the result.

## Problem

Meeting transcripts contain far more text than someone needs after the call. A useful brief has to distinguish confirmed decisions from suggestions, connect action items to the correct owner, identify real blockers, preserve unresolved questions, and summarize the meeting without inventing commitments.

The hardest planned failure case is intentionally included in the evaluation set:

> A suggestion or discussion point is incorrectly reported as a confirmed decision.

## Architecture

```text
existing meeting transcript
          |
          v
MiniLM + FAISS retrieval
          |
          v
cross-encoder reranking
          |
          +---------------------+
          |                     |
          v                     v
retrieved rules         optional few-shot examples
          |                     |
          +----------+----------+
                     |
                     v
          Gemini structured extraction
                     |
                     v
          deterministic validation
                     |
                     v
          structured operational brief
                     |
                     v
       metrics + judge + failure analysis
```

Gemini is used for the reasoning-heavy part of the system: ambiguous transcript interpretation, owner resolution, synthesis, and structured brief generation. Retrieval, reranking, validation, scoring, logging, and the targeted failure mitigation run locally or deterministically.

## Integration by Reuse

The capstone reuses prior course components instead of rebuilding them.

| Technique | Reused from | Capstone use |
| --- | --- | --- |
| Structured prompting/output | [Week 3](../week-03/) | fixed JSON-oriented operational brief and versioned prompt discipline |
| Deterministic schema validation | [Week 4](../week-04/) | required fields, types, evidence fields, and structured failure handling |
| RAG with MiniLM + FAISS | [Week 5](../week-05/) | semantic retrieval of task-specific operational guidance |
| Cross-encoder reranking | [Week 6](../week-06/) | rerank retrieved rules/examples before generation |
| Dynamic few-shot retrieval | [Week 7](../week-07/) | select semantically similar examples and measure whether they help or regress |

This exceeds the rubric requirement of three integrated prior techniques while keeping the system within one narrow workflow.

## Models

### Gemini

Gemini handles:

- confirmed-decision interpretation
- indirect action-item extraction
- owner/coreference reasoning
- blockers and unresolved questions
- executive summarization
- structured brief generation
- the separate LLM-as-judge pass

The configured model name is an environment variable so a model change does not require rewriting the pipeline.

### Qwen3.5-0.8B local comparison

A small local model is evaluated only on the narrow classification problem:

- `decision`
- `action_item`
- `blocker`
- `follow_up_question`
- `context`

The project does not assume that the local model belongs in the final architecture. Accuracy and latency determine whether it is good enough for a limited role.

### Retrieval models

- `sentence-transformers/all-MiniLM-L6-v2`
- FAISS inner-product search over normalized embeddings
- `cross-encoder/ms-marco-MiniLM-L-6-v2`

Generative models are not used for basic retrieval when local deterministic models are sufficient.

## Evaluation

The repository contains **12 held-out meeting cases** in [`data/eval_cases.json`](data/eval_cases.json). These cases are not used as dynamic demonstrations.

The same cases are evaluated under three ablations:

1. **A — transcript only**
2. **B — transcript + retrieved/reranked operational context**
3. **C — transcript + retrieved/reranked context + dynamic few-shot examples**

Concrete metrics include:

- decision precision, recall, and F1
- action-item precision, recall, and F1
- owner accuracy
- blocker F1
- follow-up-question F1
- structured-output validity rate
- transcript-evidence support rate
- latency

### LLM-as-judge

Every held-out case is also judged on three named 1–5 dimensions:

- **correctness**
- **grounding**
- **operational usefulness**

The notebook compares judge averages across A/B/C rather than judging only the chosen configuration.

## Required Failure Mode

The notebook automatically traces at least one failure to a component using the ablation evidence.

It first looks for a case where configuration C loses decision F1 relative to B, which would implicate the dynamic few-shot context. If that does not occur, it checks B versus A for a retrieval-context regression. If neither retrieval stage causes a regression, the lowest-scoring case is attributed to the generation/extraction stage instead of claiming a retrieval failure without evidence.

The trace prints:

- transcript
- gold reference
- A/B/C outputs and per-case metrics
- retrieved operational rules
- retrieved few-shot examples
- reranker scores

### Mitigation

A narrow deterministic guardrail addresses suggestion-as-decision errors. A proposed decision is filtered when its supporting evidence contains suggestion/hedging language without a commitment cue. The notebook measures the mitigation separately so any precision improvement can be checked against recall loss.

## Project Artifacts

- [`week8_meeting_to_action_capstone.ipynb`](week8_meeting_to_action_capstone.ipynb) — integrated capstone notebook
- [`capstone_core.py`](capstone_core.py) — reusable pipeline, scoring, judge, failure trace, and local-model comparison
- [`data/eval_cases.json`](data/eval_cases.json) — 12 held-out meeting cases with predeclared gold labels
- [`research-note.md`](research-note.md) — research question, hypotheses, evaluation design, failure mode, and final-result location

The Week 8 dependency threat model is documented in [`../week-08/README.md`](../week-08/README.md).

## Running the Capstone

Run from the `project/` directory.

Install dependencies if needed:

```bash
pip install sentence-transformers faiss-cpu openai pandas numpy
```

Set `GEMINI_API_KEY`, then run `week8_meeting_to_action_capstone.ipynb` from top to bottom.

For the optional local comparison, start a llama.cpp OpenAI-compatible server and set:

```bash
export RUN_LOCAL_MODEL=1
export LOCAL_LLM_BASE_URL=http://127.0.0.1:8080/v1
export LOCAL_LLM_MODEL=qwen3.5-0.8b
```

After a complete execution, export the saved notebook:

```bash
jupyter nbconvert --to html week8_meeting_to_action_capstone.ipynb
```

The final notebook contains a submission guard. It reports **READY FOR SUBMISSION** only after the 12-case ablation, LLM-as-judge pass, and failure trace are present.

## Exact Scope

Included:

- existing text transcripts
- local semantic retrieval
- local reranking
- optional dynamic few-shot selection
- Gemini structured extraction/synthesis
- deterministic validation
- small local-model comparison
- 12-case held-out evaluation
- quantitative metrics
- LLM-as-judge evaluation
- ablation study
- required failure trace and mitigation

Explicitly out of scope:

- audio transcription or speech-to-text
- live meeting capture
- Teams/Zoom integration
- calendar integration
- email sending or task creation
- autonomous multi-agent workflows
- fine-tuning
- custom embedding training
- production authentication
- web application development
- cloud deployment
- long-term memory
- automatic execution of extracted actions

The system stops after producing and evaluating the operational brief.

## Submission Status

The implementation and evaluation harness are complete. Final measured Gemini/judge results require an actual execution with `GEMINI_API_KEY`; the notebook deliberately refuses to substitute fabricated results when the API is unavailable. The executed `.ipynb`, HTML export, and measured-result update to the research note are the final submission artifacts.
