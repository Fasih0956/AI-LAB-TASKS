import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("cleaned_data.csv")

#Used to visualize effect of attribute on target to drop attributes
#for categorical
'''sns.countplot(x='age', hue='approved_loan_amount', data=df)
plt.title("Age vs Approved_loan_amount")
plt.show()'''

#for numeric
'''sns.lineplot(x='capital_loss', y='approved_loan_amount', data=df)
plt.title("Age vs Approved_loan_amount")
plt.show()
sns.scatterplot(x='age', y='approved_loan_amount', data=df)
plt.title("Age vs Approved_loan_amount")
plt.show()'''

#used to visulaize outliers to drop outlying values
'''sns.boxplot(y=df['age'])
plt.show()'''

#used to check skewed data
'''sns.histplot(df['age'], kde=True)
plt.show()'''

#graphs as required
df['gender'].value_counts().plot(kind='bar')
plt.title("Gender Distribution")
plt.show()

df['approved'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title("Approval Ratio")
plt.show()

sns.boxplot(x=df['hours_per_week_log'])
plt.title("Box Plot for Hours_per_week")
plt.show()

sns.scatterplot(x='age' , y = 'approved'  ,data=df)
plt.show()

df.columns = df.columns.str.strip() #removing spaces

# Correlation heatmap only for numeric columns
numeric_df = df.select_dtypes(include=['int64', 'float64'])

plt.figure(figsize=(10,6))
sns.heatmap(numeric_df.corr(), annot=True)
plt.title("Correlation Heatmap")
plt.show()

print("\nGRAPH VISUALIZATION SUCCESS !")

#After visualizing it is clear that approved_loan_amount has no direct relation with any attribute and data is mostly random.