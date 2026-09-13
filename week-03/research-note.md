# Week 3 Research Note

## Task

Support-ticket classification into four categories: billing, technical, account, and shipping.

## Prompt Versions

- `support_ticket_v1.txt`: baseline structured prompt with system instructions, three few-shot examples, required JSON output, and brief-rationale guidance.
- `support_ticket_v2.txt`: adds a primary-intent rule for ambiguous tickets.

## Hypothesis

The primary-intent rule is expected to improve ambiguous support-ticket classification by directing the model to focus on the customer's main problem instead of reacting to secondary details or individual keywords. This should reduce cases where a ticket is placed in the wrong category simply because it mentions a charge, account action, or technical symptom that is not the customer's primary reason for contacting support.

## Evaluation Method

The test suite contains at least 10 input/expected-output pairs. Each response is evaluated with:

- Exact match on the predicted category.
- Semantic similarity between the expected rationale and generated rationale using `sentence-transformers` locally.

## Results

TODO: Add the measured v1 and v2 exact-match and semantic-similarity results after running the notebook with Gemini.

## Improved Case

TODO: Identify one test case that improved from v1 to v2 and include metric values for both versions.

## Regression / Failure Case

TODO: Identify one test case that regressed from v1 to v2 and include metric values for both versions. If there is no regression in the live run, document that result and the measured change instead.

## Tradeoff Analysis

TODO: Explain why the v2 edit helped one input and hurt another, or why no regression occurred.

## Proposed Resolution

TODO: Describe how the prompt could be refined to resolve the tradeoff without simply reversing the change.

## AI Tool Use

ChatGPT was used to help scaffold and review the versioned prompt files and assignment structure. The experiment execution, measurements, interpretation, and final conclusions will be based on the student's own run and analysis.
