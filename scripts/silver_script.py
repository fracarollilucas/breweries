import pandas as pd
import os

INPUT_FILE = os.path.join("data", "bronze", "raw_data.json")
OUTPUT_PATH = os.path.join("data", "silver", "breweries_parquet")


def treat_column_names(df):
    """
    Trim whitespace from ends of each string column in DataFrame df.
    Rename columns so as to remove capitalization and spaces.
    """

    trim = lambda x : x.strip() if isinstance(x, str) else x
    rename = lambda x : x.lower().replace(" ", "_") if isinstance(x, str) else x
    
    return df.map(trim).map(rename)

def run_silver_script():
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    df = pd.read_json(INPUT_FILE)
    df_treated = treat_column_names(df)

    df_treated.to_parquet(
        OUTPUT_PATH,
        engine="pyarrow", # default engine
        partition_cols=["country"],
        index=False
    )

if __name__ == "__main__":
    run_silver_script()