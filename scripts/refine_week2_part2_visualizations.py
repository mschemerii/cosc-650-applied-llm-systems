import json
from pathlib import Path

path = Path("week-02/week2_sampling_experiment.ipynb")
notebook = json.loads(path.read_text())

cell = next(
    c for c in notebook["cells"]
    if c.get("id") == "part2-direct-comparison-plots"
)

code = '''def plot_before_after(base_probabilities, filtered_probabilities, title, n):
    order = np.argsort(base_probabilities)[::-1][:n]
    x = np.arange(1, len(order) + 1)
    width = 0.42

    plt.figure(figsize=(14, 5))
    plt.bar(x - width / 2, base_probabilities[order], width, label="Base distribution")
    plt.bar(x + width / 2, filtered_probabilities[order], width, label="After filtering")
    plt.ylabel("Probability")
    plt.xlabel("Token rank in the base distribution")
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
top_p_survivors = surviving_tokens(top_p_only)
print("Top-p only surviving tokens:", top_p_survivors)
plot_before_after(
    base,
    top_p_only,
    "Top-p = 0.90: base distribution vs filtered distribution",
    n=top_p_survivors + 20,
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

# Combination 2: top-k sets a ceiling of 20 candidates, then top-p can cut further.
# This directly visualizes the interaction examined in the failure analysis.
combo_visual_2 = apply_sampling(z, temperature=1.0, top_k=20, top_p=0.90)
combo_2_survivors = surviving_tokens(combo_visual_2)
print("Combination 2 surviving tokens:", combo_2_survivors)
plot_before_after(
    base,
    combo_visual_2,
    "Combination: top-k = 20, top-p = 0.90",
    n=30,
)
'''

cell["source"] = [line + "\n" for line in code.splitlines()]
cell["execution_count"] = None
cell["outputs"] = []

path.write_text(json.dumps(notebook, indent=2, ensure_ascii=False) + "\n")
print("Refined Part 2 visual comparison cell.")
