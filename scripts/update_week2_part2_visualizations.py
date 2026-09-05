import json
from pathlib import Path

path = Path("week-02/week2_sampling_experiment.ipynb")
notebook = json.loads(path.read_text())
marker = "### 2E. Direct before-and-after filter comparisons"

if any(marker in "".join(cell.get("source", [])) for cell in notebook["cells"]):
    print("Visualization cells already present; no insertion needed.")
    raise SystemExit(0)

insert_at = next(
    i
    for i, cell in enumerate(notebook["cells"])
    if cell.get("cell_type") == "markdown"
    and "".join(cell.get("source", [])).lstrip().startswith("## Part 3")
)

markdown_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "id": "part2-direct-comparisons",
    "source": [
        "### 2E. Direct before-and-after filter comparisons\n",
        "\n",
        "The plots below compare each filtered distribution directly with the same base next-token distribution. Using the base-token ranking on the x-axis makes the truncation boundary visible: top-k imposes a fixed ceiling on the number of candidates, while top-p keeps only the smallest ranked prefix whose cumulative probability reaches the threshold. The two final plots show how the controls interact when combined in the inference order used above.\n",
    ],
}

code = '''def plot_before_after(base_probabilities, filtered_probabilities, title, n):
    order = np.argsort(base_probabilities)[::-1][:n]
    labels = [
        tokenizer.decode([int(i)]).replace("\\n", "\\\\n")
        for i in order
    ]
    x = np.arange(len(order))
    width = 0.42

    plt.figure(figsize=(14, 5))
    plt.bar(x - width / 2, base_probabilities[order], width, label="Base distribution")
    plt.bar(x + width / 2, filtered_probabilities[order], width, label="After filtering")
    plt.xticks(x, labels, rotation=70, ha="right")
    plt.ylabel("Probability")
    plt.xlabel("Tokens ranked by base probability")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()


# Top-k by itself: the first 20 candidates survive and the rest are zeroed.
top_k_only = apply_sampling(z, temperature=1.0, top_k=20, top_p=1.0)
print("Top-k only surviving tokens:", surviving_tokens(top_k_only))
plot_before_after(
    base,
    top_k_only,
    "Top-k = 20: base distribution vs filtered distribution",
    n=40,
)

# Top-p by itself: the cutoff is determined by cumulative probability, not a fixed count.
top_p_only = apply_sampling(z, temperature=1.0, top_k=None, top_p=0.90)
top_p_n = min(120, max(40, surviving_tokens(top_p_only) + 10))
print("Top-p only surviving tokens:", surviving_tokens(top_p_only))
plot_before_after(
    base,
    top_p_only,
    "Top-p = 0.90: base distribution vs filtered distribution",
    n=top_p_n,
)

# Combination 1: lower temperature sharpens first, then top-k truncates.
combo_visual_1 = apply_sampling(z, temperature=0.7, top_k=40, top_p=1.0)
print("Combination 1 surviving tokens:", surviving_tokens(combo_visual_1))
plot_before_after(
    base,
    combo_visual_1,
    "Combination: temperature = 0.7, top-k = 40",
    n=50,
)

# Combination 2: higher temperature flattens first; top-k sets a ceiling,
# then top-p can reduce the candidate set further.
combo_visual_2 = apply_sampling(z, temperature=1.2, top_k=100, top_p=0.90)
combo_2_n = min(120, max(70, surviving_tokens(combo_visual_2) + 10))
print("Combination 2 surviving tokens:", surviving_tokens(combo_visual_2))
plot_before_after(
    base,
    combo_visual_2,
    "Combination: temperature = 1.2, top-k = 100, top-p = 0.90",
    n=combo_2_n,
)
'''

code_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "id": "part2-direct-comparison-plots",
    "outputs": [],
    "source": [line + "\n" for line in code.splitlines()],
}

notebook["cells"][insert_at:insert_at] = [markdown_cell, code_cell]
path.write_text(json.dumps(notebook, indent=2, ensure_ascii=False) + "\n")
print("Inserted Part 2 comparison cells before Part 3.")
