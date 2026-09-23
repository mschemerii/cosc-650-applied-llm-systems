# Week 4 — Tool Calling: From Model to Agent

This week builds a complete function-calling loop with constrained tool schemas, tool execution, returned tool results, recovery from failure, and a guarded code-execution tool.

## Files

- `week4_tool_calling_agent.ipynb` — main assignment notebook
- GitHub issue #15 — documented runtime failure and recovery case

## Assignment mapping

### Part 1 — Build the assistant

The notebook defines three tools with constrained JSON schemas:

1. `lookup_course_reference`
   - Required fields: `topic`, `detail`
   - Enums constrain both fields to supported values.
   - Used for a small deterministic local reference lookup.

2. `convert_length`
   - Required fields: `value`, `from_unit`, `to_unit`
   - `value` is numeric.
   - Unit fields use enums so unsupported units cannot be requested through the schema.

3. `run_guarded_python`
   - Required fields: `task`, `code`
   - `task` is restricted to the `arithmetic` enum.
   - `code` is a string containing one arithmetic expression.

All schemas set `additionalProperties: false`.

The notebook implements the complete loop: send tools to the model, intercept tool calls, execute locally, append structured tool results, and call the model again until it returns a final answer.

### Part 2 — Guarded code runner

The code runner uses an AST allowlist before execution.

**Permitted**
- Numeric constants
- Parentheses
- `+`, `-`, `*`, `/`, `//`, `%`, `**`
- Unary `+` and `-`

**Blocked**
- Filesystem access
- Network access
- Imports
- Function and method calls
- Variable/name access
- Attribute access
- Indexing/subscripts
- Loops, assignments, comprehensions, and control flow
- Model-supplied process execution

The validated expression executes in a separate worker process with empty built-ins. The parent process terminates the worker if the execution exceeds the configured time limit.

This is a focused instructional guardrail, not a production sandbox.

### Part 3 — Evaluation

The notebook includes four live evaluation queries:

1. Course-reference lookup
2. Length conversion
3. Guarded arithmetic execution
4. Two-tool sequence: guarded arithmetic followed by length conversion

The agent records a tool-call log for every run containing:
- selected tool,
- arguments,
- success/failure status,
- structured result.

The saved executed notebook should contain the actual Gemini outputs.

### Part 4 — Failure and recovery

The notebook intentionally requests:

```json
{
  "task": "arithmetic",
  "code": "10 / 0"
}
```

The call is valid according to the JSON schema and AST guardrail but fails at runtime with `ZeroDivisionError`. The tool catches the exception and returns a structured error to the model. The model is then given the opportunity to retry with `10 / 2`.

This is a **retry after structured runtime error**. The case is also documented in [GitHub issue #15](https://github.com/mschemerii/cosc-650-applied-llm-systems/issues/15).

## Model and environment

The notebook uses Gemini Flash through Google's OpenAI-compatible endpoint with the OpenAI Python client.

The API key is loaded from the `GEMINI_API_KEY` environment variable and must not be committed to GitHub.

The notebook includes:
- short exponential backoff for failed model requests,
- an in-memory response cache to avoid unnecessary repeated calls during one session,
- no GPU requirement.

## Running the notebook

1. Open the notebook in Jupyter or Google Colab.
2. Set `GEMINI_API_KEY` in the environment.
3. Run the notebook from top to bottom.
4. Verify the tool-call logs show the expected tools and arguments.
5. Verify the failure experiment records the initial error and successful retry.
6. Save the executed notebook with outputs before submission.
7. Export the executed notebook to PDF or HTML for Canvas.

## Submission checklist

- [ ] Notebook executes from top to bottom.
- [ ] Three constrained tools are present.
- [ ] All tool schemas use required fields, explicit types, and enums where appropriate.
- [ ] Full function-calling loop is demonstrated.
- [ ] Guardrail permissions and blocked categories are stated plainly.
- [ ] Code execution is validated before running and time-limited.
- [ ] At least three evaluation queries are shown.
- [ ] Every tool is exercised.
- [ ] At least one query uses two tools in sequence.
- [ ] Tool-call logs show tool, arguments, and success/failure.
- [ ] Real failure and recovery are documented.
- [ ] GitHub issue #15 contains the failure/recovery write-up.
- [ ] `GEMINI.md` documents AI assistance.
- [ ] Same executed notebook is committed to GitHub and exported for Canvas.
- [ ] Pull request description explains schema choices and links the notebook and issue.
