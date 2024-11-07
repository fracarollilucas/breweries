import pandas as pd
import os


INPUT_PATH = os.path.join("data", "silver", "breweries_parquet")
OUTPUT_FOLDER = os.path.join("data", "gold")
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "aggregated_breweries.parquet")


def create_aggregated_view(data, group_by=None):
    """Receives a Dataframe data and a list of grouping columns 
    group_by and returns the Dataframe grouped by these columns
    with the count of the breweries observing each grouping
    criterium."""
    grouped_data = data \
        .groupby(group_by, observed=False) \
        .size() \
        .reset_index(name="brewery_count")

    return grouped_data

def run_gold_script():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    df = pd.read_parquet(INPUT_PATH)

    df_aggregated = create_aggregated_view(df, ["country", "brewery_type"])

    
    with open(OUTPUT_FILE, 'wb') as output:
        df_aggregated.to_parquet(
            output, 
            index=False)

if __name__ == "__main__":
    run_gold_script()