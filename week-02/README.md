# Week 2: Inference and Sampling

Week 2 examines how a language model converts logits into next-token probabilities and how sampling parameters change the candidates available for generation.

## Deliverables

The Week 2 assignment and discussion are separate course deliverables:

- **Assignment — Inference and Sampling:** trace a DistilGPT2 forward pass, implement temperature, top-k, and top-p sampling, visualize how they reshape the probability distribution, compare predictions with measurements, and document one failure case with its cause and mitigation.
- **Discussion — Where Did That Output Come From?:** run the same prompt through the same model with three sampling configurations, preserve the exact outputs, and compare their style, length, accuracy, and usefulness.

The current notebook in this directory supports the discussion experiment. It should not be treated as the completed main assignment notebook.

## Discussion Experiment

The notebook uses `gemini-3.1-flash-lite` through the Google Gen AI SDK. It asks the model to explain next-token generation to a non-technical audience in no more than 100 words.

The same prompt is used for all three runs:

1. Temperature `0.0`
2. Temperature `0.7` with top-p `0.9`
3. Temperature `1.2` with top-k `50`

This design exercises all three sampling controls required by the Canvas discussion instructions. Parameters that are not named in a run remain at Gemini's defaults.

## Recorded Results

| Configuration | Length | Observation |
| --- | ---: | --- |
| Temperature `0.0` | 94 words | Most direct and least variable configuration |
| Temperature `0.7`, top-p `0.9` | 93 words | Smoothest and most natural explanation |
| Temperature `1.2`, top-k `50` | 92 words | Slightly less precise because it describes generation as “word-by-word” |

All three outputs stayed within the 100-word limit and remained broadly accurate. Temperature `0.7` with top-p `0.9` was the strongest fit for the explanatory task.

## Interpretation

The observed differences arise during next-token sampling after the model produces logits:

- **Temperature** reshapes the probability distribution. Higher values flatten it and give lower-probability tokens more influence; lower values concentrate probability on the strongest candidates.
- **Top-k** retains only a fixed number of the highest-probability candidates.
- **Top-p** retains the smallest candidate set whose cumulative probability reaches the selected threshold.

The third run changes both temperature and top-k. Its wording difference therefore cannot be attributed to either parameter independently: the higher temperature increased randomness while top-k restricted selection to the 50 highest-probability candidates. Temperature `0` is described as the most deterministic setting, but a hosted API does not guarantee identical output across every request.

## Files

- [`week2_sampling_experiment.ipynb`](week2_sampling_experiment.ipynb) — executable discussion experiment, recorded outputs, word counts, and analysis
- [`README.md`](README.md) — Week 2 scope, experiment summary, results, and interpretation

## Running the Notebook

1. Open the notebook in Google Colab or a compatible Jupyter environment.
2. Install `google-genai` if it is not already available.
3. Store the API key as `GEMINI_API_KEY`; do not place it directly in the notebook.
4. Run the notebook from top to bottom.
5. Preserve the generated outputs before using them in the discussion comparison.

Because sampling can produce different wording on later calls, rerunning the stochastic cells may not reproduce the recorded responses exactly.
