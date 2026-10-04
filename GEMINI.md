# GEMINI.md

This repository contains coursework for COSC-650 Applied LLM Systems.

## Week 6

Week 6 extends the Week 5 retrieval pipeline with Gemini Flash-Lite multi-query transformation and local cross-encoder re-ranking. The notebook keeps the Week 5 corpus and frozen 10-query evaluation set, measures baseline retrieval, transformation-only retrieval, and final reranked retrieval, and reports per-query deltas plus a transformation-specific failure case.

The Week 6 notebook is self-contained. Gemini query rewrites are cached in an in-notebook dictionary during execution and printed into notebook output; no external JSON cache file is required. The executed notebook is exported to HTML for Canvas submission.

ChatGPT was used to debug the Week 6 notebook, preserve the Week 5 evaluation set, and grammatically check/improve documentation.

Gemini Flash-Lite is used for the measured query transformations. The analysis, measurements, and final decisions are based on the executed notebook results.
