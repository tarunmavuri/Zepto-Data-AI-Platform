# Analytics Module 📊

## Overview

This module performs comprehensive data analysis and machine learning on the Titanic dataset. It includes exploratory data analysis (EDA), data cleaning, feature engineering, and building predictive models for passenger survival classification and fare prediction.

## Files

| File | Purpose |
|------|----------|
| `01_eda.py` | Exploratory Data Analysis and data cleaning |
| `02.modeling.py` | Classification and regression model building |
| `titanic.csv` | Original Titanic dataset (reference copy) |
| `titanic_cleaned.csv` | Cleaned dataset output (generated) |
| `README.md` | Module documentation |

## What This Module Does

### 1. Exploratory Data Analysis (`01_eda.py`)

- **Data Loading**: Loads the Titanic dataset from seaborn
- **Dataset Overview**: Prints shape, data types, and statistical summaries
- **Missing Value Analysis**: Calculates missing value percentages for each column
- **Data Cleaning**:
  - Handles missing values for `age`, `embarked`, `embark_town`, and `deck`
  - Uses appropriate imputation strategies (median for age, mode for categorical)
  - Exports cleaned data to `titanic_cleaned.csv`
- **Offline Storage**: Creates a local CSV copy for reproducible analysis

### 2. Modeling and Predictions (`02.modeling.py`)

- **Classification Task**: Predicts passenger survival (binary classification)
  - Handles class imbalance using SMOTE (Synthetic Minority Over-sampling Technique)
  - Compares multiple models: Logistic Regression, Random Forest, Gradient Boosting
  - Evaluates using accuracy, precision, recall, F1-score
  - Persists best model as pipeline for reuse

- **Regression Task**: Predicts fare amounts
  - Builds regression pipelines with feature scaling
  - Evaluates using MSE, RMSE, R² metrics
  - Compares multiple regression algorithms

## How to Run

### Run EDA and Data Cleaning
```bash
python analytics/01_eda.py
```
This will:
- Load and analyze the Titanic dataset
- Print comprehensive statistics and missing value analysis
- Generate `titanic_cleaned.csv`

### Run Modeling
```bash
python analytics/02.modeling.py
```
This will:
- Train classification models for survival prediction
- Train regression models for fare prediction
- Compare model performance
- Save trained pipelines for later use

## Dataset Description

The Titanic dataset includes passenger information such as:
- **Demographic**: Age, Sex, Class
- **Family**: SibSp (siblings/spouses), Parch (parents/children)
- **Fare**: Ticket price
- **Embarked**: Port of embarkation (C=Cherbourg, Q=Queenstown, S=Southampton)
- **Target**: Survived (0=No, 1=Yes)

## Dependencies

Requires packages from the root `requirements.txt`:
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn

Install from project root:
```bash
pip install -r requirements.txt
```

## Output Files

- `titanic_cleaned.csv` - Cleaned dataset ready for further analysis
- Trained model pipelines - Saved during model training for reuse

## Technical Notes

- The module uses scikit-learn pipelines for reproducibility and ease of deployment
- SMOTE is applied only to training data to avoid data leakage
- All numerical features are standardized using StandardScaler
- Models are evaluated using cross-validation for robust performance estimates
- The analytics module is self-contained and doesn't depend on other project modules
