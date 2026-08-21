import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("data.csv")

# Inspect the dataset
print("First 5 rows:")
print(df.head())

print("\nDataset information:")
print(df.info())

print("\nMissing values:")
print(df.isnull().sum())

print("\nSummary statistics:")
print(df.describe())

# Clean column names
df.columns = df.columns.str.strip()

# Convert Date to datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Handle missing Date values
df["Date"] = df["Date"].ffill()

# Handle missing Calories values using the median
df["Calories"] = df["Calories"].fillna(df["Calories"].median())

# Remove rows with missing values in important numeric columns
df = df.dropna(subset=["Duration", "Pulse", "Maxpulse"])

# Filter rows
high_pulse = df[df["Pulse"] > 100]

print("\nRows where Pulse is greater than 100:")
print(high_pulse)

# Create new columns
df["Pulse_Difference"] = df["Maxpulse"] - df["Pulse"]
df["Calories_per_Minute"] = df["Calories"] / df["Duration"]

# Create a workout intensity column
df["Intensity"] = pd.cut(
    df["Pulse"],
    bins=[0, 80, 100, float("inf")],
    labels=["Low", "Medium", "High"]
)

# Display cleaned data
print("\nCleaned dataset:")
print(df.head())

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nAverage calories burned:")
print(df["Calories"].mean())

print("\nAverage pulse:")
print(df["Pulse"].mean())

print("\nWorkout intensity counts:")
print(df["Intensity"].value_counts())

# Save cleaned dataset
df.to_csv("week3_cleaned_data.csv", index=False)

# Visualization 1: Duration vs Calories
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="Duration", y="Calories")
plt.title("Duration vs Calories")
plt.xlabel("Duration")
plt.ylabel("Calories")
plt.tight_layout()
plt.show()

# Visualization 2: Pulse distribution
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="Pulse", bins=10, kde=True)
plt.title("Pulse Distribution")
plt.xlabel("Pulse")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Visualization 3: Average calories by intensity
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="Intensity", y="Calories")
plt.title("Average Calories by Workout Intensity")
plt.xlabel("Intensity")
plt.ylabel("Average Calories")
plt.tight_layout()
plt.show()
