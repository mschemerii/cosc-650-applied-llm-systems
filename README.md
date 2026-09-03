# COSC 650: Applied LLM Systems

This repository contains my coursework, experiments, and projects for COSC 650: Applied LLM Systems at Maryville University.

## Course Context

COSC 650 is an eight-week graduate course focused on the design and implementation of applied large language model systems. Topics include tokenization, transformer architecture, inference and sampling, prompt engineering, function calling, retrieval-augmented generation, fine-tuning, and evaluation.

My goal is to understand what happens beneath LLM frameworks so I can design systems intentionally rather than simply connect libraries. In particular, I want to build and evaluate LLM applications that use tools, retrieval, structured outputs, and local models while understanding why each component works.

## Weekly Work

| Week | Topic | Work |
| --- | --- | --- |
| [Week 1](week-01/) | Tokenization | Compared Spanish and English tokenization, examined Unicode normalization, and documented a token-count failure case and mitigation. |
| [Week 2](week-02/) | Inference and sampling | Examined how temperature, top-p, and top-k affect next-token selection and generated output. The Week 2 assignment and discussion are separate deliverables. |
| Weeks 3–8 | Upcoming topics | Additional weekly notebooks and experiments will be added as the course progresses. |

## Repository Organization

- `week-01/` through `week-08/` — weekly assignments, experiments, and notebooks
- `notes/` — research notes and reading annotations
- `project/` — final project code and documentation
- `CLAUDE.md` and `GEMINI.md` — project context and conventions for AI coding assistants

## Technologies

Technologies used throughout the course may include:

- Python 3.11+
- Jupyter notebooks and Google Colab
- Hugging Face Transformers
- Google Gen AI SDK
- tiktoken
- OpenAI SDK
- Anthropic SDK
- Local large language models
- Retrieval-augmented generation
- LLM tool and function calling
- Structured outputs
- Model and application evaluation

## Workflow

Weekly work is developed on a dedicated branch and submitted through a pull request with a written results summary. Notebooks retain their measured outputs, and supporting research is documented through linked GitHub issues when required.

## Purpose

This repository serves as both a record of my progress through COSC 650 and a portfolio of practical work demonstrating how LLM-based systems are designed, implemented, tested, and evaluated.
