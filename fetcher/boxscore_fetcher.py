import json
import time
from nba_api.stats.endpoints import BoxScoreTraditionalV3
from utils.file_paths import *

def fetch_boxscores() -> dict:
    with open(SCHEDULE_FILEPATH, "r") as f:
        schedule = json.load(f)

    results = {}

    for date_label, games in schedule.items():
        day_results = []

        for game in games:
            game_id = game["game_id"]
            status = game["game_status"]

            # Ignore future games ("7:30 PM ET")
            if "ET" in status:
                continue

            boxscore = None

            # Retry for rate limits
            for _ in range(3):
                try:
                    endpoint = BoxScoreTraditionalV3(game_id=game_id)
                    boxscore = endpoint.get_dict()
                    break
                except Exception:
                    time.sleep(1)

            if boxscore is None:
                continue
            # Extract player stats
            players = boxscore["boxScoreTraditional"]
            # Build output entry
            day_results.append({
                "game_id": game_id,
                "players": players
            })

        if day_results:
            results[date_label] = day_results

    return results
