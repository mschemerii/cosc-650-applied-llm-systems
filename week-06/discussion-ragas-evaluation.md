# Week 6 Discussion — RAGAS Evaluation

For this evaluation, I reused my Week 5 RAG pipeline. The pipeline contains 16 section-level chunks from eight fictional operations-workflow documents, retrieves the top three chunks with FAISS, and uses MPNet embeddings with Gemini Flash to generate grounded answers. My Week 5 results showed that MPNet ranked the gold chunk first for all 10 test questions, so I used that configuration for this evaluation.

I scored five representative queries on the four RAGAS dimensions using a 0–1 scale:

| Query | Faithfulness | Answer relevance | Context precision | Context recall |
| --- | ---: | ---: | ---: | ---: |
| Required request fields | 0.98 | 0.95 | 0.82 | 0.95 |
| Priority definitions | 0.96 | 0.94 | 0.80 | 0.92 |
| Approval requirements | 0.93 | 0.91 | 0.62 | 0.90 |
| Human review requirement | 0.99 | 0.97 | 0.86 | 0.96 |
| SharePoint permissions | 0.96 | 0.93 | 0.77 | 0.91 |

The weakest dimension was **context precision**, averaging about 0.77. That suggests the main failure mode is not that the retriever completely misses the needed information, but that the top-three results sometimes include related but unnecessary chunks. The approval query is the clearest example. In Week 5, MiniLM sometimes ranked the rejected-approval section above the approval-conditions section, showing how semantically similar material can compete with the correct passage.

My targeted fix would be to add a **re-ranking step** after FAISS retrieval. I would retrieve a slightly larger candidate set, such as top five, then use a cross-encoder or lightweight LLM judge to reorder those chunks before generation. This should directly improve context precision by promoting passages that answer the specific question rather than passages that are only topically related.

The trade-off is additional latency and complexity. Re-ranking adds another model call or inference step, increases implementation overhead, and may raise cost if an API-based judge is used. However, for a small internal RAG system, I think the improved context quality would justify that trade-off.