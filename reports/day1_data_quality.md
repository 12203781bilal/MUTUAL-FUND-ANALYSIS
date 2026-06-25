# Day 1 Data Quality Summary

## Per-file diagnostics
### 01_fund_master
- shape: (6, 6)
- missing counts: {'amfi_code': 0, 'scheme_name': 0, 'fund_house': 0, 'category': 6, 'sub_category': 6, 'risk_grade': 6}
- duplicated rows: 0
### 02_nav_history
- shape: (23008, 4)
- missing counts: {'amfi_code': 0, 'scheme_name': 0, 'date': 0, 'nav': 0}
- duplicated rows: 0
- invalid_nav_count: 1
### Axis_Bluechip_nav
- shape: (3582, 2)
- missing counts: {'date': 0, 'nav': 0}
- duplicated rows: 0
- invalid_nav_count: 0
### HDFC_Top100_Direct_nav
- shape: (3108, 2)
- missing counts: {'date': 0, 'nav': 0}
- duplicated rows: 0
- invalid_nav_count: 0
### HDFC_Top100_nav
- shape: (3108, 2)
- missing counts: {'date': 0, 'nav': 0}
- duplicated rows: 0
- invalid_nav_count: 0
### ICICI_Bluechip_nav
- shape: (3324, 2)
- missing counts: {'date': 0, 'nav': 0}
- duplicated rows: 0
- invalid_nav_count: 1
### Kotak_Bluechip_nav
- shape: (3318, 2)
- missing counts: {'date': 0, 'nav': 0}
- duplicated rows: 0
- invalid_nav_count: 0
### Nippon_LargeCap_nav
- shape: (3315, 2)
- missing counts: {'date': 0, 'nav': 0}
- duplicated rows: 0
- invalid_nav_count: 0
### SBI_Bluechip_nav
- shape: (3253, 2)
- missing counts: {'date': 0, 'nav': 0}
- duplicated rows: 0
- invalid_nav_count: 0

## AMFI Code Validation
- codes in master: 6
- codes in nav_history: 6
- codes in master missing from nav_history: []
- codes in nav_history missing from master: []