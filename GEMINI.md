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
- `CLAUDE.md`: Claude-specific project context retained for cross-tool compatibility

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
