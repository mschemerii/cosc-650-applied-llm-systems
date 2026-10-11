# Week 7 — Adaptation Decision and Production Dataset

COSC 650 - Applied LLM Systems

## Assignment

- `week7_adaptation_decision.ipynb` — dataset quality checks, local retrieval-selected few-shot adaptation, Gemini Flash-Lite evaluation, failure-slice analysis, and adaptation decision memo.
- `week7_train.csv` — 200 synthetic training examples, balanced across five intent labels.
- `week7_eval.csv` — 50 held-out evaluation examples, balanced across the same five labels.
- `week7_eval_cache.json` — cache populated by the notebook so completed Gemini calls are not repeated.

The measured comparison uses a deterministic 25-example balanced subset to stay within free-tier API limits. Run the notebook with `GEMINI_API_KEY`, save all outputs, fill the measured-result placeholders in the decision memo, and export the executed notebook to HTML for Canvas.

## Discussion

- [Week 7 Discussion — Fine-Tuning Decision Framework](discussion-finetuning-decision.md)
