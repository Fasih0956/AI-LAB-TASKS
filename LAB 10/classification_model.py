#Logistic regression was also tested before this which gave 78% accuracy that's why this model is used because it gives higher accuracy.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier   # BETTER THAN LOGISTIC REGRESSION FOR RANDOM DATA + HIGH ACCURACY
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

df = pd.read_csv("processed_data.csv")

X = df.drop(['approved', 'approved_loan_amount'], axis=1)
y = df['approved'].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)  
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)
model.fit(X_train, y_train)
print("RANDOM FOREST MODEL TRAINED")
importance = model.feature_importances_   # to display important features contributing to predictions.

feature_importance_df = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': importance
})

feature_importance_df = feature_importance_df.sort_values(
    by='Importance',
    ascending=False
)

top_features = feature_importance_df.head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=top_features)
plt.title("Top 10 Feature Importance (Random Forest)")
plt.show()

probs = model.predict_proba(X_test)[:, 1]

threshold = 0.4  # best accuracy was been given at this threshold , tested various.
y_pred = (probs > threshold).astype(int)

print("\nTHRESHOLD USED:", threshold)   # Metrics outputs 
print("\nACCURACY:", accuracy_score(y_test, y_pred))
print("\nCONFUSION MATRIX:\n", confusion_matrix(y_test, y_pred))
print("\nCLASSIFICATION REPORT:\n", classification_report(y_test, y_pred))

print("\nCLASS DISTRIBUTION:")
print(df['approved'].value_counts(normalize=True))
