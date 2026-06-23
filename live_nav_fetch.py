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