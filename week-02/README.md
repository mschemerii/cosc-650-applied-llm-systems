# Week 2: Inference and Sampling

Week 2 focuses on tracing a local language model forward pass and examining how sampling controls reshape the next-token probability distribution.

## Files

- [`week2_sampling_experiment.ipynb`](week2_sampling_experiment.ipynb) — **Week 2 assignment notebook**. Uses local Hugging Face `distilgpt2` on CPU to trace token IDs, embeddings, attention weights, logits, and next-token probabilities, then implements and evaluates temperature, top-k, and top-p sampling.
- [`README.md`](README.md) — Week 2 assignment guide and scope.

## Assignment — Inference and Sampling

The assignment notebook:

1. Loads `distilgpt2` locally with eager attention enabled.
2. Traces a prompt through tokenization, embeddings, attention, and vocabulary logits.
3. Implements temperature scaling, top-k filtering, and top-p filtering directly.
4. Visualizes how each control reshapes the next-token probability distribution, including combined settings.
5. Compares predictions with measured entropy, maximum probability, and surviving-token counts.
6. Demonstrates a failure/surprise case where `top-p = 1.0` leaves the full vocabulary available and explains the mitigation.

The numerical measurements in the notebook come from the locally executed model.

## Repository Organization

Week 2 coursework belongs directly under `week-02/`. Branch names such as `week-02/inference-sampling` are Git references only and should not appear as nested repository directories.
