from nba_api.live.nba.endpoints import scoreboard
from datetime import datetime
import pytz
import json
import requests

def fetch_live_games():
    germany = pytz.timezone('Europe/Berlin')

    # --- Safe API call wrapper ---
    try:
        sb = scoreboard.ScoreBoard()
        games = sb.games.get_dict()
    except Exception as e:
        print("⚠️ Live game fetch failed:", e)
        return []

    # --- If API responded but sent no games ---
    if not games:
        print("⚠️ API returned no games (empty response).")
        return []

    # --- Process games normally ---
    day_tags = {
        0: " (Mo)", 1: " (Tu)", 2: " (We)", 3: " (Th)",
        4: " (Fr)", 5: " (Sa)", 6: " (So)"
    }

    temp_games = []
    for g in games:
        home_team = g['homeTeam']['teamTricode']
        away_team = g['awayTeam']['teamTricode']

        game_time_est = datetime.fromisoformat(g['gameEt'].replace("Z", "+00:00"))
        game_time_utc = datetime.fromisoformat(g['gameTimeUTC'].replace("Z", "+00:00"))
        game_time_germany = game_time_utc.astimezone(germany)

        time_str = game_time_germany.strftime("%H:%M")

        game_id = g['gameId']
        status_text = g['gameStatusText']
        home_score = g['homeTeam']['score']
        away_score = g['awayTeam']['score']

        if status_text == "Not Started":
            home_score = 0
            away_score = 0

        germany_date = game_time_germany.date()
        est_date = game_time_est.date()

        if germany_date != est_date:
            day_overlap_tag = day_tags[germany_date.weekday()]
        else:
            day_overlap_tag = ""

        time_with_tag = time_str + day_overlap_tag
        temp_games.append({
            "game_id": game_id,
            "time": time_with_tag,
            "home": home_team,
            "away": away_team,
            "home_score": home_score,
            "away_score": away_score,
            "game_status": status_text,
            "_utc": game_time_utc
        })

    temp_games.sort(key=lambda x: x['_utc'])

    return [
        {
            "game_id": g["game_id"],
            "time": g["time"],
            "home": g["home"],
            "away": g["away"],
            "home_score": g["home_score"],
            "away_score": g["away_score"],
            "game_status": g["game_status"]
        }
        for g in temp_games
    ]
