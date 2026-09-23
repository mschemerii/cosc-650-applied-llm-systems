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

- ChatGPT was used to develop the Spanish/English test passages and explore the Unicode normalization failure case when typos caused frustration.
- The tokenizer experiments were executed locally by me using `tiktoken`.
- The reported token counts are the saved results of those runs.

### Week 2

- ChatGPT was used to review the assignment requirements, help interpret the sampling experiment, and improve explanations of temperature, top-k, top-p, probability-distribution changes, and the observed failure/surprise case.
- ChatGPT was also used to review the completed notebook for rubric compliance and help update the Week 2 README.
- The `distilgpt2` forward-pass and sampling experiments were executed by me, and the reported numerical measurements and outputs come from those runs.

### Week 3

- ChatGPT was used to scaffold and review the versioned prompt files, test-suite structure, evaluation code, and supporting documentation for the prompt-engineering assignment.
- ChatGPT was used to help debug the Colab/Gemini API workflow, rate-limit handling, repository prompt-file loading, and the final comparison-table presentation.
- ChatGPT was used to review the measured results and help organize the README and research note around the observed exact-match and semantic-similarity results.
- The live Gemini experiment was executed by me using the saved notebook. The reported exact-match and semantic-similarity measurements are the results of that run; no regression or improvement was fabricated beyond the measured outputs.


### Week 4

- ChatGPT was used to scaffold the Week 4 notebook structure, constrained tool schemas, the end-to-end function-calling loop, guarded arithmetic code-runner design, evaluation queries, and supporting README documentation.
- ChatGPT was also used to create the GitHub issue documenting the planned runtime failure and recovery case.
- The code runner was designed with an AST allowlist that permits numeric arithmetic only and blocks filesystem, network, imports, function calls, attribute/name access, subscripting, control flow, and model-supplied process execution before execution.
- The live Gemini calls, selected tools, generated arguments, tool outputs, failure behavior, recovery behavior, and final measured observations must come from running the notebook. These results are not fabricated by ChatGPT.
- Final interpretation of the executed results and any changes made after observing the live run are the student's own analysis and decisions.
