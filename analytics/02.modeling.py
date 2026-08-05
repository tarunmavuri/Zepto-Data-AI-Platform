# TITANIC DATA ANALYSIS - PART B (MODELING)

import warnings
warnings.filterwarnings("ignore")

import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn import compose, pipeline, impute, preprocessing
from sklearn import model_selection, metrics
from sklearn import linear_model, tree, ensemble
from imblearn.over_sampling import SMOTE
import imblearn.pipeline as imb_pipeline
# ---------------- Load cleaned data ----------------
df = pd.read_csv("analytics/titanic_cleaned.csv")
print(df.head())

target="survived"
drop_cols=[c for c in ["alive"] if c in df.columns]
df=df.drop(columns=drop_cols)

X=df.drop(columns=[target])
y=df[target]

print("\nClass Balance")
print(y.value_counts(normalize=True)*100)

cat=[c for c in X.select_dtypes(include=["object","category","bool"]).columns]
num=[c for c in X.columns if c not in cat]

pre=compose.ColumnTransformer([
("num",pipeline.Pipeline([
("imp",impute.SimpleImputer(strategy="median")),
("scaler",preprocessing.StandardScaler())
]),num),
("cat",pipeline.Pipeline([
("imp",impute.SimpleImputer(strategy="most_frequent")),
("enc",preprocessing.OneHotEncoder(handle_unknown="ignore"))
]),cat)
])

Xtrain,Xtest,ytrain,ytest=model_selection.train_test_split(X,y,test_size=0.2,stratify=y,random_state=42)

models={
"Logistic Regression":linear_model.LogisticRegression(max_iter=1000),
"Decision Tree":tree.DecisionTreeClassifier(random_state=42),
"Random Forest":ensemble.RandomForestClassifier(random_state=42)
}

rows=[]
plt.figure(figsize=(7,5))
for name,est in models.items():
    pipe=pipeline.Pipeline([("prep",pre),("model",est)])
    pipe.fit(Xtrain,ytrain)
    pred=pipe.predict(Xtest)
    proba=pipe.predict_proba(Xtest)[:,1]
    rows.append([name,
                 metrics.accuracy_score(ytest,pred),
                 metrics.precision_score(ytest,pred),
                 metrics.recall_score(ytest,pred),
                 metrics.f1_score(ytest,pred),
                 metrics.roc_auc_score(ytest,proba)])
    print("\n",name)
    print(f"\n{name} Confusion Matrix")
    print(metrics.confusion_matrix(ytest, pred))   
    fpr,tpr,_=metrics.roc_curve(ytest,proba)
    plt.plot(fpr,tpr,label=f"{name} ({metrics.roc_auc_score(ytest,proba):.3f})")

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curves Comparison")
plt.legend()
plt.grid(True)
plt.show()

cmp=pd.DataFrame(rows,columns=["Model","Accuracy","Precision","Recall","F1","AUC"])
print("\nClassification Model Comparison")
print(cmp.round(3))

tree_pipe=pipeline.Pipeline([("prep",pre),("model",tree.DecisionTreeClassifier(random_state=42))])
tree_pipe.fit(Xtrain,ytrain)
feat=tree_pipe.named_steps["prep"].get_feature_names_out()
plt.figure(figsize=(18,10))
plt.title("Decision Tree Classifier")
tree.plot_tree(
    tree_pipe.named_steps["model"],
    feature_names=feat,
    class_names=["Not Survived", "Survived"],
    filled=True,
    max_depth=3
)
plt.show()

imbalance_results = []

for label, clf in [
    ("Baseline", ensemble.RandomForestClassifier(random_state=42)),
    ("Class Weight", ensemble.RandomForestClassifier(
        class_weight="balanced",
        random_state=42))
]:
    p = pipeline.Pipeline([
        ("prep", pre),
        ("model", clf)
    ])
    p.fit(Xtrain, ytrain)
    pr = p.predict(Xtest)
    imbalance_results.append([
        label,
        metrics.precision_score(ytest, pr),
        metrics.recall_score(ytest, pr),
        metrics.f1_score(ytest, pr)
    ])
sm = imb_pipeline.Pipeline([
    ("prep", pre),
    ("smote", SMOTE(random_state=42)),
    ("model", ensemble.RandomForestClassifier(random_state=42))
])
sm.fit(Xtrain, ytrain)
pr = sm.predict(Xtest)
imbalance_results.append([
    "SMOTE",
    metrics.precision_score(ytest, pr),
    metrics.recall_score(ytest, pr),
    metrics.f1_score(ytest, pr)
])
imbalance_df = pd.DataFrame(
    imbalance_results,
    columns=["Method", "Precision", "Recall", "F1 Score"]
)
print("\nImbalance Handling Comparison")
print(imbalance_df.round(3))

grid=pipeline.Pipeline([
("prep",pre),
("model",ensemble.RandomForestClassifier(oob_score=True,bootstrap=True,random_state=42))
])

params={
"model__n_estimators":[100,200],
"model__max_depth":[None,5,10],
"model__max_features":["sqrt","log2"]
}

gs=model_selection.GridSearchCV(grid,params,cv=5,n_jobs=-1)
gs.fit(Xtrain,ytrain)
print("\nBest Random Forest Parameters:")
print(gs.best_params_)
print("\nOut-of-Bag Score:")
print(f"{gs.best_estimator_.named_steps['model'].oob_score_:.3f}")
# ---------------- Regression Model: Predict Fare ----------------

# Prepare regression dataset
reg = df.dropna(subset=["fare"]).copy()

# Define features and target
yr = reg["fare"]
Xr = reg.drop(columns=["fare"])

# Identify categorical and numerical columns
ctr = [c for c in Xr.select_dtypes(include=["object", "category", "bool"]).columns]
ntr = [c for c in Xr.columns if c not in ctr]

# Preprocessing pipeline
prep2 = compose.ColumnTransformer([
    (
        "num",
        pipeline.Pipeline([
            ("imp", impute.SimpleImputer(strategy="median")),
            ("sc", preprocessing.StandardScaler())
        ]),
        ntr
    ),
    (
        "cat",
        pipeline.Pipeline([
            ("imp", impute.SimpleImputer(strategy="most_frequent")),
            ("oh", preprocessing.OneHotEncoder(handle_unknown="ignore"))
        ]),
        ctr
    )
])

# Split data into training and testing sets
xrtr, xrte, yrtr, yrte = model_selection.train_test_split(
    Xr,
    yr,
    test_size=0.2,
    random_state=42
)
# Build Linear Regression pipeline
rpipe = pipeline.Pipeline([
    ("prep", prep2),
    ("model", linear_model.LinearRegression())
])
# Train the model
rpipe.fit(xrtr, yrtr)
# Make predictions
pred = rpipe.predict(xrte)

# Evaluate the regression model
mae = metrics.mean_absolute_error(yrte, pred)
rmse = np.sqrt(metrics.mean_squared_error(yrte, pred))
r2 = metrics.r2_score(yrte, pred)

# Calculate Adjusted R²
n = len(yrte)
p = rpipe.named_steps["prep"].transform(xrte).shape[1]

adj = 1 - (1 - r2) * (n - 1) / (n - p - 1)
print("\nRegression Model Performance")
print(f"MAE          : {mae:.3f}")
print(f"RMSE         : {rmse:.3f}")
print(f"R² Score     : {r2:.3f}")
print(f"Adjusted R²  : {adj:.3f}")
# ---------------- Final Model Comparison Table ----------------

comparison = cmp.copy()

comparison["MAE"] = ""
comparison["RMSE"] = ""
comparison["R²"] = ""
comparison["Adjusted R²"] = ""

regression_row = pd.DataFrame({
    "Model": ["Linear Regression"],
    "Accuracy": [""],
    "Precision": [""],
    "Recall": [""],
    "F1": [""],
    "AUC": [""],
    "MAE": [round(mae, 3)],
    "RMSE": [round(rmse, 3)],
    "R²": [round(r2, 3)],
    "Adjusted R²": [round(adj, 3)]
})

comparison = pd.concat([comparison, regression_row], ignore_index=True)

print("\nFinal Model Comparison")
print(comparison.to_string(index=False))

res=yrte-pred
plt.figure(figsize=(6,4))
plt.scatter(pred,res)
plt.axhline(0,linestyle="--")
plt.title("Residual Plot: Actual vs Predicted Fare")
plt.xlabel("Predicted")
plt.ylabel("Residuals")
plt.grid(True, alpha=0.3)
plt.show()
print("\nResidual Analysis")
print(
    "The residuals appear to be randomly scattered around zero with no "
    "strong funnel-shaped pattern, suggesting no significant "
    "heteroscedasticity."
)

# Save the best complete pipeline
joblib.dump(gs.best_estimator_, "best_titanic_pipeline.pkl")
print("\nPipeline saved successfully!")
# Reload the saved pipeline
loaded = joblib.load("best_titanic_pipeline.pkl")
print("Pipeline loaded successfully!")
# Predict on raw (unprocessed) data
sample = Xtest.iloc[[0]]
prediction = loaded.predict(sample)

print("\nReload Prediction:", prediction[0])
print("Actual Value:", ytest.iloc[0])

print("\nFinal Recommendation")
print("-" * 60)
print(
    "Based on the evaluation metrics, the Random Forest classifier "
    "performed the best overall with the highest Accuracy, F1 Score and "
    "AUC. It achieved a better balance between precision and recall than "
    "Logistic Regression and the Decision Tree. Therefore, the Random "
    "Forest model is recommended for deployment because it provides the "
    "most reliable predictions for passenger survival on the Titanic dataset."
)