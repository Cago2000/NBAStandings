from datetime import datetime, timedelta, time
import pandas as pd
import pytz
from nba_api.stats.endpoints import ScheduleLeagueV2

def fetch_schedule(days_back=1, days_forward=2):
    schedule = ScheduleLeagueV2()
    games_df = schedule.season_games.get_data_frame()

    # Convert string columns to datetime
    games_df['gameDateTimeEst'] = pd.to_datetime(games_df['gameDateTimeEst'])

    # Eastern timezone
    eastern = pytz.timezone("US/Eastern")
    today = datetime.now(eastern).date()

    # Start and end of window
    start_day = today - timedelta(days=days_back)
    end_day = today + timedelta(days=days_forward)
    start_date = eastern.localize(datetime.combine(start_day, time(0, 0, 0)))
    end_date = eastern.localize(datetime.combine(end_day, time(23, 59, 59)))

    # Filter games in window
    window_games = games_df[
        (games_df['gameDateTimeEst'] >= start_date) &
        (games_df['gameDateTimeEst'] <= end_date)
    ]

    schedule_dict = {}
    for date, group in window_games.groupby(window_games['gameDateTimeEst'].dt.date):
        if date == today:
            date_str = date.strftime('%A, %d %b %Y') + " (Today)"
        else:
            date_str = date.strftime('%A, %d %b %Y')

        schedule_dict[date_str] = []

        for _, row in group.iterrows():
            dt_est = row['gameDateTimeEst']

            if dt_est.tzinfo is None:
                dt_local = pytz.UTC.localize(dt_est).astimezone(eastern)
            else:
                dt_local = dt_est.tz_convert(eastern)

            time_str = dt_local.strftime('%I:%M%p')  # e.g., "07:30 PM EST"

            away = row['awayTeam_teamTricode']
            home = row['homeTeam_teamTricode']
            status = row['gameStatusText']

            away_score = row['awayTeam_score'] if pd.notna(row['awayTeam_score']) else None
            home_score = row['homeTeam_score'] if pd.notna(row['homeTeam_score']) else None

            game_info = {
                "time": time_str,
                "away": away,
                "home": home,
                "game_status": status,
                "away_score": away_score,
                "home_score": home_score
            }
            schedule_dict[date_str].append(game_info)

    return schedule_dict
