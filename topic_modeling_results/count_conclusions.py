import pandas as pd

# Load your dataset
df = pd.read_csv("topic_modeling_results/arguments-training-with-topics.csv")

# Count distinct conclusions
num_conclusions = df["Conclusion"].nunique()

print(f"Number of distinct conclusions: {num_conclusions}")
conclusion_counts = df["Conclusion"].value_counts()
print(conclusion_counts.head(20))  # top 20
conclusion_counts.to_csv("topic_modeling_results/conclusion_counts.csv")
