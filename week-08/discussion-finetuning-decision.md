# Week 8 Discussion: Should I Fine-Tune It?

My first instinct would be to fine-tune an LLM for an internal renewal assistant that reviews customer renewal data and produces a consistent recommendation for the next renewal proposal. The behavior I would want to change is not simply answering questions correctly, but following a repeatable process: identify the customer, separate full-year and prorated charges, apply the current renewal rules, explain exceptions, and produce a concise output for human review.

At first this sounds like a behavior problem because I want the model to respond in a specific structure and reasoning pattern. However, much of the difficulty is actually a knowledge problem. Renewal rules, source spreadsheets, pricing guidance, and exceptions can change. Fine-tuning those facts into the model would make them harder to update and could cause the model to rely on stale information.

A prompting solution could define the required steps, output format, and guardrails. For example, the system prompt could require the model to cite the supplied renewal data, distinguish prorated charges from full-year charges, and avoid inventing missing values. This would probably solve much of the behavior problem, but long prompts can become brittle as rules and exceptions accumulate.

A RAG solution would retrieve the current renewal procedure, customer-specific records, and relevant policy sections before generation. That solves the freshness problem much better than fine-tuning. Its weakness is that retrieval alone does not guarantee the model will consistently follow the required workflow or format.

My final choice would be **RAG plus a strong structured prompt**, not fine-tuning. I would first measure whether this combination produces reliable outputs. Fine-tuning would only become justified if repeated evaluations showed a persistent behavioral failure, such as ignoring the required sequence or format even when the correct context is retrieved. Distillation would make more sense later if the proven workflow needed to run on a smaller, cheaper local model.
