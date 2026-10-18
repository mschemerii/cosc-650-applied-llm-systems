# COSC 650: Applied LLM Systems

This repository contains my coursework, experiments, and capstone project for COSC 650: Applied LLM Systems at Maryville University.

## Capstone Project

### [Meeting-to-Action Assistant](week-08/)

The capstone integrates techniques from across the course into one measured system that converts an existing meeting transcript into a structured operational brief with:

- executive summary
- decisions
- action items and owners
- blockers
- follow-up questions

The system combines structured prompting, deterministic validation, MiniLM/FAISS retrieval, cross-encoder reranking, dynamic few-shot prompting, held-out evaluation, LLM-as-judge scoring, component-level failure analysis, and a measured comparison between Gemini and a small local Qwen model for narrow classification.

**Primary capstone artifacts**

- [Week 8 README and architecture](week-08/README.md)
- [Self-contained capstone notebook](week-08/week8_meeting_to_action_capstone.ipynb)
- [Capstone pull request](https://github.com/mschemerii/cosc-650-applied-llm-systems/pull/29)

The notebook is self-contained and includes the held-out set, retrieval/reranking pipeline, evaluation, judge pass, failure trace, mitigation, Gemini-vs-Qwen comparison, retry/backoff handling, caching, and the research note generated from the measured results at the end.

## Course Context

COSC 650 is an eight-week graduate course focused on the design and implementation of applied large language model systems. Topics include tokenization, transformer architecture, inference and sampling, prompt engineering, function calling, retrieval-augmented generation, adaptation decisions, evaluation, and integrated LLM-system design.

My goal is to understand what happens beneath LLM frameworks so I can design systems intentionally rather than simply connect libraries. In particular, I want to build and evaluate LLM applications that use tools, retrieval, structured outputs, and local models while understanding why each component works.

## Eight-Week Progression

| Week | Topic | Work |
| --- | --- | --- |
| [Week 1](week-01/) | Tokenization | Compared Spanish and English tokenization, examined Unicode normalization, and documented a token-count failure case and mitigation. |
| [Week 2](week-02/) | Inference and sampling | Examined how temperature, top-p, and top-k affect next-token selection and generated output. |
| [Week 3](week-03/) | Prompts as engineering artifacts | Versioned and evaluated support-ticket classification prompts over a 10-case test set using exact-match accuracy and semantic similarity. |
| [Week 4](week-04/) | Tool calling and structured function calling | Built a complete Gemini tool-calling loop with constrained JSON-schema tools, guarded arithmetic execution, structured failure handling, and recovery. |
| [Week 5](week-05/) | RAG and retrieval evaluation | Built an eight-document RAG pipeline with local MiniLM/MPNet embeddings, FAISS retrieval, ten labeled queries, chunk-level precision/recall, and grounded Gemini generation. |
| [Week 6](week-06/) | Query transformation and reranking | Extended the retriever with Gemini multi-query transformation, reciprocal-rank fusion, local cross-encoder reranking, and per-query evaluation. |
| [Week 7](week-07/) | Adaptation decision | Built a deterministic meeting-transcript classification dataset and compared zero-shot prompting with retrieval-selected dynamic few-shot adaptation. The measured run favored the simpler zero-shot approach. |
| [Week 8](week-08/) | Integrated LLM system | Built the self-contained Meeting-to-Action Assistant by reusing Weeks 3–7 components, with a 10-case A/B/C evaluation, Gemini-as-judge pass, required failure trace, targeted mitigation, Gemini-vs-local-Qwen comparison, and dynamically generated research note. |

## Capstone Reuse Map

The capstone intentionally reuses prior work:

- **Week 3:** structured prompting and output contracts
- **Week 4:** deterministic validation and explicit failure handling
- **Week 5:** MiniLM embeddings and FAISS retrieval
- **Week 6:** local cross-encoder reranking
- **Week 7:** dynamic few-shot selection and held-out evaluation discipline

This progression is the central story of the repository: each week adds one system-building capability, and Week 8 integrates them into one working application.

## Repository Organization

- `week-01/` through `week-08/` — weekly assignments, discussions, experiments, and notebooks
- `GEMINI.md` — agent context, project conventions, and AI-use documentation

## Technologies

- Python 3.11+
- Jupyter notebooks and Google Colab
- Google Gemini Flash
- Qwen local language model
- JSON-oriented structured outputs
- LLM tool/function calling
- retrieval-augmented generation
- sentence-transformers
- FAISS
- cross-encoder reranking
- deterministic evaluation and LLM-as-judge evaluation

## Workflow

Weekly work is developed on a dedicated branch and submitted through a pull request. Notebooks retain measured outputs, and conclusions are based on executed results rather than assumed performance.

For the capstone, the authoritative implementation is the self-contained Week 8 notebook. The pull request is the submission artifact for Canvas and the repository is curated as the portfolio view.

## Purpose

This repository serves as both a record of my progress through COSC 650 and a portfolio of practical work demonstrating how LLM-based systems are designed, implemented, tested, evaluated, simplified, and justified with evidence.
