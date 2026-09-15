# Week 3: Prompts as Engineering Artifacts

COSC 650 - Applied LLM Systems

## Overview

This week focuses on treating prompts as versioned engineering artifacts that can be tested, measured, and revised with evidence rather than judged from a single successful example.

The assignment uses a support-ticket classification task with four categories:

- `billing`
- `technical`
- `account`
- `shipping`

Each model response returns a structured JSON object containing the predicted category and a brief rationale.

## Prompt Versions

Two prompt versions are stored in `week-03/prompts/`:

- `support_ticket_v1.txt` - baseline prompt with a system message, category definitions, three few-shot examples, structured JSON output, and brief-rationale guidance.
- `support_ticket_v2.txt` - revised prompt that adds a primary-intent rule for ambiguous tickets.

## Evaluation

The notebook evaluates both prompt versions over 10 input/expected-output pairs using two metrics:

1. Exact match on the predicted support-ticket category.
2. Semantic similarity between the expected rationale and generated rationale using `sentence-transformers` with `all-MiniLM-L6-v2`.

Live prompt runs use Gemini through its OpenAI-compatible endpoint. The saved experiment run used `gemini-3.5-flash-lite`.

## Measured Results

| Prompt | Exact Match | Mean Semantic Similarity |
| --- | ---: | ---: |
| v1 | 90% | 0.519 |
| v2 | 90% | 0.511 |

The prompt revision did not change overall category accuracy. Both versions classified 9 of 10 cases correctly.

The per-case comparison showed measurable rationale changes even though the exact-match results stayed the same:

- Strongest semantic improvement: case #5, `0.291 -> 0.433` (`+0.142`).
- Strongest semantic regression: case #4, `0.540 -> 0.364` (`-0.176`).
- Persistent classification failure: case #3 was expected to be `account`, but both versions returned `technical`.

These results show that the prompt edit preserved structured classification accuracy while changing the semantic alignment of the generated rationales in both positive and negative directions.

## Files

- `week3_prompt_engineering.ipynb` - executable experiment, live Gemini evaluation, metrics, and 10-case comparison table.
- `prompts/support_ticket_v1.txt` - baseline prompt.
- `prompts/support_ticket_v2.txt` - revised prompt.
- `research-note.md` - experiment hypothesis, measured results, tradeoff analysis, and proposed refinement.

## Reproducing the Experiment

The notebook is designed to run in Google Colab or from a local checkout.

In Colab, add a secret named `GEMINI_API_KEY`, open the notebook from the repository, and run the cells from top to bottom. The notebook reads the versioned prompt files from the repository, calls Gemini for live classifications, and evaluates the responses with exact-match and local semantic-similarity metrics.
