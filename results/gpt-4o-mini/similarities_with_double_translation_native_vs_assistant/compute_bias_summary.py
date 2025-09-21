import pandas as pd

def compute_country_bias_summary(country_sources, topic_col='topic', similarity_col='mean_similarity'):
    """
    Given a dict mapping country -> (DataFrame or CSV path),
    compute per-country average ideological alignment (bias) with assistant responses.

    Returns:
        pd.DataFrame with columns: country, avg_bias_score, bias_std, n_topics
    """
    frames = []

    for country, src in country_sources.items():
        # Load source
        if isinstance(src, pd.DataFrame):
            df = src.copy()
        elif isinstance(src, str):
            df = pd.read_csv(src)
        else:
            raise TypeError(f"Unsupported source type for {country}: {type(src)}")

        # Basic column checks / coercions
        if topic_col not in df.columns:
            raise KeyError(f"Missing '{topic_col}' column for {country}")
        if similarity_col not in df.columns:
            raise KeyError(f"Missing '{similarity_col}' column for {country}")

        # Ensure numeric similarity and drop NaNs
        df[similarity_col] = pd.to_numeric(df[similarity_col], errors='coerce')
        df = df.dropna(subset=[similarity_col])

        df["country"] = country
        df["bias_score"] = df[similarity_col]
        frames.append(df[["country", topic_col, "bias_score"]])

    if not frames:
        return pd.DataFrame(columns=["country", "avg_bias_score", "bias_std", "n_topics"])

    merged = pd.concat(frames, ignore_index=True)

    # Aggregate per country
    summary = (
        merged.groupby("country")
        .agg(
            avg_bias_score=("bias_score", "mean"),
            bias_std=("bias_score", "std"),
            n_topics=(topic_col, "nunique"),
        )
        .reset_index()
        .sort_values("avg_bias_score", ascending=False)
    )

    return summary


# Dictionary of country -> CSV path (or DataFrame)
country_dfs = {
    "USA":     "results/gpt-4o-mini/similarities_with_double_translation_native_vs_assistant/similarity_avgENIT_America_native_vs_assistant.csv",
    "China":   "results/gpt-4o-mini/similarities_with_double_translation_native_vs_assistant/similarity_avgENIT_China_native_vs_assistant.csv",
    "France":  "results/gpt-4o-mini/similarities_with_double_translation_native_vs_assistant/similarity_avgENIT_France_native_vs_assistant.csv",
    "Germany": "results/gpt-4o-mini/similarities_with_double_translation_native_vs_assistant/similarity_avgENIT_Germany_native_vs_assistant.csv",
    "Iran":    "results/gpt-4o-mini/similarities_with_double_translation_native_vs_assistant/similarity_avgENIT_Iran_native_vs_assistant.csv",
    "Israel":  "results/gpt-4o-mini/similarities_with_double_translation_native_vs_assistant/similarity_avgENIT_Israel_native_vs_assistant.csv",
    "Italy":   "results/gpt-4o-mini/similarities_with_double_translation_native_vs_assistant/similarity_avgENIT_Italy_native_vs_assistant.csv",
    "Russia":  "results/gpt-4o-mini/similarities_with_double_translation_native_vs_assistant/similarity_avgENIT_Russia_native_vs_assistant.csv",
    "Ukraine": "results/gpt-4o-mini/similarities_with_double_translation_native_vs_assistant/similarity_avgENIT_Ukraine_native_vs_assistant.csv",
}

# Compute and save
summary_df = compute_country_bias_summary(country_dfs)
out_path = "results/gpt-4o-mini/similarities_with_double_translation_native_vs_assistant/bias_summary_native_vs_assistant.csv"
summary_df.to_csv(out_path, index=False)
print(f"Saved: {out_path}")
