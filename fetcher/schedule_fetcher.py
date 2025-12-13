from datetime import datetime, timedelta, time
import pandas as pd
import pytz
from nba_api.stats.endpoints import ScheduleLeagueV2


def fetch_schedule(days_back=1, days_with_games=4):
    print("Starting schedule fetch")

    schedule = ScheduleLeagueV2()
    print("Got ScheduleLeagueV2 object")

    games_df = schedule.season_games.get_data_frame()
    print(f"Got games_df with {len(games_df)} rows")

    games_df['gameDateTimeUTC'] = pd.to_datetime(games_df['gameDateTimeUTC'], utc=True)
    print("Converted gameDateTimeUTC to datetime")

    eastern = pytz.timezone("US/Eastern")
    germany = pytz.timezone("Europe/Berlin")
    today_eastern = datetime.now(eastern).date()

    start_day = today_eastern - timedelta(days=days_back)
    start_utc = eastern.localize(datetime.combine(start_day, time(0, 0))).astimezone(pytz.UTC)
    print(f"Start UTC: {start_utc}")

    future_games = games_df[games_df['gameDateTimeUTC'] >= start_utc].copy()
    future_games = future_games.sort_values('gameDateTimeUTC')
    print(f"Filtered to {len(future_games)} future games")

    unique_dates = future_games['gameDateTimeUTC'].apply(lambda x: x.astimezone(eastern).date()).unique()
    print(f"Found {len(unique_dates)} unique dates")

    available_days = len(unique_dates)
    selected_dates = unique_dates[:min(days_with_games, available_days)]
    print(f"Selected {len(selected_dates)} dates")

    window_games = future_games[
        future_games['gameDateTimeUTC'].apply(lambda x: x.astimezone(eastern).date()).isin(selected_dates)
    ]
    print(f"Window has {len(window_games)} games")

    day_tags = {0: " (Mo)", 1: " (Tu)", 2: " (We)", 3: " (Th)", 4: " (Fr)", 5: " (Sa)", 6: " (So)"}

    print("Starting groupby operation")
    grouped = {}
    for date, group in window_games.groupby(
            window_games['gameDateTimeUTC'].apply(lambda x: x.astimezone(eastern).date())):
        print(f"Processing date: {date}")

        date_str = date.strftime('%A, %d %b %Y')
        if date == today_eastern:
            date_str += " (Today)"

        games_list = []
        print(f"Iterating over {len(group)} games for {date}")
        for _, row in group.iterrows():
            game_time_germany = row['gameDateTimeUTC'].tz_convert(germany)
            time_germany_str = game_time_germany.strftime('%H:%M')
            game_id = row['gameId']
            game_time_est = row['gameDateTimeUTC'].tz_convert(eastern)

            germany_date = game_time_germany.date()
            est_date = game_time_est.date()
            if germany_date != est_date:
                day_overlap_tag = day_tags[germany_date.weekday()]
            else:
                day_overlap_tag = ""

            games_list.append({
                "game_id": game_id,
                "time": time_germany_str + day_overlap_tag,
                "home": row['homeTeam_teamTricode'],
                "away": row['awayTeam_teamTricode'],
                "game_status": row['gameStatusText'],
                "home_score": row['homeTeam_score'],
                "away_score": row['awayTeam_score'],
            })

        grouped[date_str] = games_list
        print(f"Added {len(games_list)} games for {date_str}")

    print(f"Finished, returning {len(grouped)} date groups")
    return grouped