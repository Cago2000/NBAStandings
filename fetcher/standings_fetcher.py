from nba_api.stats.endpoints import LeagueStandings

def fetch_standings():
    """Fetch NBA standings with full team names."""
    try:
        standings_resp = LeagueStandings()
        standings_data = standings_resp.get_data_frames()[0]
        result = {"East": [], "West": []}
        for _, row in standings_data.iterrows():
            conf = row['Conference']
            if conf in result:
                result[conf].append({
                    "team": f"{row["TeamCity"]} {row['TeamName']}",
                    "games_behind": float(row['ConferenceGamesBack']),
                    "wins": int(row['WINS']),
                    "losses": int(row['LOSSES'])
                })

        for conf in result:
            result[conf].sort(key=lambda x: x["wins"], reverse=True)

        return result
    except Exception as e:
        print("Error fetching NBA data:", e)
        return None
