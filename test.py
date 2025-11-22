from nba_api.live.nba.endpoints import BoxScore

game_id = "0022500268"  # example NBA game ID
live_game = BoxScore(game_id)

print("Home:", live_game.home_team.get_dict()['teamTricode'], live_game.home_team.get_dict()['score'])
print("Away:", live_game.away_team.get_dict()['teamTricode'], live_game.away_team.get_dict()['score'])
print("Quarter:", live_game.game.get_dict()['period'])
print("Clock:", live_game.game.get_dict()['gameClock'])
