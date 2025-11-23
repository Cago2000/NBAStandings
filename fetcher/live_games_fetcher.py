from nba_api.live.nba.endpoints import scoreboard
from datetime import datetime
import pytz
import json


def fetch_live_games():
    germany = pytz.timezone('Europe/Berlin')
    print("[DEBUG] Fetching scoreboard...")

    sb = scoreboard.ScoreBoard()
    games = sb.games.get_dict()
    print(f"[DEBUG] Number of games fetched: {len(games)}")

    day_tags = {
        0: " (Mo)", 1: " (Tu)", 2: " (We)", 3: " (Th)",
        4: " (Fr)", 5: " (Sa)", 6: " (So)"
    }

    temp_games = []
    for g in games:
        print("\n[DEBUG] Processing game:", g['gameId'])

        home_team = g['homeTeam']['teamTricode']
        away_team = g['awayTeam']['teamTricode']
        print(f"[DEBUG] Teams: {away_team} @ {home_team}")

        game_time_est = datetime.fromisoformat(g['gameEt'].replace("Z", "+00:00"))
        game_time_utc = datetime.fromisoformat(g['gameTimeUTC'].replace("Z", "+00:00"))
        game_time_germany = game_time_utc.astimezone(germany)

        print(f"[DEBUG] gameEt: {game_time_est}, gameTimeUTC: {game_time_utc}, Germany time: {game_time_germany}")

        time_str = game_time_germany.strftime("%H:%M")

        game_id = g['gameId']
        status_text = g['gameStatusText']
        home_score = g['homeTeam']['score']
        away_score = g['awayTeam']['score']

        print(f"[DEBUG] Status: {status_text} — Scores: {away_score}-{home_score}")

        if status_text == "Not Started":
            print("[DEBUG] Game not started → forcing score to 0-0")
            home_score = 0
            away_score = 0

        germany_date = game_time_germany.date()
        est_date = game_time_est.date()

        if germany_date != est_date:
            day_overlap_tag = day_tags[germany_date.weekday()]
        else:
            day_overlap_tag = ""

        print(f"[DEBUG] Day overlap tag: '{day_overlap_tag}'")

        time_with_tag = time_str + day_overlap_tag
        print(f"[DEBUG] Final time label: {time_with_tag}")

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

    print("\n[DEBUG] Sorting games by UTC time...")
    temp_games.sort(key=lambda x: x['_utc'])

    print("[DEBUG] Building final list...")
    live_games_list = []
    for game in temp_games:
        print(f"[DEBUG] -> {game['game_id']} ({game['away']} @ {game['home']}) — {game['time']}")

        live_games_list.append({
            "game_id": game["game_id"],
            "time": game["time"],
            "home": game["home"],
            "away": game["away"],
            "home_score": game["home_score"],
            "away_score": game["away_score"],
            "game_status": game["game_status"]
        })

    print("[DEBUG] Done.\n")
    return live_games_list
