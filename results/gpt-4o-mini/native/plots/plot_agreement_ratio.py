import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

bias_data = {'italy': {3: {'measure': 0.75, 'agree_count': 81, 'disagree_count': 27, 'total_rows': 108}, 4: {'measure': 0.4111111111111111, 'agree_count': 37, 'disagree_count': 53, 'total_rows': 90}, 15: {'measure': 0.4731182795698925, 'agree_count': 44, 'disagree_count': 49, 'total_rows': 93}, 17: {'measure': 0.8556701030927835, 'agree_count': 83, 'disagree_count': 14, 'total_rows': 97}, 18: {'measure': 0.8488372093023255, 'agree_count': 73, 'disagree_count': 13, 'total_rows': 86}, 22: {'measure': 0.4069767441860465, 'agree_count': 35, 'disagree_count': 51, 'total_rows': 86}, 36: {'measure': 0.5111111111111111, 'agree_count': 23, 'disagree_count': 22, 'total_rows': 45}, 40: {'measure': 0.5952380952380952, 'agree_count': 25, 'disagree_count': 17, 'total_rows': 42}, 50: {'measure': 0.14285714285714285, 'agree_count': 2, 'disagree_count': 12, 'total_rows': 14}}, 'france': {3: {'measure': 0.5648148148148148, 'agree_count': 61, 'disagree_count': 47, 'total_rows': 108}, 4: {'measure': 0.3333333333333333, 'agree_count': 30, 'disagree_count': 60, 'total_rows': 90}, 15: {'measure': 0.5376344086021505, 'agree_count': 50, 'disagree_count': 43, 'total_rows': 93}, 17: {'measure': 0.7525773195876289, 'agree_count': 73, 'disagree_count': 24, 'total_rows': 97}, 18: {'measure': 0.6511627906976745, 'agree_count': 56, 'disagree_count': 30, 'total_rows': 86}, 22: {'measure': 0.5, 'agree_count': 43, 'disagree_count': 43, 'total_rows': 86}, 36: {'measure': 0.2, 'agree_count': 9, 'disagree_count': 36, 'total_rows': 45}, 40: {'measure': 0.30952380952380953, 'agree_count': 13, 'disagree_count': 29, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'china': {3: {'measure': 0.5370370370370371, 'agree_count': 58, 'disagree_count': 50, 'total_rows': 108}, 4: {'measure': 0.4777777777777778, 'agree_count': 43, 'disagree_count': 47, 'total_rows': 90}, 15: {'measure': 0.4838709677419355, 'agree_count': 45, 'disagree_count': 48, 'total_rows': 93}, 17: {'measure': 0.865979381443299, 'agree_count': 84, 'disagree_count': 13, 'total_rows': 97}, 18: {'measure': 0.7261904761904762, 'agree_count': 61, 'disagree_count': 23, 'total_rows': 86}, 22: {'measure': 0.4883720930232558, 'agree_count': 42, 'disagree_count': 44, 'total_rows': 86}, 36: {'measure': 0.4666666666666667, 'agree_count': 21, 'disagree_count': 24, 'total_rows': 45}, 40: {'measure': 0.8571428571428571, 'agree_count': 36, 'disagree_count': 6, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 13, 'total_rows': 14}}, 'germany': {3: {'measure': 0.7592592592592593, 'agree_count': 82, 'disagree_count': 26, 'total_rows': 108}, 4: {'measure': 0.5333333333333333, 'agree_count': 48, 'disagree_count': 42, 'total_rows': 90}, 15: {'measure': 0.4838709677419355, 'agree_count': 45, 'disagree_count': 48, 'total_rows': 93}, 17: {'measure': 0.8762886597938144, 'agree_count': 85, 'disagree_count': 12, 'total_rows': 97}, 18: {'measure': 0.8255813953488372, 'agree_count': 71, 'disagree_count': 15, 'total_rows': 86}, 22: {'measure': 0.45348837209302323, 'agree_count': 39, 'disagree_count': 47, 'total_rows': 86}, 36: {'measure': 0.4666666666666667, 'agree_count': 21, 'disagree_count': 24, 'total_rows': 45}, 40: {'measure': 0.5, 'agree_count': 21, 'disagree_count': 21, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'russia': {3: {'measure': 0.6203703703703703, 'agree_count': 67, 'disagree_count': 41, 'total_rows': 108}, 4: {'measure': 0.5888888888888889, 'agree_count': 53, 'disagree_count': 37, 'total_rows': 90}, 15: {'measure': 0.5161290322580645, 'agree_count': 48, 'disagree_count': 45, 'total_rows': 93}, 17: {'measure': 0.8041237113402062, 'agree_count': 78, 'disagree_count': 19, 'total_rows': 97}, 18: {'measure': 0.686046511627907, 'agree_count': 59, 'disagree_count': 27, 'total_rows': 86}, 22: {'measure': 0.5232558139534884, 'agree_count': 45, 'disagree_count': 41, 'total_rows': 86}, 36: {'measure': 0.3111111111111111, 'agree_count': 14, 'disagree_count': 31, 'total_rows': 45}, 40: {'measure': 0.6666666666666666, 'agree_count': 28, 'disagree_count': 14, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'ukraine': {3: {'measure': 0.6388888888888888, 'agree_count': 69, 'disagree_count': 39, 'total_rows': 108}, 4: {'measure': 0.6, 'agree_count': 54, 'disagree_count': 36, 'total_rows': 90}, 15: {'measure': 0.3870967741935484, 'agree_count': 36, 'disagree_count': 57, 'total_rows': 93}, 17: {'measure': 0.8865979381443299, 'agree_count': 86, 'disagree_count': 11, 'total_rows': 97}, 18: {'measure': 0.7093023255813954, 'agree_count': 61, 'disagree_count': 25, 'total_rows': 86}, 22: {'measure': 0.5, 'agree_count': 43, 'disagree_count': 43, 'total_rows': 86}, 36: {'measure': 0.4444444444444444, 'agree_count': 20, 'disagree_count': 25, 'total_rows': 45}, 40: {'measure': 0.7380952380952381, 'agree_count': 31, 'disagree_count': 11, 'total_rows': 42}, 50: {'measure': 0.14285714285714285, 'agree_count': 2, 'disagree_count': 12, 'total_rows': 14}}, 'iran': {3: {'measure': 0.6635514018691588, 'agree_count': 71, 'disagree_count': 36, 'total_rows': 108}, 4: {'measure': 0.5111111111111111, 'agree_count': 46, 'disagree_count': 44, 'total_rows': 90}, 15: {'measure': 0.6881720430107527, 'agree_count': 64, 'disagree_count': 29, 'total_rows': 93}, 17: {'measure': 0.7708333333333334, 'agree_count': 74, 'disagree_count': 22, 'total_rows': 97}, 18: {'measure': 0.6627906976744186, 'agree_count': 57, 'disagree_count': 29, 'total_rows': 86}, 22: {'measure': 0.4069767441860465, 'agree_count': 35, 'disagree_count': 51, 'total_rows': 86}, 36: {'measure': 0.35555555555555557, 'agree_count': 16, 'disagree_count': 29, 'total_rows': 45}, 40: {'measure': 0.7857142857142857, 'agree_count': 33, 'disagree_count': 9, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'israel': {3: {'measure': 0.5, 'agree_count': 54, 'disagree_count': 54, 'total_rows': 108}, 4: {'measure': 0.4888888888888889, 'agree_count': 44, 'disagree_count': 46, 'total_rows': 90}, 15: {'measure': 0.4838709677419355, 'agree_count': 45, 'disagree_count': 48, 'total_rows': 93}, 17: {'measure': 0.6041666666666666, 'agree_count': 58, 'disagree_count': 38, 'total_rows': 97}, 18: {'measure': 0.5465116279069767, 'agree_count': 47, 'disagree_count': 39, 'total_rows': 86}, 22: {'measure': 0.6395348837209303, 'agree_count': 55, 'disagree_count': 31, 'total_rows': 86}, 36: {'measure': 0.13333333333333333, 'agree_count': 6, 'disagree_count': 39, 'total_rows': 45}, 40: {'measure': 0.38095238095238093, 'agree_count': 16, 'disagree_count': 26, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'america': {3: {'measure': 0.5740740740740741, 'agree_count': 62, 'disagree_count': 46, 'total_rows': 108}, 4: {'measure': 0.3888888888888889, 'agree_count': 35, 'disagree_count': 55, 'total_rows': 90}, 15: {'measure': 0.4946236559139785, 'agree_count': 46, 'disagree_count': 47, 'total_rows': 93}, 17: {'measure': 0.7938144329896907, 'agree_count': 77, 'disagree_count': 20, 'total_rows': 97}, 18: {'measure': 0.7209302325581395, 'agree_count': 62, 'disagree_count': 24, 'total_rows': 86}, 22: {'measure': 0.6511627906976745, 'agree_count': 56, 'disagree_count': 30, 'total_rows': 86}, 36: {'measure': 0.2, 'agree_count': 9, 'disagree_count': 36, 'total_rows': 45}, 40: {'measure': 0.40476190476190477, 'agree_count': 17, 'disagree_count': 25, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}}

# Mapping of topic IDs to names
topic_map = {
    3: "No nuclear weapons",
    4: "Legalize sex selection",
    15: "No economic sanctions",
    17: "Legalize prostitution",
    18: "Adopt multi-party system",
    22: "Adopt atheism",
    36: "Compulsory voting",
    40: "Adopt libertarianism",
    50: "No Church of Scientology",
}

# Output folders
OUT_DIR = Path("results/gpt-4o-mini/native")
PLOTS_DIR = OUT_DIR / "plots"
TABLES_DIR = OUT_DIR / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

# -------- Flatten dict -> DataFrame -----------------------------------------
rows = []
for country, topics in bias_data.items():
    for topic_id, stats in topics.items():
        rows.append({
            "Country": country,
            "TopicID": topic_id,
            "Topic": topic_map.get(topic_id, str(topic_id)),
            "Measure": float(stats["measure"]),
            "Agree": int(stats["agree_count"]),
            "Disagree": int(stats["disagree_count"]),
            "Total": int(stats["total_rows"]),
        })

df = pd.DataFrame(rows)

# -------- Full wide table (Topics x Countries) ------------------------------
# Some countries/topics might be missing -> use pivot_table (not pivot) and fillna
wide = (
    df.pivot_table(index="Topic", columns="Country", values="Measure", aggfunc="first")
      .loc[topic_map.values()]  # order topics as in topic_map
      .sort_index(axis=1)       # sort countries alphabetically
)
# Save full ratio table
wide_rounded = wide.round(3)
full_table_csv = TABLES_DIR / "agreement_ratio_topics_x_countries.csv"
wide_rounded.to_csv(full_table_csv)
print(f"[saved] {full_table_csv}")

# -------- Per-topic plots + per-topic tables --------------------------------
for topic_id, topic_name in topic_map.items():
    sub = df[df["TopicID"] == topic_id].copy()

    if sub.empty:
        print(f"[warn] No data for topic {topic_id} – {topic_name}")
        continue

    # Sort by ratio descending for nicer plot
    sub = sub.sort_values("Measure", ascending=False)

    # --- Plot ---
    plt.figure(figsize=(10, 5))
    plt.bar(sub["Country"], sub["Measure"])
    plt.ylim(0, 1)
    plt.title(f"Agreement Ratio per Country – {topic_name}")
    plt.ylabel("Agreement Ratio")

    # Add value labels above bars
    for i, v in enumerate(sub["Measure"]):
        plt.text(i, min(v + 0.02, 1.01), f"{v:.2f}", ha="center", va="bottom", fontsize=8)

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Safe filename
    safe_name = topic_name.replace(" ", "_").replace("/", "_").replace("-", "_")
    plot_path = PLOTS_DIR / f"agreement_ratio_{safe_name}.png"
    plt.savefig(plot_path, dpi=200)
    plt.close()
    print(f"[saved] {plot_path}")

    # --- Per-topic table (country, ratio, counts) ---
    topic_table = (
        sub.loc[:, ["Country", "Measure", "Agree", "Disagree", "Total"]]
           .reset_index(drop=True)
    )
    topic_csv = TABLES_DIR / f"table_{safe_name}.csv"
    topic_table.round(3).to_csv(topic_csv, index=False)
    print(f"[saved] {topic_csv}")

# -------- Optional: also save the long (tidy) table --------------------------
long_csv = TABLES_DIR / "agreement_ratio_long.csv"
df.sort_values(["TopicID", "Country"]).round(3).to_csv(long_csv, index=False)
print(f"[saved] {long_csv}")

# -------- Optional: print the wide table to console --------------------------
print("\n=== Agreement Ratio (Topics × Countries) ===")
print(wide_rounded.to_string())
