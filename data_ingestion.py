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