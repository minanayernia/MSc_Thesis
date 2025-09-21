import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def plot_similarity_summary(csv_path, outdir, title, fname_prefix, xlim=(0.4, 0.9)):

    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)
    if not {"country","avg_bias_score","bias_std"}.issubset(df.columns):
        raise ValueError("CSV must have columns: country, avg_bias_score, bias_std")

    # Sort countries by mean similarity
    df = df.sort_values("avg_bias_score", ascending=True)

    plt.figure(figsize=(7.2, 5.2))
    y = np.arange(len(df))
    plt.barh(
        y, df["avg_bias_score"],
        xerr=df["bias_std"],
        height=0.6,
        color="#4c78a8",
        edgecolor="black",
        linewidth=0.5
    )
    plt.yticks(y, df["country"])
    plt.xlabel("Mean cosine similarity (± std)")
    plt.xlim(xlim)
    plt.title(title)
    plt.grid(axis="x", linestyle="--", alpha=0.3)

    # Save
    png_path = outdir / f"{fname_prefix}.png"
    pdf_path = outdir / f"{fname_prefix}.pdf"
    plt.tight_layout()
    plt.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.savefig(pdf_path, bbox_inches="tight")
    plt.close()
    print(f"Saved summary plot to:\n- {png_path}\n- {pdf_path}")

plot_similarity_summary(
    csv_path="results/llama3.1-70b/similarities_with_double_translation_native_vs_assistant/bias_summary_native_vs_assistant.csv",
    outdir="results/llama3.1-70b/similarities_with_double_translation_native_vs_assistant/plots",
    title="LLaMA 3.1-70B: Native vs. Assistant Similarities",
    fname_prefix="native_vs_assistant_summary",
)
