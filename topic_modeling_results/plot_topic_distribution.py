import pandas as pd
import matplotlib.pyplot as plt

def plot_and_save_topic_distribution(
    csv_path,
    output_counts="topic_modeling_results/plots/topic_distribution.csv",
    output_chart="topic_modeling_results/plots/topic_distribution.png",
    topic_column="Topic"
):
    # Topics of interest
    topic_map = {
        3: "Nuclear weapons & war",
        4: "Sex selection & gender",
        15: "Economic sanctions & countries",
        17: "Legalizing prostitution",
        18: "Multi-party system",
        22: "Atheism & religion",
        36: "Compulsory voting",
        40: "Libertarianism & government",
    }

    # Load CSV
    df = pd.read_csv(csv_path)

    # Count occurrences for selected topics
    counts = (
        df[df[topic_column].isin(topic_map.keys())][topic_column]
        .map(topic_map)
        .value_counts()
    )

    # Save counts to CSV
    counts_df = counts.reset_index()
    counts_df.columns = ["Theme", "Count"]
    counts_df.to_csv(output_counts, index=False)
    print(f"Counts saved to {output_counts}")

    # Plot pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(
        counts,
        labels=counts.index,
        autopct='%1.1f%%',
        startangle=90,
        counterclock=False
    )
    plt.title("Topic Distribution")
    plt.tight_layout()

    # Save chart to file
    plt.savefig(output_chart, dpi=300)
    print(f"Pie chart saved to {output_chart}")

    # Show chart in notebook
    plt.show()

# Example usage:
plot_and_save_topic_distribution("topic_modeling_results/arguments-training-with-topics.csv")
