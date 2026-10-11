# Week 7 — Adaptation Decision and Production Dataset

COSC 650 - Applied LLM Systems

## Assignment

The Week 7 assignment is centered on `week7_adaptation_decision.ipynb`. The notebook builds a deterministic synthetic meeting-transcript classification dataset with **250 training examples** and **50 held-out evaluation examples** across five labels: `decision`, `action_item`, `blocker`, `follow_up_question`, and `context`.

The notebook performs:

- dataset validation, duplicate checks, train/evaluation leakage checks, label balance, and token-length statistics;
- local MiniLM retrieval of the four most relevant training examples for each evaluation input;
- Gemini Flash-Lite zero-shot and dynamic few-shot evaluation;
- an in-memory response cache with rate-limit handling;
- a predeclared five-example contrastive challenge slice designed to test retrieval-induced label bias;
- a balanced 25-example primary evaluation, with automatic expansion to all 50 held-out examples only if the primary run shows no few-shot regression;
- measured failure-slice analysis;
- a final-results section and decision memo generated from the current run; and
- the required research note inside the notebook.

The notebook reads `GEMINI_API_KEY` from **Google Colab Secrets**. It does not use `.env`, Google Drive, or a JSON cache file.

## Executed results

The current executed notebook produced:

- **Zero-shot accuracy:** 100.0%
- **Dynamic few-shot accuracy:** 96.0%
- **Absolute change:** -4.0%
- **Clearest underperforming slice:** `action_item`
  - zero-shot: 100.0%
  - dynamic few-shot: 80.0%
  - change: -20.0%
- **Final decision:** keep the simpler constrained prompt rather than use dynamic few-shot for this task.

The observed regression supports the notebook's main adaptation decision: adding retrieval-selected demonstrations can introduce negative transfer when semantically similar examples bias the model toward a competing label.

## Repository artifacts

- `week7_adaptation_decision.ipynb` — executed assignment notebook
- `week7_adaptation_decision.html` — HTML export of the executed notebook for submission/reference
- `data/week7_train_part1.csv` — first 125 training examples
- `data/week7_train_part2.csv` — remaining 125 training examples
- `data/week7_eval.csv` — 50 held-out evaluation examples, including the five-example contrastive challenge slice
- `discussion-finetuning-decision.md` — Week 7 discussion deliverable

The CSV files are repository artifacts for the dataset requirement. The notebook is self-contained and regenerates the same dataset internally, so Canvas execution does not depend on external CSV files.

## Submission

For Canvas, submit the executed notebook and its HTML export:

- `week7_adaptation_decision.ipynb`
- `week7_adaptation_decision.html`

## Discussion

- [Week 7 Discussion — Fine-Tuning Decision Framework](discussion-finetuning-decision.md)
