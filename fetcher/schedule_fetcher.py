from datetime import datetime, timedelta, time
import pandas as pd
import pytz
from nba_api.stats.endpoints import ScheduleLeagueV2
from fetcher.standings_fetcher import fetch_standings
from utils.loader import load_standings


def fetch_schedule(days_back=1, days_with_games=4, verbose=False):
    if verbose:
        print("Starting schedule fetch")

    try:
        schedule = ScheduleLeagueV2()
        if verbose:
            print("Got ScheduleLeagueV2 object")

        games_df = schedule.season_games.get_data_frame()
        if verbose:
            print(f"Got games_df with {len(games_df)} rows")
    except Exception as e:
        print(f"Error fetching schedule data: {e}")
        return None

    try:
        games_df['gameDateTimeUTC'] = pd.to_datetime(games_df['gameDateTimeUTC'], utc=True)
        if verbose:
            print("Converted gameDateTimeUTC to datetime")

        eastern = pytz.timezone("US/Eastern")
        germany = pytz.timezone("Europe/Berlin")
        today_eastern = datetime.now(eastern).date()

        start_day = today_eastern - timedelta(days=days_back)
        start_utc = eastern.localize(datetime.combine(start_day, time(0, 0))).astimezone(pytz.UTC)
        if verbose:
            print(f"Start UTC: {start_utc}")

        games_df = games_df[games_df['gameDateTimeUTC'] >= start_utc].copy()
        games_df = games_df.sort_values('gameDateTimeUTC')
        if verbose:
            print(f"Filtered to {len(games_df)} games")

        unique_dates = games_df['gameDateTimeUTC'].apply(
            lambda x: x.astimezone(eastern).date()
        ).unique()
        if verbose:
            print(f"Found {len(unique_dates)} unique dates")

        selected_dates = unique_dates[:days_with_games]
        if verbose:
            print(f"Selected {len(selected_dates)} dates")

        games_df = games_df[
            games_df['gameDateTimeUTC'].apply(
                lambda x: x.astimezone(eastern).date()
            ).isin(selected_dates)
        ]
        if verbose:
            print(f"Window has {len(games_df)} games")

        day_tags = {0: " (Mo)", 1: " (Tu)", 2: " (We)", 3: " (Th)", 4: " (Fr)", 5: " (Sa)", 6: " (So)"}

        if verbose:
            print("Starting groupby operation")

        grouped = {}
        standings = load_standings()

        for date, group in games_df.groupby(
                games_df['gameDateTimeUTC'].apply(lambda x: x.astimezone(eastern).date())):
            if verbose:
                print(f"Processing date: {date}")

            date_str = date.strftime('%A, %d %b %Y')
            if date == today_eastern:
                date_str += " (Today)"

            games_list = []
            if verbose:
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

                home_seed, away_seed = 0, 0
                for conference, standing_entries in standings.items():
                    for standing_entry in standing_entries:
                        if f"{row['homeTeam_teamCity']} {row['homeTeam_teamName']}" == standing_entry['team']:
                            home_seed = standing_entry['seed']
                        if f"{row['awayTeam_teamCity']} {row['awayTeam_teamName']}" == standing_entry['team']:
                            away_seed = standing_entry['seed']

                games_list.append({
                    "game_id": game_id,
                    "time": time_germany_str + day_overlap_tag,
                    "home": row['homeTeam_teamTricode'],
                    "away": row['awayTeam_teamTricode'],
                    "game_status": row['gameStatusText'],
                    "home_score": row['homeTeam_score'],
                    "away_score": row['awayTeam_score'],
                    "home_seed": home_seed,
                    "away_seed": away_seed
                })

            grouped[date_str] = games_list
            if verbose:
                print(f"Added {len(games_list)} games for {date_str}")

        if verbose:
            print(f"Finished, returning {len(grouped)} date groups")

        return grouped

    except Exception as e:
        print(f"Error processing schedule: {e}")
        return None