from nba_api.stats.endpoints import LeagueStandings


def fetch_standings():
    """Fetch NBA standings with full team names."""
    try:
        print("Starting standings fetch")
        standings_resp = LeagueStandings()
        standings_data = standings_resp.get_data_frames()[0]
        print(f"Got standings data with {len(standings_data)} teams")

        result = {"East": [], "West": []}
        for _, row in standings_data.iterrows():
            conf = row['Conference']
            if conf in result:
                result[conf].append({
                    "team": f"{row['TeamCity']} {row['TeamName']}",
                    "games_behind": float(row['ConferenceGamesBack']),
                    "wins": int(row['WINS']),
                    "losses": int(row['LOSSES'])
                })

        for conf in result:
            result[conf].sort(key=lambda x: x["wins"], reverse=True)

        print(f"Processed {len(result['East'])} East teams, {len(result['West'])} West teams")
        return result
    except Exception as e:
        print("Error fetching NBA data:", e)
        return None