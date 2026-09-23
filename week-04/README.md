# Week 4: Tool Schemas and Structured Function Calling

COSC 650 - Applied LLM Systems

## Overview

Week 4 covers both schema design and the complete model-to-tool execution loop. The work for this week includes a discussion experiment comparing loose and constrained schemas, plus the main assignment notebook that implements an agent loop with three tools, guarded code execution, structured error handling, and recovery.

## Main Assignment

The main assignment notebook is `week4_tool_calling_agent.ipynb`.

It implements three tools:

1. `lookup_course_reference`
   - Required fields: `topic` and `detail`
   - Uses enums to restrict both fields to supported values
   - Uses `additionalProperties: false`

2. `convert_length`
   - Required fields: `value`, `from_unit`, and `to_unit`
   - Uses an explicit numeric type for `value`
   - Uses enums for supported units
   - Uses `additionalProperties: false`

3. `run_guarded_python`
   - Required fields: `task` and `code`
   - Restricts `task` to the `arithmetic` enum
   - Accepts one arithmetic expression as a string
   - Uses `additionalProperties: false`

The notebook implements the complete function-calling loop: the model receives the tool schemas, selects a tool, sends arguments, receives the structured result, and continues until it produces a final answer.

## Guarded Code Runner

The code runner validates model-suggested arithmetic with an AST allowlist before execution.

Permitted operations include numeric constants, parentheses, arithmetic operators, and unary plus/minus.

Blocked categories include:

- filesystem access
- network access
- imports
- function and method calls
- variable/name access
- attribute access
- indexing/subscripts
- loops, assignments, comprehensions, and other control flow
- model-supplied process execution

The validated expression executes in a separate worker process with empty built-ins and a time limit. This is a focused classroom guardrail, not a production sandbox.

## Evaluation Results

The executed notebook contains four evaluation queries:

- course-reference lookup
- length conversion
- guarded arithmetic
- a two-tool sequence that calculates `144 * 3` and then converts the result from centimeters to meters

The saved tool-call logs show the tool selected, arguments sent, success/failure status, and returned result.

The measured two-tool sequence successfully called:

1. `run_guarded_python` → `432`
2. `convert_length` → `4.32 meters`

## Failure and Recovery

The notebook intentionally calls:

```json
{
  "task": "arithmetic",
  "code": "10 / 0"
}
```

The call is schema-valid and passes the arithmetic allowlist, but fails at runtime with `ZeroDivisionError`. The tool returns that error as structured data rather than crashing the agent loop. The model then retries with `10 / 2` and receives the successful result `5.0`.

This failure and recovery are documented in [GitHub issue #15](https://github.com/mschemerii/cosc-650-applied-llm-systems/issues/15).

## Discussion Experiment

The separate Week 4 discussion experiment compares loose and constrained JSON Schemas for a support-ticket search tool. It demonstrates that schema constraints reduce invalid tool arguments but cannot eliminate semantic ambiguity in natural-language intent.

## Files

- [`week4_tool_calling_agent.ipynb`](week4_tool_calling_agent.ipynb) - executed main Week 4 assignment notebook
- [`week4_tool_calling_agent.html`](week4_tool_calling_agent.html) - HTML export for Canvas submission
- [`week4_schema_design_discussion.ipynb`](week4_schema_design_discussion.ipynb) - discussion experiment notebook
- [`discussion-schema-design.md`](discussion-schema-design.md) - full discussion post
- [`discussion-schema-design-canvas.txt`](discussion-schema-design-canvas.txt) - Canvas-ready discussion text

## Running the Assignment Notebook

1. Add `GEMINI_API_KEY` to Colab Secrets or set it as an environment variable.
2. Run `week4_tool_calling_agent.ipynb` from top to bottom.
3. Verify that the saved tool-call logs show all three tools.
4. Verify that the two-tool query uses both tools in sequence.
5. Verify that the failure case records the initial `ZeroDivisionError` and successful retry.
6. Export the executed notebook to HTML or PDF for Canvas.

## Main Takeaway

Tight schemas limit the model's action space, while the agent loop allows the model to use tool results as new context and decide what to do next. Structured errors are just as important as successful results because they allow the system to recover from failures without crashing.
