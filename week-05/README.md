# Week 5: Retrieval-augmented generation

## Assignment: RAG pipeline with retrieval evaluation

[`week5_rag_retrieval_evaluation.ipynb`](week5_rag_retrieval_evaluation.ipynb) is the executed assignment notebook. It runs on CPU in JupyterLab or Colab. Eight fictional documentation pages yield 16 section chunks; ten questions have predeclared relevant chunk IDs. Two local sentence-transformer models embed the same chunks, FAISS retrieves the top three, and Gemini Flash generates answers from those retrieved excerpts. Successful generation responses are cached locally.

| Embedding model | Mean precision@3 | Mean recall@3 | Gold chunk ranked first |
| --- | ---: | ---: | ---: |
| MiniLM | 0.333 | 1.00 | 8/10 |
| MPNet | 0.333 | 1.00 | 10/10 |

Each query has one relevant chunk, so the highest possible precision@3 is 1/3. For Q05, MiniLM ranked the rejected-approval section above the approval-conditions section. Reducing to `k=1` lost the gold chunk; `k=3` retained it. The notebook includes the returned passages, a grounded Gemini generation run, and analysis of the observed results.

For Canvas, export the **executed RAG notebook** to HTML or PDF. Keep the `.ipynb` committed to the Week 5 pull request. The required classmate PR review and its URL are separate from this notebook.

## Discussion: The Chunking Decision

- [`discussion-chunking-decision-canvas.txt`](discussion-chunking-decision-canvas.txt) — Canvas-ready discussion post.
- [`discussion-chunking-decision.md`](discussion-chunking-decision.md) — Markdown copy.
- [`week5_chunking_decision.ipynb`](week5_chunking_decision.ipynb) — validation notebook for three chunking strategies.
- [`week5_chunking_decision.html`](week5_chunking_decision.html) — its HTML export.

This separate experiment uses the `llama.cpp` HTTP Server README pinned to commit `217f81c266a7b7c986ee3d2c58e1cccee05a0744`.
