# COSC 650 Capstone — Meeting-to-Action Assistant

## Project Overview

The capstone project is a **Meeting-to-Action Assistant** that takes a meeting transcript and converts it into a structured operational brief. The goal is to build one small, measurable system that combines techniques from earlier COSC 650 assignments into a realistic end-to-end workflow.

The system will identify and organize the parts of a meeting that are most useful after the call is over:

- executive summary
- decisions made
- action items
- owners
- blockers
- follow-up questions

The project is intentionally focused. It is not intended to become a general-purpose meeting platform, autonomous agent, transcription service, or enterprise workflow system. The capstone will concentrate on the quality of extracting operational information from already available transcript text.

## Problem

Meeting transcripts are usually much longer than the information someone needs to act on. Decisions may be stated indirectly, action items may be spread across multiple speakers, owners may be implied rather than named in the same sentence, and suggestions can easily be mistaken for confirmed decisions.

The project will test whether a small retrieval-and-reasoning pipeline can turn that noisy transcript into a reliable operational brief while preserving enough evidence to evaluate where the system succeeds or fails.

A central failure case will be distinguishing a **confirmed decision** from a suggestion, possibility, or discussion point.

## Project Goal

The goal is to determine the smallest architecture that produces useful and defensible meeting briefs.

The system will reuse proven components from earlier course work instead of rebuilding every capability from scratch. Deterministic code and local models will be used where they are sufficient. Gemini will be reserved for tasks where stronger language reasoning provides a measurable advantage.

The final model and pipeline choices will be based on evaluation results rather than assumptions about which model should perform best.

## Planned Pipeline

```text
Meeting transcript
       |
       v
Transcript preparation / chunking
       |
       v
Semantic retrieval
       |
       v
Cross-encoder reranking
       |
       v
Relevant transcript context and optional examples
       |
       v
Gemini structured extraction and synthesis
       |
       v
Deterministic schema validation
       |
       v
Structured operational brief
       |
       v
Evaluation and failure analysis
```

## Techniques Integrated

The capstone will integrate techniques already explored in the course.

### 1. Retrieval-Augmented Generation

Local sentence-transformer embeddings and FAISS retrieval will select transcript passages or labeled examples relevant to decisions, action items, blockers, owners, and follow-up questions.

The retrieval implementation will build on the Week 5 RAG work.

### 2. Reranking

A local cross-encoder reranker will reorder retrieved candidates before they are supplied to the generation step.

This component will build on the Week 6 retrieval and reranking work.

### 3. Structured Prompting and Output

Gemini will be prompted to return a fixed structured representation of the meeting brief rather than unconstrained prose.

Expected fields will include:

```text
executive_summary
decisions[]
action_items[]
    description
    owner
blockers[]
follow_up_questions[]
```

The structured prompting approach will build on the Week 3 prompt-engineering work.

### 4. Deterministic Validation

Python validation will verify required fields, data types, and output structure. Invalid model output will be recorded as a measurable failure rather than silently accepted.

This approach will reuse the schema and validation principles from Week 4.

### 5. Dynamic Few-Shot Prompting

The system will experimentally retrieve labeled examples that are semantically similar to the current transcript content and provide them as demonstrations to Gemini.

Dynamic few-shot prompting will be treated as an experimental component, not an assumed improvement. Week 7 results showed that retrieved examples can sometimes introduce label bias, so the capstone will measure whether they help or hurt this task.

## Models

### Gemini

Gemini will be the primary model for reasoning-heavy extraction and synthesis tasks, including:

- determining whether a statement represents a confirmed decision
- identifying action items expressed indirectly
- resolving owners across multiple speakers
- interpreting blockers and unresolved questions
- combining information from multiple transcript passages
- generating the executive summary
- producing the final structured meeting brief

### Small Local Model

A small local instruct model, initially **Qwen3.5-0.8B** or a similarly sized model, will be evaluated against Gemini.

The local model will first be tested on narrower tasks such as classifying transcript spans as:

- `decision`
- `action_item`
- `blocker`
- `follow_up_question`
- `context`

It may also be tested on complete brief generation to establish where performance begins to break down.

The purpose of this comparison is not to force the local model into the final architecture. The goal is to determine whether it is good enough to replace Gemini for any narrow portion of the workflow.

### Retrieval Models

Generative models will not be used for basic retrieval when deterministic local models are sufficient.

The project will reuse:

- a sentence-transformer embedding model such as `all-MiniLM-L6-v2`
- FAISS for similarity search
- a local cross-encoder for reranking

## Evaluation

A held-out evaluation set of approximately **10–20 meeting transcript examples** will be created and kept separate from examples used for prompt development or few-shot retrieval.

The evaluation will measure:

- decision precision
- decision recall
- action-item precision
- action-item recall
- owner accuracy
- structured-output validity rate
- latency
- Gemini API cost
- local inference cost
- model-based correctness and grounding scores

Where practical, deterministic metrics will be preferred over model judgment.

## Ablation Study

The project will compare at least these three configurations:

1. **Transcript only**
2. **Transcript + retrieved context**
3. **Transcript + retrieved context + retrieved few-shot examples**

This will show whether retrieval and dynamic examples materially improve the final result rather than simply increasing system complexity.

Additional comparisons may include Gemini versus the local model, but only if they can be performed without expanding the project beyond the capstone scope.

## Failure Analysis

At least one observed failure will be traced back to the component most likely responsible for it.

The primary expected failure case is:

> A suggestion or discussion point is incorrectly reported as a confirmed decision.

The failure will be investigated using evidence such as:

- retrieved passages
- reranker scores
- selected few-shot examples
- prompt configuration
- model output
- ablation results

The objective is not merely to report that the model was wrong, but to identify which part of the pipeline contributed to the error.

## Exact Project Scope

The capstone will include:

- input from an existing text meeting transcript
- transcript chunking or passage preparation
- local semantic retrieval
- local reranking
- optional dynamic few-shot example selection
- Gemini structured extraction and synthesis
- deterministic output validation
- a small local-model comparison
- a held-out evaluation set
- quantitative metrics
- at least one ablation study
- at least one documented failure analysis
- an executable notebook or small Python implementation
- repository documentation and an executed submission artifact

## Explicitly Out of Scope

To keep the project small enough to finish and evaluate properly, the following are **not** part of the capstone unless a course requirement later makes them necessary:

- audio transcription or speech-to-text
- live meeting capture
- Zoom or Microsoft Teams integration
- calendar integration
- email sending
- automatic task creation
- autonomous multi-agent workflows
- vector databases or hosted retrieval infrastructure
- fine-tuning a model
- training a custom embedding model
- production authentication or user accounts
- graphical web application development
- cloud deployment
- long-term conversational memory
- automatic execution of extracted action items

The final system stops after producing and evaluating the structured operational brief.

## Success Criteria

The project will be considered successful if it demonstrates that:

1. a transcript can be converted into the required structured operational brief;
2. the output can be evaluated with repeatable metrics;
3. retrieval, reranking, and prompting choices can be compared experimentally;
4. at least one failure can be traced to a specific component using evidence;
5. the local model can be fairly compared with Gemini on an appropriate subset of the task; and
6. the final architecture uses the simplest component that performs well enough for each part of the workflow.

The capstone prioritizes **integration, measurement, and evidence** over adding features. A small system that works consistently and can explain its failures is the intended final result.
