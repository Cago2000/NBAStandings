import time, os, json
from fetcher.standings_fetcher import fetch_standings

def save_json(data, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    try:
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print("Failed to save standings:", e)

def auto_update_standings(output_file, update_interval):
    while True:
        data = fetch_standings()
        if data:
            save_json(data, output_file)
        else:
            print("Failed to fetch standings, retrying later...")
        time.sleep(update_interval)
