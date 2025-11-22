from datetime import datetime, timedelta, time
import pandas as pd
import pytz
from nba_api.stats.endpoints import ScheduleLeagueV2

def fetch_schedule(days_back=1, days_forward=2):
    # Fetch schedule
    schedule = ScheduleLeagueV2()
    games_df = schedule.season_games.get_data_frame()

    # Use the correct timestamp column (UTC)
    games_df['gameDateTimeUTC'] = pd.to_datetime(games_df['gameDateTimeUTC'], utc=True)

    # Timezones
    germany = pytz.timezone('Europe/Berlin')
    today_germany = datetime.now(germany).date()

    # Build filter window based on German dates → convert to UTC
    start_day = today_germany - timedelta(days=days_back)
    end_day = today_germany + timedelta(days=days_forward)

    start_utc = germany.localize(datetime.combine(start_day, time(0, 0))).astimezone(pytz.UTC)
    end_utc = germany.localize(datetime.combine(end_day, time(23, 59, 59))).astimezone(pytz.UTC)

    # Filter games by UTC window
    window_games = games_df[
        (games_df['gameDateTimeUTC'] >= start_utc) &
        (games_df['gameDateTimeUTC'] <= end_utc)
    ].copy()

    # Convert to German time
    window_games['gameDateTimeGerman'] = window_games['gameDateTimeUTC'].dt.tz_convert(germany)
    window_games['gameTimeGerman'] = window_games['gameDateTimeGerman'].dt.strftime('%H:%M')

    # Build schedule grouped by German date
    schedule_dict = {}

    for date, group in window_games.groupby(window_games['gameDateTimeGerman'].dt.date):
        date_str = date.strftime('%A, %d %b %Y')
        if date == today_germany:
            date_str += " (Today)"

        games_list = []

        for _, row in group.iterrows():
            games_list.append({
                "time": row['gameTimeGerman'],
                "home": row['homeTeam_teamTricode'],
                "away": row['awayTeam_teamTricode'],
                "status": row['gameStatusText'],
                "home_score": row['homeTeam_score'] if pd.notna(row['homeTeam_score']) else None,
                "away_score": row['awayTeam_score'] if pd.notna(row['awayTeam_score']) else None
            })

        # Sort chronologically
        games_list.sort(key=lambda x: datetime.strptime(x['time'], '%H:%M'))

        schedule_dict[date_str] = games_list

    return schedule_dict
