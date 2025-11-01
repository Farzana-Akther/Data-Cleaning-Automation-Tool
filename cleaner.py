import pandas as pd
import numpy as np

def handle_missing(df, strategy='mean'):
    df_clean = df.copy()
    for col in df_clean.columns:
        if df_clean[col].isnull().sum() > 0:
            if df_clean[col].dtype in ['int64', 'float64']:
                if strategy == 'mean':
                    df_clean[col].fillna(df_clean[col].mean(), inplace=True)
                elif strategy == 'median':
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
            else:
                df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
    return df_clean

def remove_duplicates(df):
    return df.drop_duplicates()

def clean_text_columns(df):
    df_clean = df.copy()
    for col in df_clean.select_dtypes(include=['object', 'string']).columns:
        df_clean[col] = (
            df_clean[col]
            .astype(str)
            .str.strip()
            .str.lower()
            .str.replace(r'[^\w\s]', '', regex=True)
        )
        df_clean[col].replace("nan", np.nan, inplace=True)
    return df_clean

def remove_outliers(df):
    df_clean = df.copy()
    numeric_cols = df_clean.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df_clean = df_clean[(df_clean[col] >= lower) & (df_clean[col] <= upper)]
    return df_clean

def auto_clean(df):
    print("📌 Original shape:", df.shape)
    df = remove_duplicates(df)
    df = handle_missing(df)
    df = clean_text_columns(df)
    df = remove_outliers(df)
    return df
