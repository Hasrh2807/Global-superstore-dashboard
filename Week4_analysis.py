"""
Week 4 Capstone — End-to-End Sales Analysis
Data Analyst Course

Pipeline:
  1. Load & clean the raw dataset (pandas)
  2. Explore structure, nulls, types
  3. Analyze key business metrics (segment, product, country, discount, time)
  4. Export cleaned data + summary tables for Excel / Power BI / Tableau
"""

import pandas as pd

# ---------------------------------------------------------------
# 1. LOAD & CLEAN
# ---------------------------------------------------------------
SRC = "Sample_data.xlsx"          # original raw file
OUT_CSV = "cleaned_sales_data.csv"

df = pd.read_excel(SRC)
df.columns = [c.strip() for c in df.columns]   # strip stray whitespace (" Sales")

# Discount Band is blank when no discount was applied -> label explicitly
df["Discount Band"] = df["Discount Band"].fillna("None")

# Derived metric used throughout the analysis
df["Profit Margin %"] = (df["Profit"] / df["Sales"] * 100).round(2)

assert df.isnull().sum().sum() == 0, "Unexpected nulls remain after cleaning"
df.to_csv(OUT_CSV, index=False)

# ---------------------------------------------------------------
# 2. EXPLORE
# ---------------------------------------------------------------
print("Shape:", df.shape)
print(df.dtypes)
print(df.describe(include="all"))

# ---------------------------------------------------------------
# 3. KEY METRICS
# ---------------------------------------------------------------
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
overall_margin = total_profit / total_sales * 100
print(f"\nTotal Sales:  ${total_sales:,.0f}")
print(f"Total Profit: ${total_profit:,.0f}")
print(f"Overall Margin: {overall_margin:.1f}%")

by_segment = (
    df.groupby("Segment")
      .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
      .assign(Margin_Pct=lambda x: x.Profit / x.Sales * 100)
      .sort_values("Sales", ascending=False)
)
print("\n=== By Segment ===\n", by_segment)

by_product = (
    df.groupby("Product")
      .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
      .assign(Margin_Pct=lambda x: x.Profit / x.Sales * 100)
      .sort_values("Sales", ascending=False)
)
print("\n=== By Product ===\n", by_product)

by_country = (
    df.groupby("Country")
      .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
      .assign(Margin_Pct=lambda x: x.Profit / x.Sales * 100)
      .sort_values("Sales", ascending=False)
)
print("\n=== By Country ===\n", by_country)

monthly = (
    df.groupby(["Year", "Month Number", "Month Name"])
      .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
      .reset_index()
      .sort_values(["Year", "Month Number"])
)
print("\n=== Monthly Trend ===\n", monthly)

discount_impact = (
    df.groupby("Discount Band")
      .agg(Avg_Sales=("Sales", "mean"), Avg_Profit=("Profit", "mean"),
           Avg_Margin_Pct=("Profit Margin %", "mean"))
)
print("\n=== Discount Band Impact ===\n", discount_impact)

# ---------------------------------------------------------------
# 4. FLAG: Enterprise segment loss driver (key finding)
# ---------------------------------------------------------------
enterprise = df[df["Segment"] == "Enterprise"]
print("\nEnterprise segment margin: "
      f"{enterprise['Profit'].sum() / enterprise['Sales'].sum() * 100:.1f}%")
print("Enterprise COGS-to-Sales ratio: "
      f"{enterprise['COGS'].sum() / enterprise['Sales'].sum() * 100:.1f}%")
print("Overall COGS-to-Sales ratio:    "
      f"{df['COGS'].sum() / df['Sales'].sum() * 100:.1f}%")

# ---------------------------------------------------------------
# 5. EXPORT SUMMARY TABLES (for Power BI / Tableau / Excel import)
# ---------------------------------------------------------------
with pd.ExcelWriter("summary_tables.xlsx") as writer:
    by_segment.to_excel(writer, sheet_name="By Segment")
    by_product.to_excel(writer, sheet_name="By Product")
    by_country.to_excel(writer, sheet_name="By Country")
    monthly.to_excel(writer, sheet_name="Monthly Trend", index=False)
    discount_impact.to_excel(writer, sheet_name="Discount Impact")

print("\nDone. Cleaned data -> cleaned_sales_data.csv | Summaries -> summary_tables.xlsx")
