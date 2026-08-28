# Week 1: Tokenization Analysis

This week's assignment examines how tokenization differs between equivalent English and Spanish text using `tiktoken`.

## Assignment Files

- `week1_tokenization_starter.ipynb` — executable Jupyter notebook containing the analysis and saved tokenizer results
- `week1_tokenization_starter.html` — HTML export submitted to Canvas

## Key Results

Using the same English and Spanish passages:

- `cl100k_base`: 143 English tokens vs. 197 Spanish tokens — 1.38x multilingual token cost
- `o200k_base`: 143 English tokens vs. 160 Spanish tokens — 1.12x multilingual token cost

The analysis also examines English/Spanish word fragmentation, context-window and cost implications, and a Unicode normalization case where visually identical text produces different token counts.
