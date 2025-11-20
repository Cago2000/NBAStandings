import json
import re
import time
from datetime import datetime, timedelta, timezone
from time import sleep

from playwright.sync_api import sync_playwright


def get_latest_mvp_ladder_url(base_url="https://www.nba.com/news/category/kia-race-to-the-mvp-ladder", weeks_back=2):
    today = datetime.now(timezone.utc).date()
    cutoff_date = today - timedelta(weeks=weeks_back)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(base_url, wait_until="domcontentloaded", timeout=60000)
        sleep(2)
        article = page.query_selector("article") or page.query_selector("main") or page.query_selector("div.article__content")
        if not article:
            browser.close()
            raise ValueError("No article or main content element found on page")
        text = article.inner_text()
        browser.close()
    dates = re.findall(
        r"(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}",
        text
    )
    if not dates:
        raise ValueError("No dates found in page content")
    date_objs = [datetime.strptime(d, "%B %d, %Y").date() for d in dates]
    recent_dates = [d for d in date_objs if cutoff_date <= d <= today]
    if not recent_dates:
        raise ValueError(f"No MVP ladder dates found in the last {weeks_back} weeks")
    latest_date = max(recent_dates)
    url_date = latest_date - timedelta(days=1)
    url = f"https://www.nba.com/news/kia-mvp-ladder-{url_date.strftime('%b-%d-%Y').lower()}"
    return url

def fetch_mvp_ladder():
    url = get_latest_mvp_ladder_url()
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