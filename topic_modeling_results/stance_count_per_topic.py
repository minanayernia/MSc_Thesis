import pandas as pd
from pathlib import Path

# --- CONFIG ---
CSV_PATH = "topic_modeling_results/arguments-training-with-topics.csv"
OUTPUT_DIR = Path("topic_modeling_results/stance_summaries")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- LOAD ---
df = pd.read_csv(CSV_PATH)

# Drop unnamed index columns if present
for col in list(df.columns):
    if str(col).lower().startswith("unnamed"):
        df = df.drop(columns=[col])

# Expect these exact columns
expected_cols = {"Topic", "document", "Stance", "Conclusion", "Argument ID"}
missing = expected_cols - set(df.columns)
if missing:
    raise ValueError(f"Missing columns in CSV: {missing}\nFound: {list(df.columns)}")

# --- LIGHT CLEANUPS (safe even if "already normalized") ---
# Coerce Topic to numeric for stable sorting; strip whitespace in string cols
df["Topic"] = pd.to_numeric(df["Topic"], errors="coerce")
df["Stance"] = df["Stance"].astype(str).str.strip()
df["Conclusion"] = df["Conclusion"].astype(str).str.strip()

# Optional: set categorical order for nicer plots/tables
stance_order = ["in favor of", "against"]
df["Stance"] = pd.Categorical(df["Stance"], categories=stance_order, ordered=True)

# --- OVERALL COUNTS + PCT ---
overall_counts = (
    df["Stance"]
    .value_counts(dropna=False)
    .rename_axis("Stance")
    .reset_index(name="Count")
    .sort_values("Stance")
)
overall_total = overall_counts["Count"].sum()
overall_counts["Percent"] = (overall_counts["Count"] / overall_total * 100).round(2)

# --- PER TOPIC COUNTS + PCT ---
by_topic_counts = (
    df.groupby(["Topic", "Stance"], as_index=False)
      .size()
      .rename(columns={"size": "Count"})
      .sort_values(["Topic", "Stance"])
)
by_topic_totals = by_topic_counts.groupby("Topic")["Count"].transform("sum")
by_topic_counts["Percent"] = (by_topic_counts["Count"] / by_topic_totals * 100).round(2)

# --- PER (TOPIC, CONCLUSION) COUNTS + WIDE PIVOT ---
by_topic_conclusion_counts = (
    df.groupby(["Topic", "Conclusion", "Stance"], as_index=False)
      .size()
      .rename(columns={"size": "Count"})
      .sort_values(["Topic", "Conclusion", "Stance"])
)

by_topic_conclusion_pivot = by_topic_conclusion_counts.pivot_table(
    index=["Topic", "Conclusion"],
    columns="Stance",
    values="Count",
    fill_value=0,
    aggfunc="sum"
).reset_index()

# --- SAVE SUMMARIES ---
overall_counts.to_csv(OUTPUT_DIR / "stance_overall_counts.csv", index=False)
by_topic_counts.to_csv(OUTPUT_DIR / "stance_by_topic_counts.csv", index=False)
by_topic_conclusion_counts.to_csv(OUTPUT_DIR / "stance_by_topic_conclusion_counts_long.csv", index=False)
by_topic_conclusion_pivot.to_csv(OUTPUT_DIR / "stance_by_topic_conclusion_counts_wide.csv", index=False)

# --- PRINT PREVIEWS ---
print("Overall stance counts:")
print(overall_counts.to_string(index=False))

print("\nStance counts by Topic (first 20 rows):")
print(by_topic_counts.head(20).to_string(index=False))

print("\nStance counts by (Topic, Conclusion) (first 20 rows):")
print(by_topic_conclusion_counts.head(20).to_string(index=False))

# --- NOTES ---
# - 'stance_overall_counts.csv': use for a simple 2-bar plot (in favor vs against).
# - 'stance_by_topic_counts.csv': grouped bars per topic (use the Percent column if you want normalized bars).
# - 'stance_by_topic_conclusion_counts_wide.csv': handy to inspect which conclusions dominate within topics.
