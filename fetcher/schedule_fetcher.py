from datetime import timedelta, datetime
import pandas as pd
import pytz
from nba_api.stats.endpoints import ScheduleLeagueV2


def fetch_schedule(days_back=1, days_forward=3, local_tz='Europe/Berlin'):
    schedule = ScheduleLeagueV2()
    games_df = schedule.season_games.get_data_frame()

    # Convert to datetime and localize
    games_df['gameDateTimeEst'] = pd.to_datetime(games_df['gameDateTimeEst'])
    games_df['gameDateTimeLocal'] = games_df['gameDateTimeEst'].dt.tz_convert(pytz.timezone(local_tz))

    today_local = datetime.now(pytz.timezone(local_tz))
    start_date = today_local - timedelta(days=days_back)
    end_date = today_local + timedelta(days=days_forward)

    # Filter games in window
    window_games = games_df[(games_df['gameDateTimeLocal'] >= start_date) &
                            (games_df['gameDateTimeLocal'] <= end_date)]

    schedule_dict = {}
    for date, group in window_games.groupby(window_games['gameDateTimeLocal'].dt.date):
        if date == today_local.date():
            date_str = date.strftime('%A, %d %b %Y') + " (Today)"
        else:
            date_str = date.strftime('%A, %d %b %Y')

        schedule_dict[date_str] = []

        for _, row in group.iterrows():
            # Time string
            time_str = row['gameDateTimeLocal'].strftime('%H:%M %Z').split(" ")[0]
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