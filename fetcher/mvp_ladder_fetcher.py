import json
import re
from datetime import datetime

from playwright.sync_api import sync_playwright


def get_latest_mvp_ladder_url(base_url="https://www.nba.com/news/category/kia-race-to-the-mvp-ladder"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(base_url, wait_until="domcontentloaded", timeout=60000)

        card = page.query_selector("a[href*='kia-mvp-ladder']")
        if not card:
            browser.close()
            raise ValueError("Could not find MVP Ladder article link")

        href = card.get_attribute("href")
        browser.close()

    return "https://www.nba.com" + href

def fetch_mvp_ladder():
    url = get_latest_mvp_ladder_url()
    if not datetime.now().strftime("%A") in ["Thursday", "Friday", "Saturday"]:
        return None
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