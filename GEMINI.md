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
