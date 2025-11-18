import json
import re
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

def get_mvp_ladder_url():
    date_obj = datetime.strptime("2025-11-07", "%Y-%m-%d")
    today = datetime.today()
    latest_date = date_obj
    while date_obj <= today:
        latest_date = date_obj
        date_obj += timedelta(days=7)
    return f"https://www.nba.com/news/kia-mvp-ladder-{latest_date.strftime('%b-%d-%Y').lower()}"

def fetch_mvp_ladder():
    url = get_mvp_ladder_url()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        page.wait_for_selector("article")
        article_text = page.query_selector("article").inner_text()

        pattern = r"(?m)^([1-9][0-9]?)\.\s+([^\n,–]+)[,–]?\s*(.*)$"
        matches = re.findall(pattern, article_text)

        ladder_data = []
        for rank, player, info in matches[:5]:
            ladder_data.append({
                "rank": int(rank),
                "player": player.strip(),
                "team": info.strip() if info else None
            })
        with open("jsons/mvp_ladder.json", "w", encoding="utf-8") as f:
            json.dump(ladder_data, f, ensure_ascii=False, indent=2)
        browser.close()
        return ladder_data