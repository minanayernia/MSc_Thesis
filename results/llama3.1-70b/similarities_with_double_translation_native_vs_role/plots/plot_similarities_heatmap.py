import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -------- 1) CONFIG --------
FILES = {
    "USA":  "results/llama3.1-70b/similarities_with_double_translation_native_vs_role/similarity_avgENIT_llama_America_native_vs_role.csv",
    "China":    "results/llama3.1-70b/similarities_with_double_translation_native_vs_role/similarity_avgENIT_llama_China_native_vs_role.csv",
    "France":   "results/llama3.1-70b/similarities_with_double_translation_native_vs_role/similarity_avgENIT_llama_France_native_vs_role.csv",
    "Germany":  "results/llama3.1-70b/similarities_with_double_translation_native_vs_role/similarity_avgENIT_llama_Germany_native_vs_role.csv",
    "Iran":     "results/llama3.1-70b/similarities_with_double_translation_native_vs_role/similarity_avgENIT_llama_Iran_native_vs_role.csv",
    "Israel":   "results/llama3.1-70b/similarities_with_double_translation_native_vs_role/similarity_avgENIT_llama_Israel_native_vs_role.csv",
    "Italy":    "results/llama3.1-70b/similarities_with_double_translation_native_vs_role/similarity_avgENIT_llama_Italy_native_vs_role.csv",
    "Russia":   "results/llama3.1-70b/similarities_with_double_translation_native_vs_role/similarity_avgENIT_llama_Russia_native_vs_role.csv",
    "Ukraine":  "results/llama3.1-70b/similarities_with_double_translation_native_vs_role/similarity_avgENIT_llama_Ukraine_native_vs_role.csv",
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
OUTDIR = Path("results/llama3.1-70b/similarities_with_double_translation_native_vs_role/plots")
OUTDIR.mkdir(parents=True, exist_ok=True)
OUT_PNG = OUTDIR / "native_vs_role_heatmap.png"
OUT_PDF = OUTDIR / "native_vs_role_heatmap.pdf"

VMIN, VMAX = 0.3, 0.90

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
plt.figure(figsize=(10.5, 5.2))
im = plt.imshow(pivot.values, aspect="auto", vmin=VMIN, vmax=VMAX, cmap="Blues")
cbar = plt.colorbar(im)
cbar.set_label("Mean cosine similarity")

# y-axis: countries
plt.yticks(np.arange(len(pivot.index)), pivot.index)

# x-axis: topics (use short labels)
xlabels = [TOPIC_LABELS.get(t, str(t)) for t in pivot.columns]
plt.xticks(np.arange(len(pivot.columns)), xlabels, rotation=30, ha="right")

plt.tight_layout()
plt.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
plt.savefig(OUT_PDF, bbox_inches="tight")
plt.close()

print(f"Saved heatmap:\n- {OUT_PNG}\n- {OUT_PDF}")
