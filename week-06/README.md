# Week 6 — Query Transformation and Re-ranking

## Assignment

This week extends the Week 5 RAG retrieval pipeline on the same 16 chunks and same 10 frozen test queries. The experiment adds a query-side transformation and a ranking-side re-ranker, then measures whether either change actually helps.

### Pipeline

- **Baseline:** `sentence-transformers/all-MiniLM-L6-v2` + FAISS cosine retrieval, `k=3`
- **Query transformation:** two Gemini `gemini-3.5-flash-lite` rewrites generated in one call per query
- **Transformation-only stage:** reciprocal-rank fusion over the original query and both rewrites, measured before reranking
- **Re-ranking:** local `cross-encoder/ms-marco-MiniLM-L-6-v2` over fused candidates
- **Metrics:** Precision@3, Recall@3, Hit@1, MRR, nDCG@3, and per-query deltas for baseline, transformation-only, and final reranked retrieval

MiniLM is retained as the Week 5 baseline because the saved Week 5 run ranked the gold chunk first for 8/10 queries, while MPNet was already 10/10. That gives this experiment room to measure whether transformation and re-ranking improve ranking rather than starting from a ceiling.

## Files

- `week6_query_transform_rerank.ipynb` — assignment notebook
- `week6_query_cache.json` — created when the notebook runs; stores Gemini rewrites so repeated execution does not repeat successful API calls
- `week6_query_transform_rerank_executed.html` — final Canvas submission export after the notebook is run top-to-bottom

## Free-tier behavior

The notebook checks `GEMINI_API_KEY` in Colab Secrets first, then the environment, then a local JupyterLab `.env` file. It generates both rewrites for a query in one Gemini request, so a clean ten-query run requires at most 10 live calls. Successful rewrites are cached immediately, and 429 responses use retry/backoff handling.

## Measurement structure

The notebook reports three stages separately:

1. Week 5 MiniLM + FAISS baseline
2. Gemini multi-query transformation + RRF before reranking
3. Cross-encoder reranked final results

This separation makes it possible to identify a transformation-specific regression even if the reranker later repairs it. Query types are labeled and classified as benefited, unchanged, or regressed from their measured MRR deltas.

## Run and submission checklist

1. Set `GEMINI_API_KEY` in Colab Secrets, the environment, or a local `.env` file.
2. Run the notebook top-to-bottom on CPU.
3. Inspect the generated query rewrites for intent preservation.
4. Confirm the baseline, transformation-only, and reranked metrics and per-query deltas are visible.
5. Confirm Part 3 reports a transformation regression or a justified no-regression result.
6. Save the executed `.ipynb`.
7. Commit `week6_query_cache.json`.
8. Export the executed notebook to HTML for Canvas.
9. Commit the same HTML submission file to this branch.
10. Update the pull request when the executed artifacts are complete.

## AI use

ChatGPT was used to debug the Week 6 notebook, preserve the Week 5 evaluation set, and grammatically check/improve documentation. Gemini Flash-Lite is used inside the notebook for the measured query transformations. The student remains responsible for running the experiment, reviewing the generated rewrites, verifying the measurements, and making the final analysis and decisions.
