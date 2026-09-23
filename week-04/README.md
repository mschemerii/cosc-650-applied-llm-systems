# Week 4: Tool Schemas and Structured Function Calling

COSC 650 - Applied LLM Systems

## Overview

Week 4 focuses on how JSON Schema constraints affect LLM tool calls. The discussion experiment compares a deliberately loose schema with a tighter schema for a support-ticket search tool and documents what the model gets wrong in each case.

The experiment is designed to show the difference between syntactic validity and semantic correctness. A model can produce a structurally valid tool call while still choosing an interpretation that does not fully match the user's intent.

## Discussion Experiment

The tool used in the experiment is `search_support_tickets`. The prompt asks the model to find the 10 highest-priority open AI-related tickets from the last 30 days for the Facilities team.

The loose schema allows unrestricted strings and numbers. This permits the model to invent values such as:

- `currently_open`
- `highest`
- `artificial intelligence`

The tightened schema adds:

- enums for allowed categorical values
- required fields
- integer-only numeric fields
- minimum and maximum numeric bounds
- `additionalProperties: false`

The tighter schema produces a structurally valid tool call, but it still exposes a semantic ambiguity: “highest-priority” may mean sorting all matching tickets by priority rather than filtering only for `critical` tickets.

## Files

- `discussion-schema-design.md` - full Week 4 discussion post with the loose schema, tight schema, model outputs, and analysis.
- `discussion-schema-design-canvas.txt` - plain-text version formatted for direct copy and paste into a Canvas discussion thread.
- `week4_schema_design_discussion.ipynb` - executable notebook that runs the loose and tight schema tests and validates the returned arguments with JSON Schema.

## Running the Notebook

The notebook is designed for Google Colab or a local Python environment.

For live model calls:

1. Add `GEMINI_API_KEY` to Colab Secrets or set it as an environment variable.
2. Run the notebook from top to bottom.
3. Compare the live outputs with the captured discussion examples.
4. If the model returns different arguments, update the discussion post with the actual observed outputs before submitting.

The notebook also includes local schema-validation edge cases to demonstrate how the tighter schema rejects invalid enum values, negative ranges, fractional limits, and unexpected properties.

## Main Takeaway

Schema constraints are effective at narrowing the space of invalid tool calls, but they do not eliminate ambiguity in natural-language intent. The most useful constraints enforce application rules while leaving genuinely ambiguous choices explicit rather than encoding them indirectly.
