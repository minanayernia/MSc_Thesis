import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --- CONFIG ---
INPUT_DIR = Path("topic_modeling_results/stance_summaries")
OUTPUT_DIR = Path("topic_modeling_results/plots")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- 1. ARGUMENT DISTRIBUTION OVER TOPICS ---
df_topic = pd.read_csv(INPUT_DIR / "stance_by_topic_counts.csv")

plt.figure(figsize=(10, 6))
for stance in df_topic["Stance"].unique():
    subset = df_topic[df_topic["Stance"] == stance]
    plt.bar(
        subset["Topic"].astype(str),
        subset["Count"],
        label=stance,
        bottom=df_topic[
            (df_topic["Stance"] < stance) & (df_topic["Topic"].isin(subset["Topic"]))
        ].groupby("Topic")["Count"].sum().reindex(subset["Topic"], fill_value=0).values
    )

plt.title("Distribution of arguments across topics")
plt.xlabel("Topic ID")
plt.ylabel("Number of arguments")
plt.legend(title="Stance")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "arguments_by_topic.png", dpi=300)
plt.close()


# --- 2. ARGUMENT DISTRIBUTION OVER CONCLUSIONS ---
df_conc = pd.read_csv(INPUT_DIR / "stance_by_topic_conclusion_counts_long.csv")

# Sort conclusions by total size (largest first)
conclusion_order = (
    df_conc.groupby("Conclusion")["Count"].sum().sort_values(ascending=False).index
)
df_conc["Conclusion"] = pd.Categorical(
    df_conc["Conclusion"], categories=conclusion_order, ordered=True
)

plt.figure(figsize=(12, 8))
for stance in df_conc["Stance"].unique():
    subset = df_conc[df_conc["Stance"] == stance]
    plt.barh(
        subset["Conclusion"],
        subset["Count"],
        label=stance,
        left=df_conc[
            (df_conc["Stance"] < stance)
            & (df_conc["Conclusion"].isin(subset["Conclusion"]))
        ].groupby("Conclusion")["Count"].sum().reindex(subset["Conclusion"], fill_value=0).values
    )

plt.title("Distribution of arguments across conclusions (stacked by stance)")
plt.xlabel("Number of arguments")
plt.ylabel("Conclusion")
plt.legend(title="Stance")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "arguments_by_conclusion.png", dpi=300)
plt.close()

print("Plots saved to:", OUTPUT_DIR)
