# Data Dictionary and Change Log

This document describes columns, data types, business definitions, sources, and the cleaning steps applied.

Files processed: all CSVs under `data/raw` ➜ cleaned CSVs written to `data/processed/cleaned_<name>.csv`.

General changes applied (step-by-step):
1. Loaded all CSVs from `data/raw/` using `pandas.read_csv()` with fallback encoding `latin1`.
2. For `nav` datasets: parsed date columns to `datetime`, coerced NAV to numeric, removed NAV<=0, sorted by (`amfi_code`, date), dropped duplicates and forward-filled NAVs per `amfi_code`.
3. For `investor_transactions`: parsed dates to `datetime`, converted amounts to numeric and removed amount<=0, standardized `transaction_type` to `SIP`, `Lumpsum`, or `Redemption`.
4. For `scheme_performance`: coerced return columns to numeric, normalized `expense_ratio` to numeric (removed % if present) and flagged rows outside 0.1-2.5 range.
5. Saved all cleaned outputs to `data/processed/` and loaded into SQLite `bluestock_mf.db`.

Column examples and definitions (update per your CSVs):

- `amfi_code` (TEXT): AMFI scheme identifier. Source: scheme master / nav files.
- `scheme_name` (TEXT): Fund scheme name.
- `fund_house` (TEXT): AMC / fund house name.
- `date` / `as_on` (DATE): Date of NAV / performance record. Normalized to ISO `YYYY-MM-DD`.
- `nav` (REAL): Net Asset Value per unit (in INR). Must be > 0.
- `amount` (REAL): Transaction amount in INR. Must be > 0.
- `transaction_type` (TEXT): Standardized to `SIP`, `Lumpsum`, `Redemption`.
- `expense_ratio` (REAL): Expense ratio as percent (e.g., 0.75 means 0.75%). Validated between 0.1 and 2.5.
- `investor_id` (TEXT): Identifier for investor (if present).
- `state` (TEXT): Investor state (if present).
- `kyc_status` (TEXT): KYC flag / status (if present).

Anomalies found (examples):
- Missing or non-standard date columns in some files — coerced with `errors='coerce'` resulting in NaT for bad rows.
- NAV or amount values as text with commas or percent signs — coerced to numeric where possible.
- Duplicate rows by (`amfi_code`, date) were dropped, keeping first occurrence.

Source reference: raw CSV filename saved under `data/raw/`.
