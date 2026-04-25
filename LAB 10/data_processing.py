import pandas as pd
import numpy as np  
df = pd.read_csv("bank_data.csv",low_memory=False)

if 'date_of_birth' in df.columns:  #DOB converted to meaningful attribute i.e age
    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])
    df['age'] = 2026 - df['date_of_birth'].dt.year
    df = df.drop('date_of_birth', axis=1)
print("AGE FEATURE CREATED.")

df['has_capital_loss'] = (df['capital_loss'] > 0).astype(int)  #capital loss converted to meaningful attribute i.e has_capital_loss
df = df.drop('capital_loss', axis=1)
print("HAS LOSS FEATURE CREATED.")

code_columns = ['education_num']  #converted datattype from str to numeric for median
for col in code_columns:
    if col in df.columns:
        # Convert to numeric, coerce errors to NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Missing values
# Numeric attributes - using median/mean
df['education_num'] = df['education_num'].fillna(df['education_num'].median())
df['capital_gain'] = df['capital_gain'].fillna(df['capital_gain'].median())
df['has_capital_loss'] = df['has_capital_loss'].fillna(df['has_capital_loss'].mode()[0])
df['hours_per_week'] = df['hours_per_week'].fillna(df['hours_per_week'].median())
df['inquiry_purpose_code'] = df['inquiry_purpose_code'].fillna(df['inquiry_purpose_code'].median())
df['account_type'] = df['account_type'].fillna(df['account_type'].median())
df['asset_code'] = df['asset_code'].fillna(df['asset_code'].median())
df['age'] = df['age'].fillna(df['age'].mean())  #bell shaped histogram

# Categorical attributes - using mode
df['user_id'] = df['user_id'].fillna(df['user_id'].mode()[0])
df['gender'] = df['gender'].fillna(df['gender'].mode()[0])
df['workclass'] = df['workclass'].fillna(df['workclass'].mode()[0])
df['education_level'] = df['education_level'].fillna(df['education_level'].mode()[0])
df['marital_status'] = df['marital_status'].fillna(df['marital_status'].mode()[0])
df['occupation'] = df['occupation'].fillna(df['occupation'].mode()[0])
df['relationship'] = df['relationship'].fillna(df['relationship'].mode()[0])
df['address'] = df['address'].fillna(df['address'].mode()[0])
df['email'] = df['email'].fillna(df['email'].mode()[0])
df['institute_type'] = df['institute_type'].fillna(df['institute_type'].mode()[0])
df['asset_class_cd'] = df['asset_class_cd'].fillna(df['asset_class_cd'].mode()[0])
df['portfolio_type'] = df['portfolio_type'].fillna(df['portfolio_type'].mode()[0])

# Remove duplicates
df = df.drop_duplicates()

# Remove invalid values
df = df[(df['age'] >= 18) & (df['age'] <= 100)]  # Working age adults
df = df[(df['hours_per_week'] >= 1) & (df['hours_per_week'] <= 168)]  # Max 24*7=168 hours
df = df[df['capital_gain'] >= 0]
df = df[(df['education_num'] >= 1) & (df['education_num'] <= 20)]
invalid_gender = ['?', 'Unknown', 'Other', 'NaN', 'null', 'None']
df = df[~df['gender'].isin(invalid_gender)]
invalid_workclass = ['?', 'Never-worked', 'Without-pay', 'NaN']
df = df[~df['workclass'].isin(invalid_workclass)]
critical_cols = ['occupation', 'education_level', 'marital_status']
for col in critical_cols:
    df = df[~df[col].isin(['?', 'Unknown', 'NaN', 'null', 'None'])]

# Drop irrelevant columns (not relevant / redunndant )
df = df.drop('user_id', axis=1)
df = df.drop('email', axis=1)
df = df.drop('address', axis=1)
df = df.drop('education_level', axis=1)
df = df.drop('asset_code', axis=1)
df = df.drop('capital_gain', axis=1)

num_cols = ['age', 'account_type', 'hours_per_week' ,'education_num']  #dropping outliers

for col in num_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    df = df[(df[col] >= lower) & (df[col] <= upper)]

df = df.dropna(subset=['approved'])   #dropping null values from target columns
df = df.dropna(subset=['approved_loan_amount'])

df['hours_per_week_log'] = np.log1p(df['hours_per_week'])  #fixes skewness
df=df.drop('hours_per_week',axis = 1)
df['inquiry_purpose_code_log'] = np.log1p(df['inquiry_purpose_code'])  #fixes skewness
df=df.drop('inquiry_purpose_code',axis = 1)
df['account_type_log'] = np.log1p(df['account_type'])  #fixes skewness
df=df.drop('account_type',axis = 1)


df.to_csv("cleaned_data.csv", index=False)
print("CLEANING DONE")