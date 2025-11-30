import os
import json
import re
from datetime import datetime
from playwright.sync_api import sync_playwright

# Batch size for processing HTML lines
BATCH_SIZE = 50

# Regex to match both HTML formats:
H3_SPAN_PATTERN = re.compile(
    r'<h3[^>]*>\s*'
    r'(?:<span[^>]*>(\d+)\.\s*</span>\s*<span[^>]*>([^<]+)</span>'
    r'|<span[^>]*>(\d+)\.\s*([^<]+)</span>)'
    r'.*?</h3>',
    re.DOTALL
)


def get_latest_mvp_ladder_url(base_url="https://www.nba.com/news/category/kia-race-to-the-mvp-ladder"):
    with sync_playwright() as p:
        request_context = p.request.new_context()
        response = request_context.get(base_url)
        html = response.text()
        request_context.dispose()

    match = re.search(r'href="([^"]*kia-mvp-ladder[^"]*)"', html)
    if not match:
        raise ValueError("Could not find MVP Ladder article link")

    href = match.group(1)
    if not href.startswith("http"):
        href = "https://www.nba.com" + href

    return href


def fetch_mvp_ladder():
    today = datetime.now().strftime("%A")
    if today not in ["Thursday", "Friday", "Saturday"]:
        return None

    url = get_latest_mvp_ladder_url()
    with sync_playwright() as p:
        request_context = p.request.new_context()
        response = request_context.get(url)
        html = response.text()
        request_context.dispose()

    lines = html.splitlines()
    ladder_data = []

    for i in range(0, len(lines), BATCH_SIZE):
        batch_lines = lines[i:i + BATCH_SIZE]
        batch_text = "\n".join(batch_lines)
        matches = H3_SPAN_PATTERN.findall(batch_text)

        for m in matches:
            if m[0] and m[1]:
                rank = int(m[0])
                player_team = m[1]
            else:
                rank = int(m[2])
                player_team = m[3]

            if ',' in player_team:
                player, team = [s.strip() for s in player_team.split(',', 1)]
            else:
                player, team = player_team.strip(), None

            ladder_data.append({
                "rank": rank,
                "player": player,
                "team": team
            })

    ladder_data = ladder_data[:5]
    return ladder_data if ladder_data is not None else None