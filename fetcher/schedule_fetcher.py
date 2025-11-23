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

    return grouped
