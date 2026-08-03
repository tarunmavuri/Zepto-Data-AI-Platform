# ===========================================
#       TITANIC DATA ANALYSIS - PART A
# ===========================================

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

# Ignore warning messages
import warnings
warnings.filterwarnings("ignore")

# Make graphs look better
sns.set_style("whitegrid")

# ===========================================
# Load Titanic Dataset (Load ONLY ONCE)
# ===========================================

# Load dataset from Seaborn
df = sns.load_dataset("titanic")

# Save a copy for offline use
df.to_csv("analytics/titanic.csv", index=False)

print("Dataset Loaded Successfully!")
print("Offline copy saved as analytics/titanic.csv")

# ===========================================
# Basic Information
# ===========================================

print("\n========== DATASET SHAPE ==========")
print(df.shape)

print("\n========== DATASET INFO ==========")
df.info()

print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe(include="all"))

# ===========================================
# Missing Value Percentage
# ===========================================

print("\n========== MISSING VALUE PERCENTAGE ==========")

missing_found = False

for column in df.columns:

    missing = df[column].isnull().sum()

    if missing > 0:

        percent = (missing / len(df)) * 100

        print(f"{column} : {percent:.2f}%")

        missing_found = True

if not missing_found:
    print("No missing values found.")

# ===========================================
# Create a Copy Before Cleaning
# ===========================================

clean_df = df.copy()

# ===========================================
# Handle Missing Values
# ===========================================

print("\n========== CLEANING DATA ==========")

# AGE
# Missing values are between 5% and 30%
# Fill missing values using median

age_missing = clean_df["age"].isnull().mean() * 100
print(f"Age Missing : {age_missing:.2f}%")
print("Strategy : Median Imputation\n")

clean_df["age"] = clean_df["age"].fillna(clean_df["age"].median())


# EMBARKED
# Missing values are less than 5%
# Drop rows containing missing values

embarked_missing = clean_df["embarked"].isnull().mean() * 100
print(f"Embarked Missing : {embarked_missing:.2f}%")
print("Strategy : Drop Rows\n")

clean_df = clean_df.dropna(subset=["embarked"])


# EMBARK_TOWN
# Missing values are less than 5%
# Drop rows containing missing values

embarktown_missing = clean_df["embark_town"].isnull().mean() * 100
print(f"Embark Town Missing : {embarktown_missing:.2f}%")
print("Strategy : Drop Rows\n")

clean_df = clean_df.dropna(subset=["embark_town"])


# DECK
# More than 30% missing values
# Too many values are missing, so drop the column.

deck_missing = clean_df["deck"].isnull().mean() * 100
print(f"Deck Missing : {deck_missing:.2f}%")
print("Strategy : Drop Column (Too many missing values)\n")

clean_df = clean_df.drop(columns=["deck"])
# ===========================================
# Check Missing Values After Cleaning
# ===========================================

print("========== MISSING VALUES AFTER CLEANING ==========")

print(clean_df.isnull().sum())

# ===========================================
# Save Cleaned Dataset (Optional)
# ===========================================

clean_df.to_csv("analytics/titanic_cleaned.csv", index=False)

print("\nCleaned dataset saved as analytics/titanic_cleaned.csv")