from nba_api.live.nba.endpoints import scoreboard
from datetime import datetime
import pytz
import json


def fetch_live_games():
    germany = pytz.timezone('Europe/Berlin')
    sb = scoreboard.ScoreBoard()
    games = sb.games.get_dict()

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

        status_text = g['gameStatusText']
        home_score = g['homeTeam']['score']
        away_score = g['awayTeam']['score']

        if status_text == "Not Started":
            home_score = 0
            away_score = 0

        day_overlap_tag = day_tags[game_time_est.weekday() + 1] if game_time_est.date() != game_time_utc.date() else ""
        time_with_tag = time_str + day_overlap_tag

        temp_games.append({
            "time": time_with_tag,
            "home": home_team,
            "away": away_team,
            "home_score": home_score,
            "away_score": away_score,
            "game_status": status_text,
            "_utc": game_time_utc
        })

    temp_games.sort(key=lambda x: x['_utc'])

    schedule_json = {}
    for game in temp_games:
        game_date = game['_utc'].date()
        day_name = game_date.strftime("%A, %d %b %Y")
        if day_name not in schedule_json:
            schedule_json[day_name] = []

        schedule_json[day_name].append({
            "time": game["time"],
            "home": game["home"],
            "away": game["away"],
            "home_score": game["home_score"],
            "away_score": game["away_score"],
            "game_status": game["game_status"]
        })

    return schedule_json