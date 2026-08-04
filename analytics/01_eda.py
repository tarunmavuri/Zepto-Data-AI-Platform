# ===========================================
#       TITANIC DATA ANALYSIS - PART A
# ===========================================

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import os

# Ignore warning messages
import warnings
warnings.filterwarnings("ignore")

# Make graphs look better
sns.set_style("whitegrid")

# Load dataset from Seaborn
df = sns.load_dataset("titanic")

# Create analytics folder if it doesn't exist
os.makedirs("analytics", exist_ok=True)

# Save a copy for offline use
df.to_csv("analytics/titanic.csv", index=False)

print("Dataset Loaded Successfully!")
print("Offline copy saved as analytics/titanic.csv")

# Basic Information
print("\n========== DATASET SHAPE ==========")
print(df.shape)

print("\n========== DATASET INFO ==========")
df.info()

print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe(include="all"))

# Missing Value Percentage
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

# Create a Copy Before Cleaning
clean_df = df.copy()

# Handle Missing Values
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

# Check Missing Values After Cleaning
print("========== MISSING VALUES AFTER CLEANING ==========")
print(clean_df.isnull().sum())

# Save Cleaned Dataset (Optional)
clean_df.to_csv("analytics/titanic_cleaned.csv", index=False)

print("\nCleaned dataset saved as analytics/titanic_cleaned.csv")

# UNIVARIATE ANALYSIS
print("\n===== UNIVARIATE ANALYSIS =====")
for col in ["age", "fare"]:
    plt.figure(figsize=(6,4))
    sns.histplot(clean_df[col], kde=True)
    plt.title(f"{col.title()} Histogram")
    plt.show()

    plt.figure(figsize=(6,2))
    sns.boxplot(x=clean_df[col])
    plt.title(f"{col.title()} Boxplot")
    plt.show()

    # IQR Outliers
    Q1 = clean_df[col].quantile(0.25)
    Q3 = clean_df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = clean_df[
        (clean_df[col] < lower) |
        (clean_df[col] > upper)
    ]

    print(f"{col.title()} Outliers : {len(outliers)}")

# Fare Statistics
print("\n===== FARE STATISTICS =====")
mean = clean_df["fare"].mean()
median = clean_df["fare"].median()
mode = clean_df["fare"].mode()[0]
print("Mean   :", mean)
print("Median :", median)
print("Mode   :", mode)
if mean > median > mode:
    print("\nInterpretation: Fare is Right-Skewed.")
elif mean < median < mode:
    print("\nInterpretation: Fare is Left-Skewed.")
else:
    print("\nInterpretation: Fare is Approximately Symmetric.")
# BIVARIATE ANALYSIS
print("\n===== SURVIVAL RATE BY SEX =====")
for gender in ["male", "female"]:
    rate = clean_df[clean_df["sex"] == gender]["survived"].mean() * 100
    print(f"{gender.title()} : {rate:.2f}%")

print("\n===== SURVIVAL RATE BY CLASS =====")
for cls in [1,2,3]:
    rate = clean_df[clean_df["pclass"] == cls]["survived"].mean() * 100
    print(f"Class {cls} : {rate:.2f}%")

print("\n===== SURVIVAL RATE BY SEX & CLASS =====")
for gender in ["male","female"]:
    for cls in [1,2,3]:
        rate = clean_df[
            (clean_df["sex"] == gender) &
            (clean_df["pclass"] == cls)
        ]["survived"].mean() * 100

        print(f"{gender.title()} Class {cls} : {rate:.2f}%")

# CORRELATION HEATMAP
cols = ["survived","pclass","age","sibsp","parch","fare"]
corr = clean_df[cols].corr()
plt.figure(figsize=(7,5))
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

# Two strongest correlations
pairs = corr.abs().where(
    np.triu(np.ones(corr.shape),1).astype(bool)
).stack().sort_values(ascending=False)

print("\nTop Two Correlations")
print(pairs.head(2))
print("\nInterpretation:")
print("These are the two strongest relationships among the selected numeric features.")
print("Higher absolute correlation means a stronger linear relationship.")

# MULTIVARIATE DATA STORY
# Chart 1
sns.barplot(data=clean_df, x="sex", y="survived")
plt.title("Survival by Sex")
plt.tight_layout()
plt.show()
print("Female passengers had a much higher survival rate than males.")
print("This suggests that gender played an important role during rescue operations.\n")
# Chart 2
sns.barplot(data=clean_df, x="pclass", y="survived")
plt.title("Survival by Class")
plt.tight_layout()
plt.show()
print("First-class passengers had the highest survival rate.")
print("Passengers in lower classes faced lower survival, showing that passenger class influenced rescue chances.\n")
# Chart 3
sns.boxplot(data=clean_df, x="survived", y="age")
plt.title("Age vs Survival")
plt.tight_layout()
plt.show()
print("Children generally had slightly better survival chances than older passengers.")
print("The age distribution suggests younger passengers received some priority during evacuation.\n")
# Chart 4
sns.boxplot(data=clean_df, x="survived", y="fare")
plt.title("Fare vs Survival")
plt.tight_layout()
plt.show()

print("Passengers paying higher fares survived more often.")
print("Higher fares are associated with higher passenger class, which may have improved access to lifeboats.\n")

# STANDARDIZATION (EDA ONLY)
print("\n===== STANDARDIZATION =====")
print("Before Scaling")
print(clean_df[["age","fare"]].agg(["mean","std"]))
scaler = StandardScaler()
scaled = scaler.fit_transform(clean_df[["age","fare"]])
scaled_df = pd.DataFrame(
    scaled,
    columns=["Age_Z","Fare_Z"]
)

print("\nAfter Scaling")
print(scaled_df.agg(["mean","std"]))
plt.figure(figsize=(6,4))
sns.histplot(scaled_df["Age_Z"], kde=True, label="Age")
sns.histplot(scaled_df["Fare_Z"], kde=True, label="Fare")
plt.legend()
plt.show()

print("\nBoth columns now have approximately mean = 0 and std = 1.")