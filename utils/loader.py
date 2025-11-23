import json


def load_template(file_path):
    try:
        with open(file_path) as f:
            return f.read()
    except Exception as e:
        print("Template load error:", e)
        return "<html><body><p>Template error</p></body></html>"

def load_standings(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception:
        return {u: {"East": [], "West": []} for u in ["Can", "Marlon", "Ole"]}

def load_standings_predictions(file_path):
    try:
        with open(file_path) as f:
            return json.load(f)
    except Exception:
        return {u: {"East": [], "West": []} for u in ["Can", "Marlon", "Ole"]}

def load_mvp_ladder(mvp_ladder_file):
    try:
        with open(mvp_ladder_file, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Failed to load MVP ladder:", e)
        return {}

def load_mvp_predictions(mvp_predictions_file):
    try:
        with open(mvp_predictions_file, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Failed to load MVP Predictions:", e)
        return {}

def load_schedule(schedule_file):
    try:
        with open(schedule_file, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Failed to load Schedule:", e)
        return {}

def load_boxscores(boxscores_file):
    try:
        with open(boxscores_file, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Failed to load Boxscores:", e)
        return {}

def load_live_games(live_games_file):
    try:
        with open(live_games_file, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Failed to load Live Games:", e)
        return {}