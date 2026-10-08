# Week 6 — Advanced Retrieval: Transform and Measure

This week extends the Week 5 retrieval pipeline with query transformation and cross-encoder re-ranking, while measuring each stage separately.

## Notebook

- `week6_query_transform_rerank.ipynb`

The notebook is self-contained and includes:

- the same 16 Week 5 chunks;
- the same frozen 10-query Week 5 evaluation set;
- MiniLM + FAISS baseline retrieval;
- Gemini Flash-Lite multi-query transformation;
- two unique rewrites per query;
- reciprocal-rank fusion across the original query and rewrites;
- transformation-only retrieval measurement;
- local cross-encoder re-ranking;
- Precision@3, Recall@3, Hit@1, MRR, and nDCG@3;
- per-query deltas;
- retrieval-behavior query-type analysis;
- a transformation-specific regression case or justified no-regression result.

## Self-contained caching

Gemini rewrites are cached in an in-notebook dictionary during execution and printed into notebook output. No separate JSON cache file is required for this course submission workflow.

The executed notebook output therefore preserves the generated rewrites, measurements, and analysis in one place.

## Submission

Run the notebook top-to-bottom in Colab or Jupyter, save the executed notebook, and export it to HTML for Canvas.

The required submission artifact is:

- `week6_query_transform_rerank_executed.html`

The notebook source remains committed in GitHub, and the executed HTML should also be committed before submission.

## AI use

AI assistance was used to debug the Week 6 notebook, preserve the Week 5 evaluation set, and grammatically check/improve documentation. Gemini Flash-Lite is used for the measured query transformations. The analysis, measurements, and final decisions are based on the executed notebook results.
