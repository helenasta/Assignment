import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# --- 1. Load cleaned data ---
df = pd.read_csv("data/generated/10k_cleaned.csv")

# --- 2. Sample description table ---
summary = df.groupby("year").agg(
    n_filings=("word_count", "count"),
    mean_words=("word_count", "mean"),
    median_words=("word_count", "median"),
    q1_words=("word_count", lambda x: x.quantile(0.25)),
    q3_words=("word_count", lambda x: x.quantile(0.75)),
).reset_index()

summary.to_csv("output/sample_by_year.csv", index=False)

# --- 3. Figure 1 Panel A: Word count over time ---
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(summary["year"], summary["median_words"], 
        label="Median", color="black", linewidth=2)
ax.plot(summary["year"], summary["q1_words"],  
        label="25th Percentile", color="black", 
        linewidth=1.5, linestyle="--")
ax.plot(summary["year"], summary["q3_words"],  
        label="75th Percentile", color="black", 
        linewidth=1.5, linestyle=":")

ax.set_xlabel("Year")
ax.set_ylabel("Number of Words")
ax.set_title("Figure 1, Panel A: 10-K Length Over Time")
ax.legend()
ax.set_ylim(0, None)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f"{int(x):,}"))
ax.set_xticks(summary["year"].unique())
ax.tick_params(axis="x", rotation=45)

plt.tight_layout()
plt.savefig("output/fig1_panel_a.pdf")
plt.savefig("output/fig1_panel_a.png", dpi=150)
plt.close()

print("Done. Outputs saved to output/")