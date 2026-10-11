# Week 7 — Adaptation Decision and Production Dataset

COSC 650 - Applied LLM Systems

## Assignment

The Week 7 assignment is centered on `week7_adaptation_decision.ipynb`. The notebook builds a deterministic synthetic meeting-transcript classification dataset with **250 training examples** and **50 held-out evaluation examples** across five labels: `decision`, `action_item`, `blocker`, `follow_up_question`, and `context`.

The notebook performs:

- dataset validation, deduplication, leakage checks, label balance, and token-length statistics;
- local MiniLM retrieval of the four most relevant training examples for each evaluation input;
- Gemini Flash-Lite zero-shot and dynamic few-shot evaluation;
- an in-memory response cache with rate-limit handling;
- a predeclared contrastive challenge slice designed to test retrieval-induced label bias;
- automatic expansion from the 25-example primary run to all 50 held-out examples if no few-shot regression appears initially;
- a measured final-results section and decision memo populated from the current run; and
- the required research note inside the notebook.

The notebook reads `GEMINI_API_KEY` from **Google Colab Secrets**. It does not use `.env`, Google Drive, or a JSON cache file.

For Canvas, run **Runtime → Run all**, save the executed notebook, and export that executed notebook to HTML.

## Repository artifacts

- `week7_adaptation_decision.ipynb` — assignment notebook
- `week7_dataset.py` — deterministic dataset source used to reproduce the 250/50 dataset outside the notebook
- `discussion-finetuning-decision.md` — Week 7 discussion deliverable

## Discussion

- [Week 7 Discussion — Fine-Tuning Decision Framework](discussion-finetuning-decision.md)
