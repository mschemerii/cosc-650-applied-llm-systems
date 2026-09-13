# Week 3 Research Note

## Task

Support-ticket classification into four categories: billing, technical, account, and shipping.

## Prompt Versions

- `support_ticket_v1.txt`: baseline structured prompt with system instructions, three few-shot examples, required JSON output, and brief-rationale guidance.
- `support_ticket_v2.txt`: adds a primary-intent rule for ambiguous tickets.

## Hypothesis

The primary-intent rule is expected to improve ambiguous support-ticket classification by directing the model to focus on the customer's main problem instead of reacting to secondary details or individual keywords. This should reduce cases where a ticket is placed in the wrong category simply because it mentions a charge, account action, or technical symptom that is not the customer's primary reason for contacting support.

## Evaluation Method

The notebook evaluates 10 input/expected-output pairs with Gemini `gemini-3.5-flash-lite` using the version-controlled prompt files in `week-03/prompts/`.

Each response is evaluated with:

- Exact match on the predicted category.
- Semantic similarity between the expected rationale and generated rationale using `sentence-transformers` locally with `sentence-transformers/all-MiniLM-L6-v2`.

The notebook also compares all 10 cases side by side using the expected category, v1 and v2 predicted categories, v1 and v2 exact-match results, v1 and v2 semantic-similarity scores, and the semantic-score change between prompt versions.

## Results

The live Gemini run produced the following aggregate results:

- **Prompt v1:** 90% exact-match accuracy; mean semantic similarity **0.519**.
- **Prompt v2:** 90% exact-match accuracy; mean semantic similarity **0.511**.
- **Exact-match change:** 0 percentage points.
- **Mean semantic-similarity change:** **-0.008**.

The prompt edit therefore did not change overall classification accuracy. Nine of the ten cases were classified correctly by both prompt versions.

Test case #3 remained incorrect in both versions. The ticket was `I want to change my email but the save button does nothing.` The expected category was `account`, while both v1 and v2 returned `technical`. Its semantic similarity also decreased from **0.172** under v1 to **0.114** under v2, a change of **-0.058**.

## Improved Case

The strongest measured semantic improvement was test case #5: `Love the new dashboard, great work.`

- Expected category: `account`
- v1 predicted category: `account`
- v2 predicted category: `account`
- v1 exact match: 1
- v2 exact match: 1
- v1 semantic similarity: **0.291**
- v2 semantic similarity: **0.433**
- Semantic change: **+0.142**

The category classification did not change, but the v2 rationale was more semantically similar to the expected rationale according to the evaluation metric.

## Regression / Failure Case

There was **no exact-match category regression** between v1 and v2. The live run produced the same category result for every test case under both prompt versions.

The strongest semantic regression was test case #4: `Tracking has not updated in four days.`

- Expected category: `shipping`
- v1 predicted category: `shipping`
- v2 predicted category: `shipping`
- v1 exact match: 1
- v2 exact match: 1
- v1 semantic similarity: **0.540**
- v2 semantic similarity: **0.364**
- Semantic change: **-0.176**

The classification remained correct, but the v2 rationale was less semantically similar to the expected rationale according to the evaluation metric.

## Tradeoff Analysis

The v2 edit preserved exact-match accuracy at **90%**, so the additional primary-intent instructions did not improve or damage the structured category output on this 10-case test suite. However, the rationale metric moved in both directions across individual cases. Test #5 improved by **+0.142**, while test #4 regressed by **-0.176**, and the overall mean semantic score declined from **0.519** to **0.511**.

These measurements show that a prompt change can leave the primary structured output unchanged while still changing the model's explanatory wording enough to affect a semantic evaluation metric. The experiment does not establish a causal explanation for the wording changes, so the measured result is limited to observing that the v2 instructions preserved category accuracy but produced uneven changes in rationale similarity.

The persistent error on test #3 is also important. The added v2 rule did not resolve the ambiguity between the requested account action (changing an email address) and the malfunctioning interface (the save button not working). Both prompt versions selected `technical` when the expected category was `account`.

## Proposed Resolution

A next prompt revision could make the category-precedence rule more explicit for mixed-intent tickets and add a few-shot example that directly covers an account action blocked by a technical symptom. The goal would be to clarify whether the requested user outcome or the immediate malfunction should determine the category.

A second useful refinement would be to add an example for a straightforward shipping-status ticket such as test #4. This could test whether more explicit rationale guidance improves semantic consistency without changing the already-correct shipping classification.

These are proposed follow-up changes only; they were not evaluated in the current experiment.

## AI Tool Use

ChatGPT was used to help scaffold and review the versioned prompt files, notebook structure, Colab/Gemini execution setup, comparison table, and this research-note organization. The reported measurements in this document come from the saved live Gemini notebook run. The final interpretation is limited to those observed measurements, and proposed prompt refinements are identified separately from the measured results.
