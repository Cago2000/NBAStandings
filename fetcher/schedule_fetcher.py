from datetime import datetime, timedelta, time
import pandas as pd
import pytz
from nba_api.stats.endpoints import ScheduleLeagueV2

def fetch_schedule(days_back=1, days_forward=2):
    schedule = ScheduleLeagueV2()
    games_df = schedule.season_games.get_data_frame()

    # Convert UTC datetime
    games_df['gameDateTimeUTC'] = pd.to_datetime(games_df['gameDateTimeUTC'], utc=True)

    eastern = pytz.timezone("US/Eastern")
    germany = pytz.timezone("Europe/Berlin")
    today_eastern = datetime.now(eastern).date()

    start_day = today_eastern - timedelta(days=days_back)
    end_day = today_eastern + timedelta(days=days_forward)

    start_utc = eastern.localize(datetime.combine(start_day, time(0, 0))).astimezone(pytz.UTC)
    end_utc = eastern.localize(datetime.combine(end_day, time(23, 59, 59))).astimezone(pytz.UTC)

    window_games = games_df[
        (games_df['gameDateTimeUTC'] >= start_utc) &
        (games_df['gameDateTimeUTC'] <= end_utc)
    ].copy()

    # Day tags
    day_tags = {0: " (Mo)", 1: " (Tu)", 2: " (We)", 3: " (Th)", 4: " (Fr)", 5: " (Sa)", 6: " (So)"}

    grouped = {}
    for date, group in window_games.groupby(window_games['gameDateTimeUTC'].apply(lambda x: x.astimezone(eastern).date())):
        date_str = date.strftime('%A, %d %b %Y')
        if date == today_eastern:
            date_str += " (Today)"

        games_list = []
        for _, row in group.iterrows():
            game_time_germany = row['gameDateTimeUTC'].tz_convert(germany)
            time_germany_str = game_time_germany.strftime('%H:%M')

            # Compute day_overlap_tag using one-liner
            game_time_est = row['gameDateTimeUTC'].tz_convert(eastern)
            game_time_utc = row['gameDateTimeUTC']
            day_overlap_tag = day_tags[(game_time_est.weekday() + 1) % 7] if game_time_est.date() != game_time_utc.date() else ""

            games_list.append({
                "time": time_germany_str + day_overlap_tag,
                "home": row['homeTeam_teamTricode'],
                "away": row['awayTeam_teamTricode'],
                "game_status": row['gameStatusText'],
                "home_score": row['homeTeam_score'],
                "away_score": row['awayTeam_score'],
            })

        grouped[date_str] = games_list

    return grouped
