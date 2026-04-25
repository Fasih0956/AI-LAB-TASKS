import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

df = pd.read_csv("processed_data.csv")

n_approved = len(df[df['approved'] == 1])
n_rejected = len(df[df['approved'] == 0])
n_samples = min(n_approved, n_rejected, 500)

print(f"Approved: {n_approved}, Rejected: {n_rejected} → Using {n_samples} each")   # 397 approved cases only not 500 so 397 used from not approved

df_balanced = pd.concat([
    df[df['approved'] == 0].sample(n_samples, random_state=42),
    df[df['approved'] == 1].sample(n_samples, random_state=42)
])
df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

X = df_balanced.drop(['approved', 'approved_loan_amount'], axis=1)
y = df_balanced['approved']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(   # same model used for accurate comparison
    n_estimators=200,   
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)
print("\nRANDOM FOREST TRAINED")

probs = model.predict_proba(X_test)[:, 1]
y_pred = model.predict(X_test)

print("\nACCURACY:", accuracy_score(y_test, y_pred))
print("\nCONFUSION MATRIX:\n", confusion_matrix(y_test, y_pred))
print("\nCLASSIFICATION REPORT:\n", classification_report(y_test, y_pred))
print("\nCLASS DISTRIBUTION:")
print(df_balanced['approved'].value_counts(normalize=True))

# it gives 87% accuracy i.e better than unbalanced data which is pretty high for prediction models.