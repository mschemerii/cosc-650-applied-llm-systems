# GEMINI.md

This repository contains coursework for COSC-650 Applied LLM Systems.

## Week 6

Week 6 extends the Week 5 retrieval pipeline with Gemini Flash-Lite multi-query transformation and local cross-encoder re-ranking. The notebook keeps the Week 5 corpus and frozen 10-query evaluation set, measures baseline retrieval, transformation-only retrieval, and final reranked retrieval, and reports per-query deltas plus a transformation-specific failure case.

The Week 6 notebook is self-contained. Gemini query rewrites are cached in an in-notebook dictionary during execution and printed into notebook output; no external JSON cache file is required. The executed notebook is exported to HTML for Canvas submission.

Gemini Flash-Lite is used for the measured query transformations. The analysis, measurements, and final decisions are based on the executed notebook results.

## Week 7

Week 7 evaluates no-GPU adaptation for a five-label meeting-transcript classification task: `decision`, `action_item`, `blocker`, `follow_up_question`, and `context`.

The deterministic synthetic dataset contains **250 balanced training examples** and **50 balanced held-out evaluation examples**. The notebook validates format, duplicates, train/evaluation leakage, label balance, and token-length distribution. A predeclared five-example `contrastive_challenge` slice places competing-label language in the held-out inputs to test whether dynamic few-shot retrieval can introduce negative transfer.

Dynamic few-shot selection runs locally with `sentence-transformers/all-MiniLM-L6-v2`. For each evaluated input, the four most relevant training examples are inserted into the prompt. Gemini Flash-Lite is used for both the zero-shot baseline and dynamic few-shot condition.

The primary measured run contains 25 balanced examples and always includes all five challenge cases. If that run contains no few-shot underperformance, the notebook automatically evaluates the remaining held-out examples and recomputes the results over all 50 rather than inventing a failure case.

`GEMINI_API_KEY` is read from Google Colab Secrets. Responses are cached only in memory during the session. No `.env`, Google Drive mount, or JSON cache file is used.

The final results and decision memo are generated from the current executed metrics. The research note is included in the notebook. No fine-tuning is performed; fine-tuning is evaluated only as a future engineering decision.

## Week 8 Capstone

The Week 8 capstone is the **Meeting-to-Action Assistant** in `week-08/`. The authoritative implementation is the self-contained notebook `week-08/week8_meeting_to_action_capstone.ipynb`.

AI assistance was used to scaffold and debug the notebook, evaluation harness, retrieval/reranking integration, deterministic validation, retry/backoff handling, local-model comparison, failure-trace logic, and repository documentation. The measured results, interpretation of those results, and final architecture decision are based on the executed notebook outputs.

The integrated system reuses prior course techniques rather than rebuilding them:

- Week 3 structured prompting/output
- Week 4 deterministic validation and structured failures
- Week 5 MiniLM + FAISS retrieval
- Week 6 cross-encoder reranking
- Week 7 dynamic few-shot retrieval and held-out evaluation discipline

Gemini Flash is used for structured meeting-brief synthesis. The notebook evaluates 10 held-out cases under three ablations, so a fully uncached run is capped at **30 synthesis calls**. The configuration with the highest deterministic extraction score is then judged across all 10 held-out cases on correctness, grounding, and operational usefulness, capped at **10 judge calls**.

The notebook also compares Gemini against **Qwen/Qwen2.5-0.5B-Instruct** on a 20-span five-label classification task (`decision`, `action_item`, `blocker`, `follow_up_question`, `context`). Gemini performs the comparison in one batched API call; Qwen runs locally on CPU. This comparison is supplemental evidence for whether a small local model is good enough for a narrow role and does not force Qwen into the final architecture.

The notebook is self-contained: the held-out cases, retrieval guidance, few-shot examples, prompts, validation code, evaluation metrics, judge logic, failure tracing, mitigation, local Qwen benchmark, and research note are all embedded directly in the notebook. No external project module or dataset is required.

To avoid repeated free-tier calls, the notebook maintains an in-memory response cache and prints a `CACHE_EXPORT` JSON string after execution. That string can be pasted back into the notebook's `PRELOADED_CACHE_JSON` variable before a later rerun, preserving the single-file submission design.

Gemini calls use exponential retry/backoff for transient 429 and 5xx errors, including temporary 503 high-demand responses. Local MiniLM retrieval, cross-encoder reranking, Qwen inference, validation, matching, metrics, and the targeted mitigation run without GPU acceleration.

The research note is generated dynamically at the end of the notebook from measured variables. No model-generated metric or conclusion should be reported as a project result until the notebook has been executed successfully.
