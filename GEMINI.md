# GEMINI.md

This repository contains coursework for COSC-650 Applied LLM Systems.

## Week 6

Week 6 extends the Week 5 retrieval pipeline with Gemini Flash-Lite multi-query transformation and local cross-encoder re-ranking. The notebook keeps the Week 5 corpus and frozen 10-query evaluation set, measures baseline retrieval, transformation-only retrieval, and final reranked retrieval, and reports per-query deltas plus a transformation-specific failure case.

The Week 6 notebook is self-contained. Gemini query rewrites are cached in an in-notebook dictionary during execution and printed into notebook output; no external JSON cache file is required. The executed notebook is exported to HTML for Canvas submission.

Gemini Flash-Lite is used for the measured query transformations. The analysis, measurements, and final decisions are based on the executed notebook results.

## Week 7

Week 7 evaluates no-GPU adaptation for a five-label intent-classification task. The committed synthetic dataset contains 200 balanced training examples and 50 balanced held-out evaluation examples. The notebook validates format, deduplication, train/evaluation leakage, label balance, and token-length distribution.

Dynamic few-shot selection runs locally with `sentence-transformers/all-MiniLM-L6-v2`. Gemini Flash-Lite is the only generative model used for assignment evaluation data. The measured comparison uses the same deterministic 25-example balanced subset for zero-shot and dynamic few-shot conditions, with responses cached to avoid duplicate API calls.

The final analysis must use the executed notebook's measured accuracy and observed failure slice. No fine-tuning is performed. Current Gemini API documentation states that general model tuning is not supported, so fine-tuning is evaluated only as a future decision condition.
