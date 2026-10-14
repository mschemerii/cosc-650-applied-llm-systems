# Week 8 Discussion — External Dependency Threat Model

## Initial Post

The external dependency I would threat-model for my capstone is the Google Gemini API. My project relies on Gemini for response synthesis and for the LLM-as-judge evaluation required by the capstone. The retrieval and ranking pieces can run locally, but the final generated answer and judge scores still depend on a service I do not control.

Several concrete changes could break the system. Google could retire or rename the model I configured, change free-tier rate limits, reduce daily quotas, or modify API behavior around structured output. A request that works today could begin returning quota errors, unsupported-model errors, or output that no longer matches the expected schema. Even an SDK update could change how responses or tool results are represented.

I would detect those failures in a few ways. First, I would keep a small smoke test that sends a known prompt to the configured model and verifies that the response is valid. Second, the capstone evaluation set would double as a regression test: if parsing failures increase or judge scores suddenly collapse, that signals a dependency problem. I would also log API errors separately from retrieval or application errors so the source of the failure is visible instead of being mistaken for a bad prompt or bad retriever.

My mitigation would be to keep the Gemini model name configurable, validate every structured response, cache completed evaluation calls, and add retry/backoff for temporary rate-limit failures. I would also keep synthesis and judging isolated enough that I could switch to another supported Gemini model without rewriting the retrieval pipeline.

That mitigation adds some code and can add latency during retries, but I think it is worth the cost. I would not build a full multi-provider abstraction for this capstone because that would add complexity without improving the assignment. The smaller safeguards address the failures that are most likely to affect a free-tier course project.
