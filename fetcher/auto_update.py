import time, os, json
from utils.file_paths import *
from fetcher.live_games_fetcher import fetch_live_games
from fetcher.mvp_ladder_fetcher import fetch_mvp_ladder
from fetcher.standings_fetcher import fetch_standings
from fetcher.schedule_fetcher import fetch_schedule
from fetcher.boxscore_fetcher import fetch_boxscores
from fetcher.live_boxscore_fetcher import fetch_live_boxscores

def save_json(data, FILEPATH):
    os.makedirs(os.path.dirname(FILEPATH), exist_ok=True)
    try:
        with open(FILEPATH, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print("Failed to save json:", e)

def auto_update_standings(update_interval):
    while True:
        data = fetch_standings()
        if data:
            save_json(data, STANDINGS_FILEPATH)
        else:
            print("Failed to fetch standings, retrying later...")
        time.sleep(update_interval)

def auto_update_mvp_ladder(update_interval):
    while True:
        data = fetch_mvp_ladder()
        if data:
            save_json(data, MVP_LADDER_FILEPATH)
        else:
            print("Failed to fetch mvp ladder, retrying later...")
        time.sleep(update_interval)

def auto_update_schedule(update_interval):
    while True:
        data = fetch_schedule()
        if data:
            save_json(data, SCHEDULE_FILEPATH)
        else:
            print("Failed to fetch schedule, retrying later...")
        time.sleep(update_interval)

def auto_update_live_games(update_interval):
    while True:
        data = fetch_live_games()
        if data:
            save_json(data, LIVE_GAMES_FILEPATH)
        else:
            print("Failed to fetch live games, retrying later...")
        time.sleep(update_interval)


def auto_update_boxscores(update_interval):
    while True:
        data = fetch_boxscores()
        if data:
            save_json(data, BOXSCORE_FILEPATH)
        else:
            print("Failed to fetch boxscores, retrying later...")
        time.sleep(update_interval)


def auto_update_live_boxscores(update_interval):
    while True:
        data = fetch_live_boxscores()
        if data:
            for d in data:
                print(d["game_id"])
            save_json(data, LIVE_BOXSCORE_FILEPATH)
        else:
            print("Failed to fetch live boxscores, retrying later...")
        time.sleep(update_interval)