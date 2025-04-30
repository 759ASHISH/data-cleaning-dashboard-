import pandas as pd

def clean_dataset(file_path):
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Use CSV or XLSX.")

    df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

    df.drop_duplicates(inplace=True)

    for col in df.columns:
        if df[col].dtype == "O":  
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:  
            df[col].fillna(df[col].mean(), inplace=True)

    for col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col])
        except (ValueError, TypeError):
            pass  

    return df
