import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the cleaned data
df = pd.read_csv("cleaned_data/cleaned_sample.csv")

# Set Seaborn theme
sns.set_theme(style="whitegrid")

# Analyze and plot each column
for col in df.columns:
    plt.figure(figsize=(8, 5))
    if df[col].dtype == 'object':
        if df[col].nunique() < 20:
            sns.countplot(data=df, x=col)
            plt.title(f"Countplot of {col}")
        else:
            continue
    elif pd.api.types.is_numeric_dtype(df[col]):
        sns.histplot(df[col], kde=True)
        plt.title(f"Histogram of {col}")
    elif pd.api.types.is_datetime64_any_dtype(df[col]):
        try:
            df_sorted = df.sort_values(col)
            sns.lineplot(x=df_sorted[col], y=df_sorted[df.columns[1]])
            plt.title(f"Line Chart over Time for {col}")
        except Exception as e:
            print(f"Could not plot {col}: {e}")
            continue
    else:
        continue

    plt.tight_layout()
    if not os.path.exists("graphs"):
        os.makedirs("graphs")
    plt.savefig(f"graphs/{col}_plot.png")
    plt.close()

