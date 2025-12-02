from nba_api.live.nba.endpoints.boxscore import BoxScore
from nba_api.live.nba.endpoints.scoreboard import ScoreBoard

def fetch_live_boxscores() -> list[dict]:
    results = []

    # Fetch today's live games
    scoreboard = ScoreBoard()
    live_games = scoreboard.games.get_dict() if scoreboard.games else []

    for game in live_games:
        if game["gameStatus"] == 0:
            continue

        game_id = game["gameId"]
        live_box = BoxScore(game_id)

        home_players = live_box.home_team_player_stats.get_dict() if live_box.home_team_player_stats else []
        away_players = live_box.away_team_player_stats.get_dict() if live_box.away_team_player_stats else []

        all_players = home_players + away_players

        results.append({
            "game_id": game_id,
            "players": all_players
        })

    return results
