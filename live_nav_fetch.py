import requests
import pandas as pd
import os

OUT_DIR = "data/raw"

SCHEMES = {
    'HDFC_Top100_Direct': '125497',
    'SBI_Bluechip': '119551',
    'ICICI_Bluechip': '120503',
    'Nippon_LargeCap': '118632',
    'Axis_Bluechip': '119092',
    'Kotak_Bluechip': '120841'
}


def fetch_scheme(amfi_code):
    url = f"https://api.mfapi.in/mf/{amfi_code}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()


def save_nav_json_and_csv(name, data):
    os.makedirs(OUT_DIR, exist_ok=True)
    jfile = os.path.join(OUT_DIR, f"{name}_raw.json")
    with open(jfile, 'w', encoding='utf-8') as f:
        import json
        json.dump(data, f, ensure_ascii=False, indent=2)
    # Parse 'data' key -> list of {'date','nav'}
    records = data.get('data') or []
    df = pd.DataFrame(records)
    csvfile = os.path.join(OUT_DIR, f"{name}_nav.csv")
    df.to_csv(csvfile, index=False)
    print(f"Saved {csvfile}")


def main():
    for name, code in SCHEMES.items():
        try:
            data = fetch_scheme(code)
            save_nav_json_and_csv(name, data)
        except Exception as e:
            print(f"Failed {name} ({code}): {e}")


if __name__ == '__main__':
    main()
import requests
import pandas as pd
import os

os.makedirs("data/raw", exist_ok=True)

schemes = {
    "HDFC_Top100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_LargeCap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

for name, code in schemes.items():

    url = f"https://api.mfapi.in/mf/{code}"

    print(f"Fetching {name}...")

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        df = pd.DataFrame(data["data"])

        filename = f"data/raw/{name}_nav.csv"

        df.to_csv(filename, index=False)

        print(f"Saved: {filename}")

    else:
        print(f"Failed: {name}")