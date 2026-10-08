# Week 7 Discussion — Fine-Tuning Decision Framework

## Initial Post

A task where my first instinct would be to fine-tune a model is an internal AI operations assistant that turns meeting transcripts and project notes into consistent executive summaries and action items. The behavior I would want to change is not basic language ability, but consistency: the model should reliably separate decisions, action items, owners, blockers, and follow-up questions without drifting into unnecessary detail.

This is primarily a behavior problem rather than a knowledge problem. The source information already exists in the transcript or project documents. The challenge is getting the model to transform that information into the same useful structure every time.

A prompting solution would start with a strict template, explicit extraction rules, and a few examples showing good and bad outputs. That would probably solve much of the problem. Its weakness is that prompt compliance can vary across long or messy transcripts, especially when decisions are implied rather than stated directly. Small wording changes in the input could also produce different levels of detail.

A RAG pipeline would help if the assistant needed organizational context, such as project terminology, team responsibilities, or prior decisions. Retrieval could provide that background before summarization. However, RAG would not directly solve the formatting and prioritization behavior. It improves what information is available to the model, not necessarily how consistently the model applies the requested structure.

My final choice would be prompting plus RAG before fine-tuning. I would first measure whether a strong prompt, examples, and retrieved organizational context can meet the required accuracy and consistency. Fine-tuning would only become justified if repeated evaluation showed a stable behavior gap that prompting could not correct. Distillation would make more sense later if the workflow were already reliable and the goal became reducing cost or latency by transferring the behavior to a smaller model.
