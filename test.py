import os
from cleaner import clean_dataset

df = clean_dataset(r"D:\test\atvc_members.xlsx")
print("Cleaned Data Preview:")
print(df.head())

os.makedirs("cleaned_data", exist_ok=True)

df.to_csv("cleaned_data/cleaned_sample.csv", index=False)
