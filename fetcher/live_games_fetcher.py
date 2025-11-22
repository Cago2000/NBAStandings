from nba_api.live.nba.endpoints import scoreboard
from datetime import datetime
import pytz

def fetch_live_games(local_tz='Europe/Berlin'):
    # Get today’s live scoreboard
    sb = scoreboard.ScoreBoard()
    games = sb.games.get_dict()  # list of games

    local_zone = pytz.timezone(local_tz)
    schedule_dict = {}

    for g in games:
        game_id = g['gameId']
        home_team = g['homeTeam']['teamTricode']
        away_team = g['awayTeam']['teamTricode']

        # Convert game start time to local timezone
        game_time_utc = datetime.fromisoformat(g['gameEt'].replace("Z", "+00:00"))
        game_time_local = game_time_utc.astimezone(local_zone)
        time_str = game_time_local.strftime("%H:%M %Z")

        status_text = g['gameStatusText']
        home_score = g['homeTeam']['score']
        away_score = g['awayTeam']['score']
        period = g.get('period', 0)
        clock = g.get('gameClock', "")

        # If scores are 0 and game hasn't started, set to None
        if status_text == "Not Started":
            home_score = None
            away_score = None
            period = 0
            clock = ""

        game_key = f"{away_team} - {home_team}"
        schedule_dict[game_key] = {
            "time": time_str.split(" ")[0],
            "home": home_team,
            "away": away_team,
            "home_score": home_score,
            "away_score": away_score,
            "game_status": status_text,
            "period": period,
            "clock": clock
        }

    return schedule_dict