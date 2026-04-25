import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_csv("cleaned_data.csv")
target_cols = ['approved', 'approved_loan_amount']
categorical_cols = [    #for encoding categorical attributes 
    col for col in df.select_dtypes(include=['object', 'string']).columns
    if col not in target_cols
]
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore') #OneHotEncoder is more efficient than LabelEncoder
encoded_data = encoder.fit_transform(df[categorical_cols])
encoded_df = pd.DataFrame(
    encoded_data,
    columns=encoder.get_feature_names_out(categorical_cols)
)
df = df.drop(categorical_cols, axis=1)
df = pd.concat([df, encoded_df], axis=1)
feature_cols = [col for col in df.columns if col not in target_cols]

scaler = StandardScaler()   #Scaling values
df[feature_cols] = scaler.fit_transform(df[feature_cols])
df.to_csv("processed_data.csv", index=False)  #final file for models to train

print("ENCODING + SCALING DONE.")