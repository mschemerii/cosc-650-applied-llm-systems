# Week 2: Inference and Sampling

Week 2 contains two separate course deliverables: the main inference-and-sampling assignment and the sampling discussion experiment.

## Files

- [`week2_sampling_experiment.ipynb`](week2_sampling_experiment.ipynb) — **main Week 2 assignment**. Uses local Hugging Face `distilgpt2` on CPU to trace the forward pass, inspect token IDs, embeddings, attention weights, logits, and next-token probabilities, then implements and evaluates temperature, top-k, and top-p sampling.
- [`week2_sampling_discussion.ipynb`](week2_sampling_discussion.ipynb) — **Week 2 discussion experiment**. Uses `gemini-3.1-flash-lite` with three sampling configurations and preserves the generated outputs for comparison.
- [`README.md`](README.md) — Week 2 file guide and scope.

## Main Assignment — Inference and Sampling

The main assignment notebook:

1. Loads `distilgpt2` locally with eager attention enabled.
2. Traces a prompt through tokenization, embeddings, attention, and vocabulary logits.
3. Implements temperature scaling, top-k filtering, and top-p filtering directly.
4. Visualizes how each control reshapes the next-token probability distribution, including combined settings.
5. Compares predictions with measured entropy, maximum probability, and surviving-token counts.
6. Demonstrates a failure/surprise case where `top-p = 1.0` leaves the full vocabulary available and explains the mitigation.

The numerical measurements in this notebook come from the locally executed model.

## Discussion — Where Did That Output Come From?

The discussion notebook uses the same prompt with three Gemini sampling configurations:

1. Temperature `0.0`
2. Temperature `0.7` with top-p `0.9`
3. Temperature `1.2` with top-k `50`

The saved outputs are compared for style, length, accuracy, and usefulness.

## Repository Organization

Week 2 coursework belongs directly under `week-02/`. Branch names such as `week-02/inference-sampling` are Git references only and should not appear as nested repository directories.
