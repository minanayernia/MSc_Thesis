import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -------- 1) CONFIG --------
FILES = {
    "USA":  "results/llama3.1-70b/similarities_rolebased_vs_assistant/similarity_llama_rolebased_america_assistant.csv",
    "China":    "results/llama3.1-70b/similarities_rolebased_vs_assistant/similarity_llama_rolebased_china_assistant.csv",
    "France":   "results/llama3.1-70b/similarities_rolebased_vs_assistant/similarity_llama_rolebased_france_assistant.csv",
    "Germany":  "results/llama3.1-70b/similarities_rolebased_vs_assistant/similarity_llama_rolebased_germany_assistant.csv",
    "Iran":     "results/llama3.1-70b/similarities_rolebased_vs_assistant/similarity_llama_rolebased_iran_assistant.csv",
    "Israel":   "results/llama3.1-70b/similarities_rolebased_vs_assistant/similarity_llama_rolebased_israel_assistant.csv",
    "Italy":    "results/llama3.1-70b/similarities_rolebased_vs_assistant/similarity_llama_rolebased_italy_assistant.csv",
    "Russia":   "results/llama3.1-70b/similarities_rolebased_vs_assistant/similarity_llama_rolebased_russia_assistant.csv",
    "Ukraine":  "results/llama3.1-70b/similarities_rolebased_vs_assistant/similarity_llama_rolebased_ukraine_assistant.csv",
}

TOPICS_ORDER = [3, 4, 15, 17, 18, 22, 36, 40]
TOPIC_LABELS = {
    3:  "No nuclear weapons",
    4:  "Legalize sex selection",
    15: "No economic sanctions",
    17: "Legalize prostitution",
    18: "Multi-party system",
    22: "Adopt atheism",
    36: "Compulsory voting",
    40: "Adopt libertarianism",
}

# Output
OUTDIR = Path("results/llama3.1-70b/similarities_rolebased_vs_assistant/plots")
OUTDIR.mkdir(parents=True, exist_ok=True)
OUT_PNG = OUTDIR / "rolebased_vs_assistant_heatmap.png"
OUT_PDF = OUTDIR / "rolebased_vs_assistant_heatmap.pdf"

# Color scale (keep consistent across similar figures)
VMIN, VMAX = 0.3, 0.90   # adjust if your values are outside this band
CHART_TITLE = "Assistant vs Role — Mean Cosine Similarity by Topic (llama3.1-70b)"


# -------- 2) LOAD & PIVOT --------
rows = []
for country, path in FILES.items():
    df = pd.read_csv(path)
    # Expect columns: topic, mean_similarity, std_similarity, n_samples
    if not {"topic", "mean_similarity"}.issubset(df.columns):
        raise ValueError(f"{path} missing required columns.")
    for _, r in df.iterrows():
        rows.append({"country": country, "topic": int(r["topic"]), "mean": float(r["mean_similarity"])})

long_df = pd.DataFrame(rows)

# Limit to selected topics and pivot
long_df = long_df[long_df["topic"].isin(TOPICS_ORDER)]
pivot = long_df.pivot_table(index="country", columns="topic", values="mean", aggfunc="mean")

# Reindex rows/cols to desired order
countries_order = list(FILES.keys())
pivot = pivot.reindex(index=countries_order, columns=TOPICS_ORDER)

# -------- 3) HEATMAP (matplotlib) --------
fig, ax = plt.subplots(figsize=(10.5, 5.2))
im = ax.imshow(pivot.values, aspect="auto", vmin=VMIN, vmax=VMAX, cmap="Blues")
cbar = fig.colorbar(im, ax=ax)
cbar.set_label("Mean cosine similarity")

# y-axis: countries
ax.set_yticks(np.arange(len(pivot.index)))
ax.set_yticklabels(pivot.index)

# x-axis: topics (use short labels)
xlabels = [TOPIC_LABELS.get(t, str(t)) for t in pivot.columns]
ax.set_xticks(np.arange(len(pivot.columns)))
ax.set_xticklabels(xlabels, rotation=30, ha="right")

# chart title
ax.set_title(CHART_TITLE, pad=10)

fig.tight_layout()
fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
fig.savefig(OUT_PDF, bbox_inches="tight")
plt.close(fig)

print(f"Saved heatmap:\n- {OUT_PNG}\n- {OUT_PDF}")
