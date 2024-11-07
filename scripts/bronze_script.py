import requests
import json
import os

BASE_URL = "https://api.openbrewerydb.org/v1/breweries"
METADATA_URL = f"{BASE_URL}/meta"

BASE_DIR = os.path.join("data", "bronze")
OUTPUT_PATH = os.path.join(BASE_DIR, "raw_data.json")

def get_total_breweries(default_val):
    """Sends a GET request that returns the total number of breweries
    as a string (hence the casting to int). Accepts a custom value to
    be used as default in case the request fails."""
    total = int(requests
                .get(METADATA_URL)
                .json()
                .get("total", default_val))

    return total

def get_all_breweries(pages, per_page):
    """Receives a number of pages and a number of breweries to fetch
    per page in each GET request. Returns a list of all the breweries
    with their respective data."""
    all_breweries = []

    with requests.Session() as session: # 25% faster than requests.get()
        for page in range(1, pages + 1):
            breweries = session.get(f"{BASE_URL}?page={page}&per_page={per_page}")
            all_breweries.extend(breweries.json())

    return all_breweries

def run_bronze_script():
    os.makedirs(BASE_DIR, exist_ok=True)
    per_page = 200 # maximum number of results per page

    # as of 2024-10-31, 8430 was the total number
    total_breweries = get_total_breweries(default_val=8430)
    pages = total_breweries // per_page + 1

    all_breweries = get_all_breweries(pages, per_page)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as output:
        json.dump(all_breweries, output, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    run_bronze_script()