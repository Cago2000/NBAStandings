from nba_api.live.nba.endpoints import scoreboard
from datetime import datetime
import pytz


def fetch_live_games():
    germany = pytz.timezone('Europe/Berlin')

    sb = scoreboard.ScoreBoard()
    games = sb.games.get_dict()

    games_list = []

    for g in games:
        home_team = g['homeTeam']['teamTricode']
        away_team = g['awayTeam']['teamTricode']

        game_time_est = datetime.fromisoformat(g['gameEt'].replace("Z", "+00:00"))
        game_time_utc = datetime.fromisoformat(g['gameTimeUTC'].replace("Z", "+00:00"))

        day_tags = {
            0: " (Mo)", 1: " (Tu)", 2: " (We)", 3: " (Th)", 4: " (Fr)", 5: " (Sa)", 6: " (So)"
        }
        day_overlap_tag = day_tags[game_time_est.weekday()+1] if game_time_est.date() != game_time_utc.date() else ""

        game_time_germany = game_time_utc.astimezone(germany)
        time_str = game_time_germany.strftime("%H:%M")

        status_text = g['gameStatusText']
        home_score = g['homeTeam']['score']
        away_score = g['awayTeam']['score']
        period = g.get('period', 0)
        clock = g.get('gameClock', "")

        if status_text == "Not Started":
            home_score = None
            away_score = None
            period = 0
            clock = ""

        games_list.append({
            "time": time_str + day_overlap_tag,
            "home": home_team,
            "away": away_team,
            "home_score": home_score,
            "away_score": away_score,
            "game_status": status_text,
            "period": period,
            "clock": clock,
            "utc_time": game_time_utc.isoformat()
        })

    games_list.sort(key=lambda x: datetime.fromisoformat(x['utc_time']))

    return games_list

if __name__ == "__main__":
    fetch_live_games()