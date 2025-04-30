# src/cleaner.py

import pandas as pd

def clean_dataset(file_path):
    # Load the dataset (supports .csv and .xlsx)
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Use CSV or XLSX.")

    # Strip whitespaces from column names
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Handle missing values (fill numeric with mean, categorical with mode)
    for col in df.columns:
        if df[col].dtype == "O":  # Object/Categorical
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:  # Numeric
            df[col].fillna(df[col].mean(), inplace=True)

    # Convert date columns if detected
    for col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col])
        except (ValueError, TypeError):
            pass  # Skip if not a datetime

    return df
