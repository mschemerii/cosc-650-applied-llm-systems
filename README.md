# COSC 650: Applied LLM Systems

This repository contains my coursework, experiments, and capstone project for COSC 650: Applied LLM Systems at Maryville University.

## Capstone Project

### [Meeting-to-Action Assistant](week-08/)

The capstone integrates earlier course techniques into one measured system that converts an existing meeting transcript into a structured operational brief with an executive summary, decisions, action items and owners, blockers, and follow-up questions.

The system combines structured prompting, deterministic validation, MiniLM/FAISS retrieval, cross-encoder reranking, dynamic few-shot prompting, held-out evaluation, LLM-as-judge scoring, and component-level failure analysis.

Key capstone artifacts:

- [Week 8 README and architecture](week-08/README.md)
- [Self-contained capstone notebook](week-08/week8_meeting_to_action_capstone.ipynb) — includes the dynamically generated research note at the end

## Course Context

COSC 650 is an eight-week graduate course focused on the design and implementation of applied large language model systems. Topics include tokenization, transformer architecture, inference and sampling, prompt engineering, function calling, retrieval-augmented generation, adaptation decisions, evaluation, and integrated LLM-system design.

My goal is to understand what happens beneath LLM frameworks so I can design systems intentionally rather than simply connect libraries. In particular, I want to build and evaluate LLM applications that use tools, retrieval, structured outputs, and local models while understanding why each component works.

## Weekly Work

| Week | Topic | Work |
| --- | --- | --- |
| [Week 1](week-01/) | Tokenization | Compared Spanish and English tokenization, examined Unicode normalization, and documented a token-count failure case and mitigation. |
| [Week 2](week-02/) | Inference and sampling | Examined how temperature, top-p, and top-k affect next-token selection and generated output. The Week 2 assignment and discussion are separate deliverables. |
| [Week 3](week-03/) | Prompts as engineering artifacts | Versioned and evaluated support-ticket classification prompts over a 10-case test set using exact-match accuracy and semantic similarity. |
| [Week 4](week-04/) | Tool calling and structured function calling | Built a complete Gemini tool-calling loop with three constrained JSON-schema tools, guarded arithmetic code execution, multi-tool sequencing, structured failure handling, and successful recovery. A separate discussion experiment compares loose and tight tool schemas. |
| [Week 5](week-05/) | RAG and retrieval evaluation | Built an eight-document RAG pipeline with local MiniLM/MPNet embeddings, FAISS retrieval, ten labeled queries, chunk-level precision/recall, and grounded Gemini generation. A separate discussion compares three chunking strategies. |
| [Week 6](week-06/) | Query transformation and re-ranking | Extended the Week 5 retriever with Gemini Flash-Lite multi-query transformation, reciprocal-rank fusion, transformation-only evaluation, and a local cross-encoder reranker. The executed run showed transformation-only MRR 0.850 versus baseline 0.900, while reranking improved final MRR to 1.000. |
| [Week 7](week-07/) | Adaptation decision and production dataset | Built a deterministic 250-example training set and 50-example held-out meeting-transcript classification set, then compared Gemini Flash-Lite zero-shot classification with local MiniLM retrieval-selected dynamic few-shot adaptation. The executed run scored **100.0% zero-shot vs. 96.0% dynamic few-shot**; `action_item` was the clearest underperforming slice at **100.0% vs. 80.0%**, supporting the simpler prompt-based approach. |
| [Week 8](week-08/) | Integrated LLM system | Built the self-contained Meeting-to-Action Assistant capstone by reusing Weeks 3–7 components, with a 10-case held-out evaluation, A/B/C ablation, LLM-as-judge pass, required failure trace, targeted mitigation, and a research note generated from the measured results at the end of the notebook. Week 8 also includes the external-dependency threat model. |

## Repository Organization

- `week-01/` through `week-08/` — weekly assignments, experiments, discussions, and notebooks
- `GEMINI.md` — project context and conventions for AI coding assistants

## Technologies

- Python 3.11+
- Jupyter notebooks and Google Colab
- Google Gemini
- JSON Schema and structured outputs
- LLM tool/function calling
- Retrieval-augmented generation
- sentence-transformers and FAISS
- Cross-encoder reranking
- Local language models through llama.cpp
- Model and application evaluation

## Workflow

Weekly work is developed on a dedicated branch and submitted through a pull request with a written results summary. Notebooks retain their measured outputs, and supporting research or failure analysis is documented when required.

## Purpose

This repository serves as both a record of my progress through COSC 650 and a portfolio of practical work demonstrating how LLM-based systems are designed, implemented, tested, evaluated, and simplified based on evidence.
