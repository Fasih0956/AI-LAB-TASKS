# LINEAR REGRESSION GAVE MAE 510100 WHICH WAS HIGHER THAN 480811 SO RANDOM FOREST USED.
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor     # BETTER FOR RANDOM DATA + HIGH ACCURACY
from sklearn.metrics import mean_absolute_error, r2_score 

df = pd.read_csv("processed_data.csv")

X = df.drop(['approved', 'approved_loan_amount'], axis=1)
y = df['approved_loan_amount']

df_reg = pd.concat([X, y], axis=1)
df_reg = df_reg.sample(frac=1, random_state=42).reset_index(drop=True)
X = df_reg.drop('approved_loan_amount', axis=1)
y = df_reg['approved_loan_amount']

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
print("REGRESSION MODEL TRAINED (RANDOM FOREST)")

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

# NEGATIVE R2 AND HIGH MAE SUGGEST THAT TARGET IS  NOT DIRECTLY LINKED OR RELATED TO ANY OF THE ATTRIBUTES.