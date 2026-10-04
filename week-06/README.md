# Week 6 — Query Transformation and Re-ranking

## Assignment

This week extends the Week 5 RAG retrieval pipeline on the same 16 chunks and same 10 frozen test queries. The experiment adds a query-side transformation and a ranking-side re-ranker, then measures whether either change actually helps.

### Pipeline

- **Baseline:** `sentence-transformers/all-MiniLM-L6-v2` + FAISS cosine retrieval, `k=3`
- **Query transformation:** two Gemini `gemini-3.5-flash-lite` rewrites per query
- **Fusion:** reciprocal-rank fusion over the original query and both rewrites
- **Re-ranking:** local `cross-encoder/ms-marco-MiniLM-L-6-v2` over fused candidates
- **Metrics:** Precision@3, Recall@3, Hit@1, MRR, nDCG@3, and per-query deltas

MiniLM is retained as the Week 5 baseline because the saved Week 5 run ranked the gold chunk first for 8/10 queries, while MPNet was already 10/10. That gives this experiment room to measure whether transformation and re-ranking improve ranking rather than starting from a ceiling.

## Files

- `week6_query_transform_rerank.ipynb` — assignment notebook
- `week6_query_cache.json` — created when the notebook runs; stores Gemini rewrites so repeated execution does not repeat API calls
- `week6_query_transform_rerank_executed.html` — final Canvas submission export after the notebook is run top-to-bottom

## Run and submission checklist

1. Set `GEMINI_API_KEY` in Colab Secrets or the notebook environment.
2. Run the notebook top-to-bottom on CPU.
3. Inspect the generated query rewrites and the automatically selected worst regression.
4. Confirm the final measured interpretation matches the displayed tables.
5. Save the executed `.ipynb`.
6. Export the executed notebook to HTML for Canvas.
7. Commit the executed notebook, generated cache, and HTML export to this branch.
8. Update the pull request from draft to ready for review.

## AI use

ChatGPT was used to scaffold and debug the Week 6 notebook, evaluation code, repository documentation, and pull-request structure. Gemini Flash-Lite is used inside the notebook for the measured query transformations. The student remains responsible for reviewing the generated rewrites, measured outputs, failure explanation, and final conclusions before submission.
