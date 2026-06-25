-- Star schema for mutual fund analytics

BEGIN TRANSACTION;

CREATE TABLE dim_fund (
  fund_id INTEGER PRIMARY KEY,
  amfi_code TEXT UNIQUE,
  scheme_name TEXT,
  fund_house TEXT,
  category TEXT,
  sub_category TEXT,
  risk_grade TEXT
);

CREATE TABLE dim_date (
  date_id INTEGER PRIMARY KEY,
  date DATE UNIQUE,
  year INTEGER,
  month INTEGER,
  day INTEGER,
  quarter INTEGER
);

CREATE TABLE fact_nav (
  nav_id INTEGER PRIMARY KEY,
  amfi_code TEXT,
  date DATE,
  nav REAL,
  FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_transactions (
  txn_id INTEGER PRIMARY KEY,
  investor_id TEXT,
  amfi_code TEXT,
  date DATE,
  transaction_type TEXT,
  amount REAL,
  state TEXT,
  kyc_status TEXT,
  FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_performance (
  perf_id INTEGER PRIMARY KEY,
  amfi_code TEXT,
  as_on DATE,
  return_1y REAL,
  return_3y REAL,
  return_5y REAL,
  expense_ratio REAL,
  FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_aum (
  aum_id INTEGER PRIMARY KEY,
  amfi_code TEXT,
  as_on DATE,
  aum REAL,
  FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code)
);

COMMIT;
