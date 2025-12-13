from nba_api.live.nba.endpoints import scoreboard
from datetime import datetime
import pytz


def fetch_live_games():
    germany = pytz.timezone('Europe/Berlin')

    try:
        sb = scoreboard.ScoreBoard()
        games = sb.games.get_dict()
    except Exception as e:
        print("⚠️ Live game fetch failed:", e)
        return []

    if not games:
        print("⚠️ API returned no games (empty response).")
        return []

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


def update_schedule_with_live_data(schedule_dict, live_games):
    if not live_games:
        return schedule_dict

    live_game_map = {
        game['game_id']: game
        for game in live_games
        if game.get('game_id')
    }

    updated_count = 0
    for day, games in schedule_dict.items():
        for game in games:
            game_id = game.get('game_id')
            if game_id in live_game_map:
                live_data = live_game_map[game_id]
                game['game_status'] = live_data['game_status']
                game['home_score'] = live_data['home_score']
                game['away_score'] = live_data['away_score']
                updated_count += 1

    if updated_count > 0:
        print(f"✓ Updated {updated_count} games with live data")

    return schedule_dict


if __name__ == '__main__':
    print("Testing live game fetcher...")
    games = fetch_live_games()
    print(f"\nFound {len(games)} games:")
    for game in games:
        status = game['game_status']
        scores = f"{game['away_score']}-{game['home_score']}" if status != "Not Started" else "vs"
        print(f"  {game['time']}: {game['away']} {scores} {game['home']} - {status}")