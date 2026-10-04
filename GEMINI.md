# GEMINI.md

## Project

Course repository for COSC 650: Applied LLM Systems (Maryville University).

This is an 8-week graduate course covering tokenization, transformer architecture, prompt engineering, function calling, retrieval-augmented generation, fine-tuning, and evaluation.

## Structure

- `week-01/` through `week-08/`: weekly assignments and notebooks
- `notes/`: research notes and reading annotations
- `project/`: final project code and documentation
- `README.md`: human-facing project description
- `GEMINI.md`: Gemini project context and conventions

## Conventions

- Coursework is organized by week.
- Notebooks and Python code are developed locally and committed to GitHub.
- All code is Python 3.11+ unless an assignment specifies otherwise.
- Use the libraries required by the assignment before introducing alternatives.
- For Week 1 tokenization experiments, use `tiktoken` with the instructor-provided `cl100k_base` and `o200k_base` encodings.
- Commits use descriptive messages, not generic messages such as `update` or `fix`.
- Course requirements and assignment rubrics take priority over optional improvements.
- Keep implementations focused on the current assignment.
- Explain important implementation decisions and underlying LLM concepts rather than only producing finished code.

## Do Not

- Delete files or directories without confirming first.
- Push directly to `main` without checking what is staged.
- Commit API keys, credentials, secrets, or `.env` files.
- Add Gemini API calls or other model APIs unless the assignment actually requires them.
- Change completed coursework unless specifically requested.
- Add unnecessary frameworks or dependencies outside the assignment scope.
- Invent assignment requirements that are not present in the course materials.

## Learning Goal

The goal is to understand how LLM-system components work, not only how to connect frameworks. Prefer direct implementations when they make the underlying behavior easier to understand.

## AI Assistance

### Week 1

- ChatGPT was used to debug the Week 1 notebook and grammatically check/improve documentation.
- The tokenizer experiments were executed locally by me using `tiktoken`.
- The reported token counts are the saved results of those runs.

### Week 2

- ChatGPT was used to debug the Week 2 notebook and grammatically check/improve documentation.
- The `distilgpt2` forward-pass and sampling experiments were executed by me, and the reported numerical measurements and outputs come from those runs.

### Week 3

- ChatGPT was used to debug the Week 3 notebook and Colab/Gemini workflow and grammatically check/improve documentation.
- The live Gemini experiment was executed by me using the saved notebook. The reported exact-match and semantic-similarity measurements are the results of that run.

### Week 4

- ChatGPT was used to debug the Week 4 notebook and grammatically check/improve documentation.
- The code runner uses an AST allowlist that permits numeric arithmetic only and blocks filesystem, network, imports, function calls, attribute/name access, subscripting, control flow, and model-supplied process execution before execution.
- The live Gemini calls, selected tools, generated arguments, tool outputs, failure behavior, recovery behavior, and final measured observations come from running the notebook.
- Final interpretation of the executed results and any changes made after observing the live run are the student's own analysis and decisions.

### Week 5 RAG assignment

- ChatGPT was used to debug the Week 5 notebook and Gemini free-tier workflow, preserve the evaluation structure, and grammatically check/improve documentation.
- The student ran local embedding and retrieval and Gemini with their own API key. The saved notebook reports MiniLM and MPNet mean recall@3 of 1.00 and mean precision@3 of 0.333; MPNet ranked the gold chunk first on 10/10 questions and MiniLM on 8/10. These values and the Q05 failure case came from the student's execution.
- The student remains responsible for checking the relevance labels, interpretations, grounded answers, and final submission.

### Week 6 query transformation and re-ranking assignment

- ChatGPT was used to debug the Week 6 notebook, preserve the Week 5 evaluation set, and grammatically check/improve documentation.
- The notebook uses `gemini-3.5-flash-lite` to generate two query rewrites in one request per test query and caches responses in `week6_query_cache.json` so successful calls are not repeated.
- MiniLM is used as the Week 6 baseline because the saved Week 5 run ranked the gold chunk first on 8/10 queries; the Week 5 MPNet result was already 10/10 and would create a ceiling for ranking improvement.
- Week 6 measurements, query rewrites, transformed rankings, re-ranked results, per-query deltas, failure/no-regression result, and final interpretation come from the student's executed notebook.
