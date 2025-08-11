import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

bias_data = {'italy': {3: {'measure': 0.8679245283018868, 'agree_count': 46, 'disagree_count': 7, 'total_rows': 108}, 4: {'measure': 0.3142857142857143, 'agree_count': 11, 'disagree_count': 24, 'total_rows': 90}, 15: {'measure': 0.7058823529411765, 'agree_count': 24, 'disagree_count': 10, 'total_rows': 93}, 17: {'measure': 0.7647058823529411, 'agree_count': 26, 'disagree_count': 8, 'total_rows': 97}, 18: {'measure': 0.7413793103448276, 'agree_count': 43, 'disagree_count': 15, 'total_rows': 86}, 22: {'measure': 0.2857142857142857, 'agree_count': 6, 'disagree_count': 15, 'total_rows': 86}, 36: {'measure': 0.19230769230769232, 'agree_count': 5, 'disagree_count': 21, 'total_rows': 45}, 40: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 4, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 13, 'total_rows': 14}}, 'france': {3: {'measure': 0.7333333333333333, 'agree_count': 55, 'disagree_count': 20, 'total_rows': 108}, 4: {'measure': 0.34, 'agree_count': 17, 'disagree_count': 33, 'total_rows': 90}, 15: {'measure': 0.66, 'agree_count': 33, 'disagree_count': 17, 'total_rows': 93}, 17: {'measure': 0.6851851851851852, 'agree_count': 37, 'disagree_count': 17, 'total_rows': 97}, 18: {'measure': 0.6571428571428571, 'agree_count': 46, 'disagree_count': 24, 'total_rows': 86}, 22: {'measure': 0.43243243243243246, 'agree_count': 16, 'disagree_count': 21, 'total_rows': 86}, 36: {'measure': 0.25, 'agree_count': 9, 'disagree_count': 27, 'total_rows': 45}, 40: {'measure': 0.2857142857142857, 'agree_count': 4, 'disagree_count': 10, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'china': {3: {'measure': 0.8888888888888888, 'agree_count': 16, 'disagree_count': 2, 'total_rows': 108}, 4: {'measure': 0.6, 'agree_count': 3, 'disagree_count': 2, 'total_rows': 90}, 15: {'measure': 0.5, 'agree_count': 7, 'disagree_count': 7, 'total_rows': 93}, 17: {'measure': 0.6666666666666666, 'agree_count': 8, 'disagree_count': 4, 'total_rows': 97}, 18: {'measure': 0.8666666666666667, 'agree_count': 13, 'disagree_count': 2, 'total_rows': 86}, 22: {'measure': 0.3333333333333333, 'agree_count': 3, 'disagree_count': 6, 'total_rows': 86}, 36: {'measure': 0.75, 'agree_count': 3, 'disagree_count': 1, 'total_rows': 45}, 40: {'measure': 0.8, 'agree_count': 4, 'disagree_count': 1, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 3, 'total_rows': 14}}, 'germany': {3: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 108}, 4: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 90}, 15: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 93}, 17: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 97}, 18: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 86}, 22: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 86}, 36: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 45}, 40: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 42}, 50: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 14}}, 'russia': {3: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 108}, 4: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 90}, 15: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 93}, 17: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 97}, 18: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 86}, 22: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 86}, 36: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 45}, 40: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 42}, 50: {'measure': 0, 'agree_count': 0, 'disagree_count': 0, 'total_rows': 14}}, 'ukraine': {3: {'measure': 0.5974025974025974, 'agree_count': 46, 'disagree_count': 31, 'total_rows': 108}, 4: {'measure': 0.43243243243243246, 'agree_count': 16, 'disagree_count': 21, 'total_rows': 90}, 15: {'measure': 0.5303030303030303, 'agree_count': 35, 'disagree_count': 31, 'total_rows': 93}, 17: {'measure': 0.7115384615384616, 'agree_count': 37, 'disagree_count': 15, 'total_rows': 97}, 18: {'measure': 0.6029411764705882, 'agree_count': 41, 'disagree_count': 27, 'total_rows': 86}, 22: {'measure': 0.5151515151515151, 'agree_count': 17, 'disagree_count': 16, 'total_rows': 86}, 36: {'measure': 0.16666666666666666, 'agree_count': 5, 'disagree_count': 25, 'total_rows': 45}, 40: {'measure': 0.1875, 'agree_count': 3, 'disagree_count': 13, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 12, 'total_rows': 14}}, 'iran': {3: {'measure': 0.7425742574257426, 'agree_count': 75, 'disagree_count': 26, 'total_rows': 108}, 4: {'measure': 0.5844155844155844, 'agree_count': 45, 'disagree_count': 32, 'total_rows': 90}, 15: {'measure': 0.7023809523809523, 'agree_count': 59, 'disagree_count': 25, 'total_rows': 93}, 17: {'measure': 0.6363636363636364, 'agree_count': 56, 'disagree_count': 32, 'total_rows': 97}, 18: {'measure': 0.7037037037037037, 'agree_count': 57, 'disagree_count': 24, 'total_rows': 86}, 22: {'measure': 0.44, 'agree_count': 33, 'disagree_count': 42, 'total_rows': 86}, 36: {'measure': 0.3902439024390244, 'agree_count': 16, 'disagree_count': 25, 'total_rows': 45}, 40: {'measure': 0.6923076923076923, 'agree_count': 27, 'disagree_count': 12, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'israel': {3: {'measure': 0.6382978723404256, 'agree_count': 60, 'disagree_count': 34, 'total_rows': 108}, 4: {'measure': 0.48, 'agree_count': 36, 'disagree_count': 39, 'total_rows': 90}, 15: {'measure': 0.6144578313253012, 'agree_count': 51, 'disagree_count': 32, 'total_rows': 93}, 17: {'measure': 0.7415730337078652, 'agree_count': 66, 'disagree_count': 23, 'total_rows': 97}, 18: {'measure': 0.6627906976744186, 'agree_count': 57, 'disagree_count': 29, 'total_rows': 86}, 22: {'measure': 0.47297297297297297, 'agree_count': 35, 'disagree_count': 39, 'total_rows': 86}, 36: {'measure': 0.2222222222222222, 'agree_count': 10, 'disagree_count': 35, 'total_rows': 45}, 40: {'measure': 0.6571428571428571, 'agree_count': 23, 'disagree_count': 12, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'america': {3: {'measure': 0.8333333333333334, 'agree_count': 65, 'disagree_count': 13, 'total_rows': 108}, 4: {'measure': 0.3114754098360656, 'agree_count': 19, 'disagree_count': 42, 'total_rows': 90}, 15: {'measure': 0.7833333333333333, 'agree_count': 47, 'disagree_count': 13, 'total_rows': 93}, 17: {'measure': 0.8088235294117647, 'agree_count': 55, 'disagree_count': 13, 'total_rows': 97}, 18: {'measure': 0.7777777777777778, 'agree_count': 56, 'disagree_count': 16, 'total_rows': 86}, 22: {'measure': 0.5192307692307693, 'agree_count': 27, 'disagree_count': 25, 'total_rows': 86}, 36: {'measure': 0.425, 'agree_count': 17, 'disagree_count': 23, 'total_rows': 45}, 40: {'measure': 0.45454545454545453, 'agree_count': 10, 'disagree_count': 12, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}}

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
OUT_DIR = Path("results/llama3.1-70b/native")
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
