# Analytics Module

This module contains Titanic dataset analysis and basic data cleaning.

## Files
- `01_eda.py`: EDA and cleaning script for the Titanic dataset
- `titanic.csv`: local Titanic dataset copy used by the analysis
- `titanic_cleaned.csv`: cleaned version of the Titanic dataset (if generated)

## What it does
- Loads `analytics/titanic.csv` from the local analytics folder
- Prints dataset shape and summary statistics
- Computes missing-value percentages for each column
- Handles missing values for `age`, `embarked`, `embark_town`, and `deck`

## Run
```bash
python analytics/01_eda.py
```

## Requirements
Install the project dependencies from the root:

```bash
pip install -r requirements.txt
```

## Notes
- The analytics module is self-contained and uses the local Titanic dataset copy.
- If you add new analytics scripts, place them in the `analytics/` folder and document them here.
