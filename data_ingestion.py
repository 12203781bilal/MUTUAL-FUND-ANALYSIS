import os
import glob
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import logging
from datetime import datetime

DATA_RAW = "data/raw"
DATA_PROCESSED = "data/processed"
DB_FILE = "bluestock_mf.db"

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def ensure_dirs():
    os.makedirs(DATA_PROCESSED, exist_ok=True)


def load_raw_csvs():
    files = glob.glob(os.path.join(DATA_RAW, "*.csv"))
    dfs = {}
    for f in files:
        try:
            df = pd.read_csv(f)
        except Exception:
            df = pd.read_csv(f, encoding='latin1')
        name = os.path.splitext(os.path.basename(f))[0]
        dfs[name] = df
        logging.info(f"Loaded {f}: shape={df.shape}")
        print(df.dtypes)
        print(df.head(3))
    return dfs


def detect_cols(df, candidates):
    cols = {c: next((col for col in df.columns if c in col.lower()), None) for c in candidates}
    return cols


def clean_nav_history(df):
    df = df.copy()
    cols = detect_cols(df, ['date', 'amfi', 'nav'])
    date_col = cols['date'] or 'date'
    amfi_col = cols['amfi'] or 'amfi_code'
    nav_col = cols['nav'] or 'nav'
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[amfi_col]) if amfi_col in df.columns else df
    if nav_col in df.columns:
        df[nav_col] = pd.to_numeric(df[nav_col], errors='coerce')
        df = df[df[nav_col] > 0]
    if amfi_col in df.columns and date_col in df.columns:
        df = df.sort_values([amfi_col, date_col])
        df = df.drop_duplicates(subset=[amfi_col, date_col], keep='first')
        df[nav_col] = df.groupby(amfi_col)[nav_col].ffill()
    return df


def clean_investor_transactions(df):
    df = df.copy()
    cols = detect_cols(df, ['date', 'amount', 'txn', 'state', 'kyc'])
    date_col = cols['date'] or 'date'
    amt_col = cols['amount'] or 'amount'
    txn_col = cols['txn'] or 'transaction_type'
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    if amt_col in df.columns:
        df[amt_col] = pd.to_numeric(df[amt_col], errors='coerce')
        df = df[df[amt_col] > 0]
    if txn_col in df.columns:
        s = df[txn_col].astype(str).str.lower()
        df[txn_col] = np.where(s.str.contains('sip'), 'SIP',
                         np.where(s.str.contains('redem|redeem'), 'Redemption', 'Lumpsum'))
    return df


def clean_scheme_performance(df):
    df = df.copy()
    # Convert any return columns to numeric
    for c in df.columns:
        if 'return' in c.lower() or 'return_' in c.lower() or '%' in c:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    # expense ratio
    exp_cols = [c for c in df.columns if 'expense' in c.lower() or 'expense_ratio' in c.lower()]
    if exp_cols:
        c = exp_cols[0]
        s = df[c].astype(str).str.replace('%', '').str.strip()
        df[c] = pd.to_numeric(s, errors='coerce')
        # If values appear like 0.8 (meaning 0.8%) keep them; if like 0.8 (80%) unlikely
        df['expense_ratio_ok'] = df[c].between(0.1, 2.5)
    return df


def save_cleaned(dfs):
    saved = {}
    for name, df in dfs.items():
        out = os.path.join(DATA_PROCESSED, f"cleaned_{name}.csv")
        df.to_csv(out, index=False)
        saved[name] = out
        logging.info(f"Saved cleaned: {out}")
    return saved


def build_sqlite_and_load(processed_paths):
    engine = create_engine(f'sqlite:///{DB_FILE}')
    counts = {}
    for name, path in processed_paths.items():
        df = pd.read_csv(path)
        table = name.lower()
        df.to_sql(table, engine, if_exists='replace', index=False)
        counts[table] = len(df)
        logging.info(f"Loaded {len(df)} rows into {table}")
    return counts


def main():
    ensure_dirs()
    raw = load_raw_csvs()

    # Apply targeted cleaning where filename matches
    cleaned = {}
    for name, df in raw.items():
        lname = name.lower()
        if 'nav' in lname or 'nav_history' in lname:
            cleaned_df = clean_nav_history(df)
        elif 'transaction' in lname or 'transactions' in lname:
            cleaned_df = clean_investor_transactions(df)
        elif 'performance' in lname:
            cleaned_df = clean_scheme_performance(df)
        else:
            cleaned_df = df.copy()
        cleaned[name] = cleaned_df

    processed_paths = save_cleaned(cleaned)
    counts = build_sqlite_and_load(processed_paths)
    logging.info(f"Row counts in SQLite: {counts}")


if __name__ == '__main__':
    main()

import pandas as pd
import os

DATA_FOLDER = "data/raw"

files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]

print("=" * 80)
print("DATASET EXPLORATION")
print("=" * 80)

for file in files:
    path = os.path.join(DATA_FOLDER, file)

    try:
        df = pd.read_csv(path)

        print(f"\nFILE: {file}")
        print("-" * 50)

        print("Shape:")
        print(df.shape)

        print("\nData Types:")
        print(df.dtypes)

        print("\nHead:")
        print(df.head())

        print("\nMissing Values:")
        print(df.isnull().sum())

    except Exception as e:
        print(f"Error reading {file}: {e}")