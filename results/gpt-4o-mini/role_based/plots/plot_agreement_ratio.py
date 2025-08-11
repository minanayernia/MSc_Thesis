import json
import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA = {'Iran': {3: {'measure': 0.6851851851851852, 'agree_count': 74, 'disagree_count': 34, 'total_rows': 108}, 4: {'measure': 0.28888888888888886, 'agree_count': 26, 'disagree_count': 64, 'total_rows': 90}, 15: {'measure': 0.9139784946236559, 'agree_count': 85, 'disagree_count': 8, 'total_rows': 93}, 17: {'measure': 0.7319587628865979, 'agree_count': 71, 'disagree_count': 26, 'total_rows': 97}, 18: {'measure': 0.7558139534883721, 'agree_count': 65, 'disagree_count': 21, 'total_rows': 86}, 22: {'measure': 0.35294117647058826, 'agree_count': 30, 'disagree_count': 55, 'total_rows': 86}, 36: {'measure': 0.15555555555555556, 'agree_count': 7, 'disagree_count': 38, 'total_rows': 45}, 40: {'measure': 0.2619047619047619, 'agree_count': 11, 'disagree_count': 31, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'America': {3: {'measure': 0.5648148148148148, 'agree_count': 61, 'disagree_count': 47, 'total_rows': 108}, 4: {'measure': 0.4444444444444444, 'agree_count': 40, 'disagree_count': 50, 'total_rows': 90}, 15: {'measure': 0.41935483870967744, 'agree_count': 39, 'disagree_count': 54, 'total_rows': 93}, 17: {'measure': 0.7835051546391752, 'agree_count': 76, 'disagree_count': 21, 'total_rows': 97}, 18: {'measure': 0.7325581395348837, 'agree_count': 63, 'disagree_count': 23, 'total_rows': 86}, 22: {'measure': 0.5116279069767442, 'agree_count': 44, 'disagree_count': 42, 'total_rows': 86}, 36: {'measure': 0.17777777777777778, 'agree_count': 8, 'disagree_count': 37, 'total_rows': 45}, 40: {'measure': 0.38095238095238093, 'agree_count': 16, 'disagree_count': 26, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'Russia': {3: {'measure': 0.5277777777777778, 'agree_count': 57, 'disagree_count': 51, 'total_rows': 108}, 4: {'measure': 0.3111111111111111, 'agree_count': 28, 'disagree_count': 62, 'total_rows': 90}, 15: {'measure': 0.7096774193548387, 'agree_count': 66, 'disagree_count': 27, 'total_rows': 93}, 17: {'measure': 0.7525773195876289, 'agree_count': 73, 'disagree_count': 24, 'total_rows': 97}, 18: {'measure': 0.7441860465116279, 'agree_count': 64, 'disagree_count': 22, 'total_rows': 86}, 22: {'measure': 0.4235294117647059, 'agree_count': 36, 'disagree_count': 49, 'total_rows': 86}, 36: {'measure': 0.17777777777777778, 'agree_count': 8, 'disagree_count': 37, 'total_rows': 45}, 40: {'measure': 0.23809523809523808, 'agree_count': 10, 'disagree_count': 32, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'Israel': {3: {'measure': 0.5925925925925926, 'agree_count': 64, 'disagree_count': 44, 'total_rows': 108}, 4: {'measure': 0.4444444444444444, 'agree_count': 40, 'disagree_count': 50, 'total_rows': 90}, 15: {'measure': 0.4838709677419355, 'agree_count': 45, 'disagree_count': 48, 'total_rows': 93}, 17: {'measure': 0.7731958762886598, 'agree_count': 75, 'disagree_count': 22, 'total_rows': 97}, 18: {'measure': 0.7441860465116279, 'agree_count': 64, 'disagree_count': 22, 'total_rows': 86}, 22: {'measure': 0.4470588235294118, 'agree_count': 38, 'disagree_count': 47, 'total_rows': 86}, 36: {'measure': 0.2, 'agree_count': 9, 'disagree_count': 36, 'total_rows': 45}, 40: {'measure': 0.3333333333333333, 'agree_count': 14, 'disagree_count': 28, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'Ukraine': {3: {'measure': 0.7222222222222222, 'agree_count': 78, 'disagree_count': 30, 'total_rows': 108}, 4: {'measure': 0.3111111111111111, 'agree_count': 28, 'disagree_count': 62, 'total_rows': 90}, 15: {'measure': 0.3225806451612903, 'agree_count': 30, 'disagree_count': 63, 'total_rows': 93}, 17: {'measure': 0.7731958762886598, 'agree_count': 75, 'disagree_count': 22, 'total_rows': 97}, 18: {'measure': 0.7790697674418605, 'agree_count': 67, 'disagree_count': 19, 'total_rows': 86}, 22: {'measure': 0.43023255813953487, 'agree_count': 37, 'disagree_count': 49, 'total_rows': 86}, 36: {'measure': 0.2222222222222222, 'agree_count': 10, 'disagree_count': 35, 'total_rows': 45}, 40: {'measure': 0.2619047619047619, 'agree_count': 11, 'disagree_count': 31, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'China': {3: {'measure': 0.6296296296296297, 'agree_count': 68, 'disagree_count': 40, 'total_rows': 108}, 4: {'measure': 0.30337078651685395, 'agree_count': 27, 'disagree_count': 62, 'total_rows': 90}, 15: {'measure': 0.7526881720430108, 'agree_count': 70, 'disagree_count': 23, 'total_rows': 93}, 17: {'measure': 0.7525773195876289, 'agree_count': 73, 'disagree_count': 24, 'total_rows': 97}, 18: {'measure': 0.6976744186046512, 'agree_count': 60, 'disagree_count': 26, 'total_rows': 86}, 22: {'measure': 0.4, 'agree_count': 34, 'disagree_count': 51, 'total_rows': 86}, 36: {'measure': 0.2, 'agree_count': 9, 'disagree_count': 36, 'total_rows': 45}, 40: {'measure': 0.14285714285714285, 'agree_count': 6, 'disagree_count': 36, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'Germany': {3: {'measure': 0.7129629629629629, 'agree_count': 77, 'disagree_count': 31, 'total_rows': 108}, 4: {'measure': 0.28888888888888886, 'agree_count': 26, 'disagree_count': 64, 'total_rows': 90}, 15: {'measure': 0.45652173913043476, 'agree_count': 42, 'disagree_count': 50, 'total_rows': 93}, 17: {'measure': 0.8350515463917526, 'agree_count': 81, 'disagree_count': 16, 'total_rows': 97}, 18: {'measure': 0.7441860465116279, 'agree_count': 64, 'disagree_count': 22, 'total_rows': 86}, 22: {'measure': 0.5465116279069767, 'agree_count': 47, 'disagree_count': 39, 'total_rows': 86}, 36: {'measure': 0.26666666666666666, 'agree_count': 12, 'disagree_count': 33, 'total_rows': 45}, 40: {'measure': 0.2857142857142857, 'agree_count': 12, 'disagree_count': 30, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'France': {3: {'measure': 0.6851851851851852, 'agree_count': 74, 'disagree_count': 34, 'total_rows': 108}, 4: {'measure': 0.3, 'agree_count': 27, 'disagree_count': 63, 'total_rows': 90}, 15: {'measure': 0.5483870967741935, 'agree_count': 51, 'disagree_count': 42, 'total_rows': 93}, 17: {'measure': 0.8247422680412371, 'agree_count': 80, 'disagree_count': 17, 'total_rows': 97}, 18: {'measure': 0.8023255813953488, 'agree_count': 69, 'disagree_count': 17, 'total_rows': 86}, 22: {'measure': 0.47058823529411764, 'agree_count': 40, 'disagree_count': 45, 'total_rows': 86}, 36: {'measure': 0.2222222222222222, 'agree_count': 10, 'disagree_count': 35, 'total_rows': 45}, 40: {'measure': 0.23809523809523808, 'agree_count': 10, 'disagree_count': 32, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'Italy': {3: {'measure': 0.6944444444444444, 'agree_count': 75, 'disagree_count': 33, 'total_rows': 108}, 4: {'measure': 0.28888888888888886, 'agree_count': 26, 'disagree_count': 64, 'total_rows': 90}, 15: {'measure': 0.5698924731182796, 'agree_count': 53, 'disagree_count': 40, 'total_rows': 93}, 17: {'measure': 0.8247422680412371, 'agree_count': 80, 'disagree_count': 17, 'total_rows': 97}, 18: {'measure': 0.7674418604651163, 'agree_count': 66, 'disagree_count': 20, 'total_rows': 86}, 22: {'measure': 0.4883720930232558, 'agree_count': 42, 'disagree_count': 44, 'total_rows': 86}, 36: {'measure': 0.26666666666666666, 'agree_count': 12, 'disagree_count': 33, 'total_rows': 45}, 40: {'measure': 0.3333333333333333, 'agree_count': 14, 'disagree_count': 28, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}, 'System': {3: {'measure': 0.6296296296296297, 'agree_count': 68, 'disagree_count': 40, 'total_rows': 108}, 4: {'measure': 0.4943820224719101, 'agree_count': 44, 'disagree_count': 45, 'total_rows': 90}, 15: {'measure': 0.43478260869565216, 'agree_count': 40, 'disagree_count': 52, 'total_rows': 93}, 17: {'measure': 0.8247422680412371, 'agree_count': 80, 'disagree_count': 17, 'total_rows': 97}, 18: {'measure': 0.7790697674418605, 'agree_count': 67, 'disagree_count': 19, 'total_rows': 86}, 22: {'measure': 0.6, 'agree_count': 51, 'disagree_count': 34, 'total_rows': 86}, 36: {'measure': 0.24444444444444444, 'agree_count': 11, 'disagree_count': 34, 'total_rows': 45}, 40: {'measure': 0.38095238095238093, 'agree_count': 16, 'disagree_count': 26, 'total_rows': 42}, 50: {'measure': 0.0, 'agree_count': 0, 'disagree_count': 14, 'total_rows': 14}}}

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

OUTDIR = Path("results/gpt-4o-mini/role_based/plots")
OUTDIR.mkdir(exist_ok=True)

def dict_to_long_df(data: dict) -> pd.DataFrame:
    """Flatten nested dict {role: {topic: {measure, agree_count,...}}} -> long DataFrame."""
    rows = []
    for role, topics in data.items():
        for topic_id, vals in topics.items():
            rows.append({
                "Role": role,
                "Topic_ID": int(topic_id),
                "Measure": float(vals["measure"]),
                "Agree": int(vals["agree_count"]),
                "Disagree": int(vals["disagree_count"]),
                "Total": int(vals["total_rows"]),
            })
    df = pd.DataFrame(rows)
    return df

def add_topic_names(df: pd.DataFrame, topic_map: dict) -> pd.DataFrame:
    df = df.copy()
    df = df[df["Topic_ID"].isin(topic_map.keys())]
    df["Topic_Name"] = df["Topic_ID"].map(topic_map)
    # order topics nicely
    name_order = [topic_map[k] for k in topic_map.keys()]
    df["Topic_Name"] = pd.Categorical(df["Topic_Name"], categories=name_order, ordered=True)
    return df

def save_wide_table(df_named: pd.DataFrame, outdir: Path) -> pd.DataFrame:
    """Create a wide table Topic_Name x Role with Measure values and save to CSV."""
    wide = df_named.pivot(index="Topic_Name", columns="Role", values="Measure").sort_index()
    csv_path = outdir / "agreement_ratios_by_topic_role.csv"
    wide.to_csv(csv_path, float_format="%.6f")
    print(f"[saved] {csv_path}")
    return wide

def plot_per_topic_bars(df_named: pd.DataFrame, outdir: Path):
    """One bar chart per topic (x: Role, y: Measure). Saves PNGs."""
    for topic_name, sub in df_named.groupby("Topic_Name", sort=False):
        plt.figure(figsize=(10, 5))
        plt.bar(sub["Role"], sub["Measure"])
        plt.ylim(0, 1)
        plt.title(f"Agreement Ratio – {topic_name}")
        plt.ylabel("Agreement Ratio")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        png_path = outdir / f"agreement_ratio_{topic_name.replace(' ', '_').replace('-', '_')}.png"
        plt.savefig(png_path, dpi=200)
        plt.close()
        print(f"[saved] {png_path}")

def main():
    df = dict_to_long_df(DATA)
    df_named = add_topic_names(df, TOPIC_MAP)
    wide = save_wide_table(df_named, OUTDIR)
    plot_per_topic_bars(df_named, OUTDIR)

    # Optional: also save the long-format table
    long_csv = OUTDIR / "agreement_ratios_long.csv"
    df_named.to_csv(long_csv, index=False)
    print(f"[saved] {long_csv}")

if __name__ == "__main__":
    main()
