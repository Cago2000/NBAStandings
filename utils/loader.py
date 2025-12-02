import json
from utils.file_paths import *

def load_template(file_path):
    try:
        with open(file_path) as f:
            return f.read()
    except Exception as e:
        print("Template load error:", e)
        return "<html><body><p>Template error</p></body></html>"

def load_standings():
    try:
        with open(STANDINGS_FILEPATH, "r") as f:
            return json.load(f)
    except Exception:
        return {u: {"East": [], "West": []} for u in ["Can", "Marlon", "Ole"]}

def load_standings_predictions():
    try:
        with open(STANDINGS_PREDICTIONS_FILEPATH) as f:
            return json.load(f)
    except Exception:
        return {u: {"East": [], "West": []} for u in ["Can", "Marlon", "Ole"]}

def load_mvp_ladder():
    try:
        with open(MVP_LADDER_FILEPATH, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Failed to load MVP ladder:", e)
        return {}

def load_mvp_predictions():
    try:
        with open(MVP_PREDICTIONS_FILEPATH, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Failed to load MVP Predictions:", e)
        return {}

def load_schedule():
    try:
        with open(SCHEDULE_FILEPATH, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Failed to load Schedule:", e)
        return {}

def load_live_games():
    try:
        with open(LIVE_GAMES_FILEPATH, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Failed to load Live Games:", e)
        return {}

def load_boxscores():
    try:
        with open(BOXSCORE_FILEPATH, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Failed to load Boxscores:", e)
        return {}

def load_live_boxscores():
    try:
        with open(LIVE_BOXSCORE_FILEPATH, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Failed to load Live Boxscores:", e)
        return {}

