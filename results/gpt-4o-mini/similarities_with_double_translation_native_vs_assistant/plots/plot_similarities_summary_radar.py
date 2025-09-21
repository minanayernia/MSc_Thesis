import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

COUNTRY_ORDER = ["USA", "China", "France", "Germany", "Iran", "Israel", "Italy", "Russia", "Ukraine"]

def load_bias_summary(src, country_col="country", value_col="avg_bias_score",
                      order=COUNTRY_ORDER, country_aliases=None):
    """
    Load a precomputed bias summary (CSV path or DataFrame) and align to fixed country order.
    Expects columns: country, avg_bias_score (and optionally bias_std, n_topics).
    """
    if isinstance(src, pd.DataFrame):
        df = src.copy()
    elif isinstance(src, str):
        df = pd.read_csv(src)
    else:
        raise TypeError(f"Unsupported source type: {type(src)}")

    if country_aliases:
        df[country_col] = df[country_col].replace(country_aliases)

    # Ensure numeric
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")

    # Keep all countries in fixed order (missing -> NaN to keep the angle slot)
    order_df = pd.DataFrame({country_col: order})
    df = order_df.merge(df, on=country_col, how="left")

    return df

def _values_in_order(summary_df, value_col="avg_bias_score", order=COUNTRY_ORDER):
    m = dict(zip(summary_df["country"], summary_df[value_col]))
    return [m.get(c, np.nan) for c in order]

def make_country_radar_single(summary_df, title="Mean Cosine Similarity",
                              value_col="avg_bias_score", order=COUNTRY_ORDER,
                              ylim=(0, 1), radial_ticks=(0.4, 0.6, 0.8, 1.0),
                              save_path=None):
    """
    Plot a single radar (spider) polygon for one summary_df.
    """
    labels = order
    vals = _values_in_order(summary_df, value_col=value_col, order=order)

    N = len(labels)
    base_angles = np.linspace(0, 2 * np.pi, N, endpoint=False)

    # Close the loop
    vals = np.r_[vals, vals[0]]
    angles = np.r_[base_angles, base_angles[0]]

    fig, ax = plt.subplots(figsize=(7.5, 7.5), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.plot(angles, vals, linewidth=2)
    ax.fill(angles, vals, alpha=0.25)

    ax.set_xticks(base_angles)
    ax.set_xticklabels(labels)

    if ylim is not None:
        ax.set_ylim(*ylim)
    if radial_ticks:
        ax.set_yticks(radial_ticks)
        ax.set_yticklabels([f"{t:.2f}" for t in radial_ticks])

    ax.set_title(title, pad=20)

    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches="tight")
    return fig, ax

def make_country_radar_multi(series_dict, title="Bias (avg similarity) by country",
                             value_col="avg_bias_score", order=COUNTRY_ORDER,
                             ylim=(0, 1), radial_ticks=(0.4, 0.6, 0.8, 1.0),
                             show_legend=True, save_path=None):
    """
    Overlay multiple series on the same radar.
    series_dict: {"Native vs Assistant (GPT-4o-mini)": summary_df, "Role vs Assistant (GPT-4o-mini)": summary_df2, ...}
    """
    labels = order
    N = len(labels)
    base_angles = np.linspace(0, 2 * np.pi, N, endpoint=False)

    fig, ax = plt.subplots(figsize=(8.5, 8.5), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    for name, sdf in series_dict.items():
        vals = _values_in_order(sdf, value_col=value_col, order=order)
        vals = np.r_[vals, vals[0]]
        angles = np.r_[base_angles, base_angles[0]]

        ax.plot(angles, vals, linewidth=2, label=name)
        ax.fill(angles, vals, alpha=0.15)

    ax.set_xticks(base_angles)
    ax.set_xticklabels(labels)

    if ylim is not None:
        ax.set_ylim(*ylim)
    if radial_ticks:
        ax.set_yticks(radial_ticks)
        ax.set_yticklabels([f"{t:.2f}" for t in radial_ticks])

    if show_legend:
        ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.15))
    ax.set_title(title, pad=20)

    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches="tight")
    return fig, ax


# ---------- Example usage with your precomputed summary CSV ----------

# Single-series radar from one precomputed summary
summary_path = "results/gpt-4o-mini/similarities_with_double_translation_native_vs_assistant/bias_summary_native_vs_assistant.csv"
summary_df = load_bias_summary(summary_path)

fig, ax = make_country_radar_single(
    summary_df,
    title="Mean Cosine Similarity – Native vs Assistant (GPT-4o-mini)",
    ylim=(0, 1),
    radial_ticks=(0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
    save_path="results/gpt-4o-mini/similarities_with_double_translation_native_vs_assistant/plots/radar_native_vs_assistant.png",
)

# Multi-series example (overlaying multiple precomputed summaries)
# series_paths = {
#     "GPT-4o-mini – Native vs Assistant": "results/.../bias_summary_native_vs_assistant.csv",
#     "GPT-4o-mini – Role vs Assistant":   "results/.../bias_summary_role_vs_assistant.csv",
#     "LLaMA – Native vs Assistant":       "results/.../llama/bias_summary_native_vs_assistant.csv",
# }
# series = {name: load_bias_summary(p) for name, p in series_paths.items()}
# fig, ax = make_country_radar_multi(
#     series,
#     title="Bias (avg similarity) – Comparison across conditions/models",
#     ylim=(0, 1),
#     radial_ticks=(0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
#     save_path="/content/drive/MyDrive/radar_multi.png",
# )
# print("Saved multi-series radar to /content/drive/MyDrive/radar_multi.png")
