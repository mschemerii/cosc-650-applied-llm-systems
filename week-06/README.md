# Week 6 — Query Transformation and Re-ranking

## Assignment

This week extends the Week 5 RAG retrieval pipeline on the same 16 chunks and same 10 frozen test queries. The experiment adds a query-side transformation and a ranking-side re-ranker, then measures whether either change actually helps.

### Pipeline

- **Baseline:** `sentence-transformers/all-MiniLM-L6-v2` + FAISS cosine retrieval, `k=3`
- **Query transformation:** two unique Gemini `gemini-3.5-flash-lite` rewrites generated in one call per query
- **Transformation-only stage:** reciprocal-rank fusion over the original query and both rewrites, measured before reranking
- **Re-ranking:** local `cross-encoder/ms-marco-MiniLM-L-6-v2` over fused candidates
- **Metrics:** Precision@3, Recall@3, Hit@1, MRR, nDCG@3, and per-query deltas for baseline, transformation-only, and final reranked retrieval

MiniLM is retained as the Week 5 baseline because the saved Week 5 run ranked the gold chunk first for 8/10 queries, while MPNet was already 10/10. That gives this experiment room to measure whether transformation and re-ranking improve ranking rather than starting from a ceiling.

## Files

- `week6_query_transform_rerank.ipynb` — assignment notebook
- `week6_query_cache.json` — created when the notebook runs; stores two unique Gemini rewrites per query so repeated execution does not repeat successful API calls
- `week6_query_transform_rerank_executed.html` — final Canvas submission export after the notebook is run top-to-bottom

## Free-tier behavior

The notebook checks `GEMINI_API_KEY` in Colab Secrets first, then the environment, then a local JupyterLab `.env` file. It generates both rewrites for a query in one Gemini request, so a clean ten-query run requires at most 10 live calls. Cache entries are de-duplicated and accepted only when they contain two unique, non-empty rewrites. Successful rewrites are cached immediately, and 429 responses use retry/backoff handling.

## Measurement structure

The notebook reports three stages separately:

1. Week 5 MiniLM + FAISS baseline
2. Gemini multi-query transformation + RRF before reranking
3. Cross-encoder reranked final results

This separation makes it possible to identify a transformation-specific regression even if the reranker later repairs it. Query types are grouped by retrieval behavior and classified from their measured MRR deltas.

## Run and submission checklist

1. Set `GEMINI_API_KEY` in Colab Secrets, the environment, or a local `.env` file.
2. Run the notebook top-to-bottom on CPU.
3. Confirm every query has two unique rewrites, especially Q04.
4. Inspect the generated rewrites for intent preservation.
5. Confirm the baseline, transformation-only, and reranked metrics and per-query deltas are visible.
6. Confirm Part 3 reports a transformation regression or a justified no-regression result.
7. Save the executed `.ipynb`.
8. Commit `week6_query_cache.json`.
9. Export the executed notebook to HTML for Canvas.
10. Commit the same HTML submission file to this branch.
11. Update the pull request with the fresh measured results and mark it ready for review.

## AI use

ChatGPT was used to debug the Week 6 notebook, preserve the Week 5 evaluation set, and grammatically check/improve documentation. Gemini Flash-Lite is used inside the notebook for the measured query transformations. The student remains responsible for running the experiment, reviewing the generated rewrites, verifying the measurements, and making the final analysis and decisions.
