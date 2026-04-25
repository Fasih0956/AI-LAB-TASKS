import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

df = pd.read_csv("processed_data.csv")

n_samples = 397   # FROM CLASSIFICATION WE KNOW APPROVED = 397
df_balanced = df.sample(n=2*n_samples, random_state=42).reset_index(drop=True)

X = df_balanced.drop(['approved', 'approved_loan_amount'], axis=1)
y = df_balanced['approved_loan_amount']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

print("REGRESSION MODEL TRAINED (BALANCED SAMPLE)")

importance = model.feature_importances_

feature_importance_df = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': importance
})

feature_importance_df = feature_importance_df.sort_values(
    by='Importance',
    ascending=False
)

top_features = feature_importance_df.head(10)

print(top_features)
plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=top_features)
plt.title("TOP 10 Important Features (Random Forest Regressor)")
plt.show()

y_pred = model.predict(X_test)

print("\nMAE:", mean_absolute_error(y_test, y_pred))
print("R2 SCORE:", r2_score(y_test, y_pred))

# IT PERFORMS EVEN WORST THAN UNBALANCED DATA DUE TO HIGH MAE AND A MORE NEGATIVE R2 SCORE