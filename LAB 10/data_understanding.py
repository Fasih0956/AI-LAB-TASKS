import pandas as pd
df = pd.read_csv("bank_data.csv" , low_memory = False)

print("===== DATA SHAPE =====")
print(df.shape)

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== SUMMARY STATISTICS =====")
print(df.describe(include='all'))

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())