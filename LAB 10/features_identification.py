import pandas as pd
df = pd.read_csv("bank_data.csv" , low_memory = False)
target_classification = "Approved"
target_regression = "Approved_loan_amount"

numeric_features = df.select_dtypes(include=['int64','float64']).columns
categorical_features = df.select_dtypes(include=['object' , 'string']).columns

print("\nNUMERIC:", numeric_features)
print("\nCATEGORICAL:", categorical_features)
print("\nTARGET CLASSIFICATION:", target_classification)
print("\nTARGET REGRESSION:",target_regression)
print("\n")


