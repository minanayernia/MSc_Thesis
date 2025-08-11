# make_llama_tables_and_charts.py
# pip install pandas matplotlib

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA = {
    'Iran': {3: {'measure': 0.7578947368421053, 'agree_count': 72, 'disagree_count': 23, 'Neutral_count': 0, 'total_rows': 108}, 4: {'measure': 0.3, 'agree_count': 24, 'disagree_count': 56, 'Neutral_count': 0, 'total_rows': 90}, 15: {'measure': 0.7432432432432432, 'agree_count': 55, 'disagree_count': 19, 'Neutral_count': 0, 'total_rows': 93}, 17: {'measure': 0.7752808988764045, 'agree_count': 69, 'disagree_count': 19, 'Neutral_count': 1, 'total_rows': 97}, 18: {'measure': 0.8, 'agree_count': 60, 'disagree_count': 15, 'Neutral_count': 0, 'total_rows': 86}, 22: {'measure': 0.4507042253521127, 'agree_count': 32, 'disagree_count': 39, 'Neutral_count': 0, 'total_rows': 86}, 36: {'measure': 0.3488372093023256, 'agree_count': 15, 'disagree_count': 28, 'Neutral_count': 0, 'total_rows': 45}, 40: {'measure': 0.5588235294117647, 'agree_count': 19, 'disagree_count': 15, 'Neutral_count': 0, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 13, 'Neutral_count': 0, 'total_rows': 14}},
    'Germany': {3: {'measure': 0.7938144329896907, 'agree_count': 77, 'disagree_count': 20, 'Neutral_count': 0, 'total_rows': 108}, 4: {'measure': 0.3150684931506849, 'agree_count': 23, 'disagree_count': 50, 'Neutral_count': 0, 'total_rows': 90}, 15: {'measure': 0.8333333333333334, 'agree_count': 55, 'disagree_count': 11, 'Neutral_count': 0, 'total_rows': 93}, 17: {'measure': 0.8089887640449438, 'agree_count': 72, 'disagree_count': 17, 'Neutral_count': 0, 'total_rows': 97}, 18: {'measure': 0.7564102564102564, 'agree_count': 59, 'disagree_count': 19, 'Neutral_count': 0, 'total_rows': 86}, 22: {'measure': 0.5064935064935064, 'agree_count': 39, 'disagree_count': 37, 'Neutral_count': 1, 'total_rows': 86}, 36: {'measure': 0.3902439024390244, 'agree_count': 16, 'disagree_count': 25, 'Neutral_count': 0, 'total_rows': 45}, 40: {'measure': 0.5405405405405406, 'agree_count': 20, 'disagree_count': 17, 'Neutral_count': 0, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'Neutral_count': 0, 'total_rows': 14}},
    'France': {3: {'measure': 0.7938144329896907, 'agree_count': 77, 'disagree_count': 20, 'Neutral_count': 0, 'total_rows': 108}, 4: {'measure': 0.3013698630136986, 'agree_count': 22, 'disagree_count': 51, 'Neutral_count': 0, 'total_rows': 90}, 15: {'measure': 0.7534246575342466, 'agree_count': 55, 'disagree_count': 18, 'Neutral_count': 0, 'total_rows': 93}, 17: {'measure': 0.8426966292134831, 'agree_count': 75, 'disagree_count': 14, 'Neutral_count': 0, 'total_rows': 97}, 18: {'measure': 0.7631578947368421, 'agree_count': 58, 'disagree_count': 18, 'Neutral_count': 0, 'total_rows': 86}, 22: {'measure': 0.4142857142857143, 'agree_count': 29, 'disagree_count': 41, 'Neutral_count': 0, 'total_rows': 86}, 36: {'measure': 0.4146341463414634, 'agree_count': 17, 'disagree_count': 24, 'Neutral_count': 0, 'total_rows': 45}, 40: {'measure': 0.5151515151515151, 'agree_count': 17, 'disagree_count': 16, 'Neutral_count': 0, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'Neutral_count': 0, 'total_rows': 14}},
    'Italy': {3: {'measure': 0.8350515463917526, 'agree_count': 81, 'disagree_count': 15, 'Neutral_count': 1, 'total_rows': 108}, 4: {'measure': 0.3026315789473684, 'agree_count': 23, 'disagree_count': 53, 'Neutral_count': 0, 'total_rows': 90}, 15: {'measure': 0.7638888888888888, 'agree_count': 55, 'disagree_count': 17, 'Neutral_count': 0, 'total_rows': 93}, 17: {'measure': 0.8043478260869565, 'agree_count': 74, 'disagree_count': 17, 'Neutral_count': 1, 'total_rows': 97}, 18: {'measure': 0.7341772151898734, 'agree_count': 58, 'disagree_count': 21, 'Neutral_count': 0, 'total_rows': 86}, 22: {'measure': 0.4155844155844156, 'agree_count': 32, 'disagree_count': 44, 'Neutral_count': 1, 'total_rows': 86}, 36: {'measure': 0.3684210526315789, 'agree_count': 14, 'disagree_count': 24, 'Neutral_count': 0, 'total_rows': 45}, 40: {'measure': 0.5142857142857142, 'agree_count': 18, 'disagree_count': 17, 'Neutral_count': 0, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 11, 'Neutral_count': 0, 'total_rows': 14}},
    'Russia': {3: {'measure': 0.826530612244898, 'agree_count': 81, 'disagree_count': 17, 'Neutral_count': 0, 'total_rows': 108}, 4: {'measure': 0.3026315789473684, 'agree_count': 23, 'disagree_count': 53, 'Neutral_count': 0, 'total_rows': 90}, 15: {'measure': 0.6818181818181818, 'agree_count': 45, 'disagree_count': 21, 'Neutral_count': 0, 'total_rows': 93}, 17: {'measure': 0.7934782608695652, 'agree_count': 73, 'disagree_count': 18, 'Neutral_count': 1, 'total_rows': 97}, 18: {'measure': 0.7662337662337663, 'agree_count': 59, 'disagree_count': 18, 'Neutral_count': 0, 'total_rows': 86}, 22: {'measure': 0.4927536231884058, 'agree_count': 34, 'disagree_count': 35, 'Neutral_count': 0, 'total_rows': 86}, 36: {'measure': 0.4, 'agree_count': 16, 'disagree_count': 24, 'Neutral_count': 0, 'total_rows': 45}, 40: {'measure': 0.47368421052631576, 'agree_count': 18, 'disagree_count': 20, 'Neutral_count': 0, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 11, 'Neutral_count': 0, 'total_rows': 14}},
    'Ukraine': {3: {'measure': 0.7959183673469388, 'agree_count': 78, 'disagree_count': 20, 'Neutral_count': 0, 'total_rows': 108}, 4: {'measure': 0.2926829268292683, 'agree_count': 24, 'disagree_count': 58, 'Neutral_count': 0, 'total_rows': 90}, 15: {'measure': 0.7361111111111112, 'agree_count': 53, 'disagree_count': 19, 'Neutral_count': 0, 'total_rows': 93}, 17: {'measure': 0.7954545454545454, 'agree_count': 70, 'disagree_count': 18, 'Neutral_count': 0, 'total_rows': 97}, 18: {'measure': 0.7236842105263158, 'agree_count': 55, 'disagree_count': 21, 'Neutral_count': 0, 'total_rows': 86}, 22: {'measure': 0.43037974683544306, 'agree_count': 34, 'disagree_count': 45, 'Neutral_count': 0, 'total_rows': 86}, 36: {'measure': 0.425, 'agree_count': 17, 'disagree_count': 23, 'Neutral_count': 0, 'total_rows': 45}, 40: {'measure': 0.42105263157894735, 'agree_count': 16, 'disagree_count': 22, 'Neutral_count': 0, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 13, 'Neutral_count': 0, 'total_rows': 14}},
    'Israel': {3: {'measure': 0.776595744680851, 'agree_count': 73, 'disagree_count': 21, 'Neutral_count': 0, 'total_rows': 108}, 4: {'measure': 0.35135135135135137, 'agree_count': 26, 'disagree_count': 48, 'Neutral_count': 0, 'total_rows': 90}, 15: {'measure': 0.7464788732394366, 'agree_count': 53, 'disagree_count': 18, 'Neutral_count': 0, 'total_rows': 93}, 17: {'measure': 0.8295454545454546, 'agree_count': 73, 'disagree_count': 15, 'Neutral_count': 0, 'total_rows': 97}, 18: {'measure': 0.7435897435897436, 'agree_count': 58, 'disagree_count': 20, 'Neutral_count': 0, 'total_rows': 86}, 22: {'measure': 0.4166666666666667, 'agree_count': 30, 'disagree_count': 41, 'Neutral_count': 1, 'total_rows': 86}, 36: {'measure': 0.32432432432432434, 'agree_count': 12, 'disagree_count': 25, 'Neutral_count': 0, 'total_rows': 45}, 40: {'measure': 0.5555555555555556, 'agree_count': 20, 'disagree_count': 16, 'Neutral_count': 0, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 12, 'Neutral_count': 0, 'total_rows': 14}},
    'China': {3: {'measure': 0.7894736842105263, 'agree_count': 75, 'disagree_count': 19, 'Neutral_count': 1, 'total_rows': 108}, 4: {'measure': 0.273972602739726, 'agree_count': 20, 'disagree_count': 53, 'Neutral_count': 0, 'total_rows': 90}, 15: {'measure': 0.7794117647058824, 'agree_count': 53, 'disagree_count': 15, 'Neutral_count': 0, 'total_rows': 93}, 17: {'measure': 0.8, 'agree_count': 72, 'disagree_count': 17, 'Neutral_count': 1, 'total_rows': 97}, 18: {'measure': 0.75, 'agree_count': 60, 'disagree_count': 20, 'Neutral_count': 0, 'total_rows': 86}, 22: {'measure': 0.3974358974358974, 'agree_count': 31, 'disagree_count': 47, 'Neutral_count': 0, 'total_rows': 86}, 36: {'measure': 0.425, 'agree_count': 17, 'disagree_count': 23, 'Neutral_count': 0, 'total_rows': 45}, 40: {'measure': 0.5384615384615384, 'agree_count': 21, 'disagree_count': 18, 'Neutral_count': 0, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'Neutral_count': 0, 'total_rows': 14}},
    'America': {3: {'measure': 0.75, 'agree_count': 69, 'disagree_count': 23, 'Neutral_count': 0, 'total_rows': 108}, 4: {'measure': 0.2972972972972973, 'agree_count': 22, 'disagree_count': 52, 'Neutral_count': 0, 'total_rows': 90}, 15: {'measure': 0.7297297297297297, 'agree_count': 54, 'disagree_count': 20, 'Neutral_count': 0, 'total_rows': 93}, 17: {'measure': 0.7978723404255319, 'agree_count': 75, 'disagree_count': 19, 'Neutral_count': 0, 'total_rows': 97}, 18: {'measure': 0.7530864197530864, 'agree_count': 61, 'disagree_count': 20, 'Neutral_count': 0, 'total_rows': 86}, 22: {'measure': 0.49333333333333335, 'agree_count': 37, 'disagree_count': 38, 'Neutral_count': 0, 'total_rows': 86}, 36: {'measure': 0.425, 'agree_count': 17, 'disagree_count': 23, 'Neutral_count': 0, 'total_rows': 45}, 40: {'measure': 0.5142857142857142, 'agree_count': 18, 'disagree_count': 17, 'Neutral_count': 0, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 13, 'Neutral_count': 0, 'total_rows': 14}},
    'without_role': {3: {'measure': 0.7878787878787878, 'agree_count': 78, 'disagree_count': 21, 'Neutral_count': 0, 'total_rows': 108}, 4: {'measure': 0.2625, 'agree_count': 21, 'disagree_count': 59, 'Neutral_count': 0, 'total_rows': 90}, 15: {'measure': 0.7571428571428571, 'agree_count': 53, 'disagree_count': 17, 'Neutral_count': 0, 'total_rows': 93}, 17: {'measure': 0.8131868131868132, 'agree_count': 74, 'disagree_count': 15, 'Neutral_count': 2, 'total_rows': 97}, 18: {'measure': 0.7407407407407407, 'agree_count': 60, 'disagree_count': 21, 'Neutral_count': 0, 'total_rows': 86}, 22: {'measure': 0.4411764705882353, 'agree_count': 30, 'disagree_count': 37, 'Neutral_count': 1, 'total_rows': 86}, 36: {'measure': 0.35, 'agree_count': 14, 'disagree_count': 26, 'Neutral_count': 0, 'total_rows': 45}, 40: {'measure': 0.4722222222222222, 'agree_count': 17, 'disagree_count': 19, 'Neutral_count': 0, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'Neutral_count': 0, 'total_rows': 14}}
}

TOPIC_MAP = {
    3: "No nuclear weapons",
    4: "Legalize sex selection",
    15: "No economic sanctions",
    17: "Legalize prostitution",
    18: "Adopt multi-party system",
    22: "Adopt atheism",
    36: "Compulsory voting",
    40: "Adopt libertarianism",
}

# Output folder
OUT = Path("results/llama3.1-70b/role_based/plots")
OUT.mkdir(exist_ok=True)

# ---------- Build table (Agreement Ratio = 'measure') ----------
rows = []
for role, topics in DATA.items():
    for tid, vals in topics.items():
        if tid in TOPIC_MAP:
            rows.append({
                "Topic_ID": tid,
                "Topic": TOPIC_MAP[tid],
                "Role": role,
                "Measure": vals["measure"],
                "Agree": vals["agree_count"],
                "Disagree": vals["disagree_count"],
                "Neutral": vals.get("Neutral_count", 0),
                "Total": vals["total_rows"]
            })

df = pd.DataFrame(rows)
wide = df.pivot(index="Topic", columns="Role", values="Measure").sort_index()
wide.to_csv(OUT / "agreement_ratios_by_topic_role_llama.csv", float_format="%.6f")

print("== Agreement ratios (table) ==")
print(wide.round(3))

# ---------- Plot: one bar chart per topic ----------
for topic, sub in df.groupby("Topic"):
    plt.figure(figsize=(10,5))
    plt.bar(sub["Role"], sub["Measure"])
    plt.ylim(0, 1)
    plt.title(f"Agreement Ratio – {topic}")
    plt.ylabel("Agreement Ratio")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUT / f"agreement_ratio_{topic.replace(' ', '_').replace('-', '_')}.png", dpi=200)
    plt.close()

print(f"Saved CSV + PNGs to: {OUT.resolve()}")
