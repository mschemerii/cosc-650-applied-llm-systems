# Week 7 Discussion: The Adaptation Decision

My first instinct would be to fine-tune a local LLM to turn meeting transcripts into short executive briefs. In this hypothetical workflow, the model keeps treating suggestions as commitments and assigning action items to people who never accepted them. I want it to distinguish decisions, proposed ideas, confirmed assignments, and unresolved questions while preserving the speaker’s meaning.

This is mainly a behavior problem. The transcript already contains the relevant information; the model needs to handle evidence and uncertainty more consistently. Company terminology could introduce a separate knowledge problem, but learning more terminology would not necessarily fix invented commitments.

A prompting solution would specify the output structure, require supporting transcript excerpts for each action, and instruct the model to mark missing owners or dates as unknown. I would include examples contrasting “we could investigate this” with “I will investigate this by Friday.” Its likely weakness is handling indirect language, interruptions, and conflicting statements across a long meeting. Still, I would test that limitation rather than assume prompting cannot work.

A RAG solution could retrieve a company glossary, project descriptions, and relevant transcript passages. That would help interpret unfamiliar terms and keep supporting evidence available. However, retrieving an older project plan could also encourage the model to confuse previous responsibilities with assignments made in the current meeting. RAG alone would not establish whether someone actually committed to an action.

My final choice would be prompting with structured extraction, evidence checks, and human review before considering training. I would evaluate unseen transcripts for unsupported actions, incorrect owners, missed commitments, and correct handling of uncertainty. Distillation could become useful if a stronger local teacher reliably produces verified examples for a smaller model, but it could also transfer the teacher’s mistakes. Distillation can itself involve fine-tuning; it describes where the training signal comes from.

I would reconsider supervised fine-tuning only if the tested prompting baseline repeatedly fails and a carefully labeled dataset improves those behaviors on held-out meetings.
