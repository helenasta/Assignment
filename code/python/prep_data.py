import pandas as pd

# --- 1. Load raw data ---
df = pd.read_csv("data/external/10k_word_counts.csv")

# --- 2. Parse dates ---
df["filing_date"] = pd.to_datetime(df["filing_date"], errors="coerce")
df["report_date"] = pd.to_datetime(df["report_date"], errors="coerce")

# Extract fiscal year from report_date
df["year"] = df["report_date"].dt.year

# --- 3. Sample selection ---

# Keep only successful downloads
df = df[df["download_success"] == True]

# Drop filings before June 1, 1996 (voluntary EDGAR period)
df = df[df["filing_date"] >= "1996-06-01"]

# Keep only years from 2000 onwards (sufficient EDGAR coverage)
df = df[df["year"] >= 2000]

# Exclude 2026 as the year is not yet complete
df = df[df["year"] <= 2025]

# Drop filings with fewer than 3,000 words (following Dyer et al.)
df = df[df["word_count"] >= 3000]

# Drop missing word counts or years
df = df.dropna(subset=["word_count", "year"])

# Drop duplicate filings: keep one filing per firm (cik) per year
# (keep the latest filing if multiple exist)
df = df.sort_values("filing_date")
df = df.drop_duplicates(subset=["cik", "year"], keep="last")

# --- 4. Save cleaned data ---
df.to_csv("data/generated/10k_cleaned.csv", index=False)

print(f"Final sample: {len(df)} firm-years, {df['cik'].nunique()} unique firms")
print(f"Years covered: {int(df['year'].min())} to {int(df['year'].max())}")

print(df.groupby("year")["cik"].count())