# Analytics Module

## Overview

This module focuses on exploratory data analysis and predictive modeling using the Titanic dataset. It demonstrates how raw tabular data can be cleaned, transformed, and used for both classification and regression tasks.

## Included Files

- `01_eda.py` — data inspection, cleaning, and output generation
- `02.modeling.py` — survival classification and fare regression modeling
- `titanic.csv` — original Titanic dataset
- `titanic_cleaned.csv` — cleaned output dataset
- `README.md` — module documentation

## Workflow

### 1. EDA and Cleaning

`01_eda.py` is responsible for:

- loading the Titanic dataset
- checking shape, dtypes, and summary statistics
- identifying missing values
- imputing missing values for critical columns
- exporting a cleaned dataset to `titanic_cleaned.csv`

### 2. Modeling

`02.modeling.py` covers:

- survival prediction using classification models
- fare prediction using regression models
- class imbalance handling with SMOTE
- model performance comparison and evaluation
- saving the best-performing model pipeline

## Run

From the project root:

```bash
python analytics/01_eda.py
python analytics/02.modeling.py
```

## Dependencies

This module uses packages defined in the project root requirements, especially:

- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- imbalanced-learn
- joblib

Install them with:

```bash
pip install -r requirements.txt
```

## Outputs

- `analytics/titanic_cleaned.csv` — cleaned dataset for repeatable use
- trained model artifacts created during model execution

## Notes

- The analytics workflow is intentionally standalone and does not depend on the support assistant module.
- StandardScaler and pipeline-based model design are used to keep the workflow reproducible and clean.
- The dataset is useful for showing typical classification and feature-engineering steps in an ML project.
