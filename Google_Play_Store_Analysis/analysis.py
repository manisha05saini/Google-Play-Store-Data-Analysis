

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Check whether dataset file exists
file_path = "googleplaystore.csv"

if os.path.exists(file_path):

    # Load dataset
    df = pd.read_csv(file_path)

    # Display first 5 rows
    print("First 5 Rows:")
    print(df.head())

    # Dataset information
    print("\nDataset Shape:")
    print(df.shape)

    # Column names
    print("\nColumn Names:")
    print(df.columns.tolist())

    # Missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

else:
    print("Dataset file not found!")
    print("Please check the dataset folder and CSV filename.")


# STEP 3: DATA CLEANING

print("\n--- DATA CLEANING STARTED ---")

# 1. Remove duplicate records
print("\nDuplicate rows:", df.duplicated().sum())
df = df.drop_duplicates()

# 2. Remove incorrect category record
df = df[df["Category"] != "1.9"].copy()

# 3. Convert columns into numeric format
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")

df["Installs"] = pd.to_numeric(
    df["Installs"].astype(str).str.replace(",", "", regex=False)
    .str.replace("+", "", regex=False),
    errors="coerce"
)

df["Price"] = pd.to_numeric(
    df["Price"].astype(str).str.replace("$", "", regex=False),
    errors="coerce"
)

# 4. Fill missing Rating values with median
df["Rating"] = df["Rating"].fillna(df["Rating"].median())

# 5. Fill other missing values with mode
columns = ["Type", "Content Rating", "Current Ver", "Android Ver"]

for col in columns:
    df[col] = df[col].fillna(df[col].mode()[0])

# 6. Save cleaned dataset
df.to_csv("googleplaystore_cleaned.csv", index=False)

# 7. Display final results
print("\n--- DATA CLEANING COMPLETED ---")
print("Cleaned Dataset Shape:", df.shape)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nCleaned Dataset Saved Successfully!")


# STEP 4: EXPLORATORY DATA ANALYSIS

# Load cleaned dataset
df = pd.read_csv("googleplaystore_cleaned.csv")

sns.set_style("whitegrid")

# Graph 1: Top 10 App Categories
plt.figure(figsize=(12, 6))

top_categories = df["Category"].value_counts().head(10)

sns.barplot(
    x=top_categories.values,
    y=top_categories.index
)

plt.title("Top 10 App Categories")
plt.xlabel("Number of Apps")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig("category_analysis.png")
plt.show()


# Graph 2: Rating Distribution
plt.figure(figsize=(10, 6))

sns.histplot(df["Rating"], bins=20, kde=True)

plt.title("Distribution of App Ratings")
plt.xlabel("App Rating")
plt.ylabel("Number of Apps")
plt.tight_layout()
plt.savefig("rating_distribution.png")
plt.show()


# Graph 3: Free vs Paid Apps
plt.figure(figsize=(7, 7))

type_counts = df["Type"].value_counts()

plt.pie(
    type_counts,
    labels=type_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Free vs Paid Apps")
plt.tight_layout()
plt.savefig("free_vs_paid.png")
plt.show()


# Graph 4: Top 10 Apps by Installs
top_apps = df.sort_values(
    by="Installs",
    ascending=False
).head(10)

plt.figure(figsize=(12, 6))

sns.barplot(
    data=top_apps,
    x="Installs",
    y="App"
)

plt.title("Top 10 Apps by Installs")
plt.xlabel("Number of Installs")
plt.ylabel("App Name")
plt.tight_layout()
plt.savefig("top_installed_apps.png")
plt.show()


print("\nEDA Completed Successfully!")


# STEP 5: DATA ANALYSIS INSIGHTS

print("\n========== PROJECT INSIGHTS ==========")

# 1. Total number of apps
print("\nTotal Apps:", len(df))

# 2. Most popular category by app count
popular_category = df["Category"].value_counts().idxmax()
print("Most Popular Category:", popular_category)

# 3. Average app rating
average_rating = df["Rating"].mean()
print("Average App Rating:", round(average_rating, 2))

# 4. Free and Paid apps count
print("\nFree and Paid Apps:")
print(df["Type"].value_counts())

# 5. Top 5 apps by installs
print("\nTop 5 Apps by Installs:")
print(
    df.sort_values(
        by="Installs",
        ascending=False
    )[["App", "Installs"]].head(5)
)

# 6. Highest rated category
category_rating = df.groupby("Category")["Rating"].mean()
print("\nHighest Average Rating Category:")
print(category_rating.idxmax())

print("\n========== ANALYSIS COMPLETED ==========")

