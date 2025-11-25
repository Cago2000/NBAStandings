import threading
from server.web_server import start_web_server
from fetcher.auto_update import *
from utils.logger import setup_logging
from cloudflare.cloudflare_tunnel import CloudflareTunnel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(BASE_DIR, "jsons/config.json")
with open(CONFIG_FILE) as f:
    config = json.load(f)

LOG_FILE = os.path.join(BASE_DIR, "logs/fetcher.log")
if config["log_to_file"]:
    setup_logging(LOG_FILE)

# === Init JSON Paths ===
STANDINGS_OUTPUT_FILE = "jsons/standings.json"
MVP_LADDER_OUTPUT_FILE = "jsons/mvp_ladder.json"
SCHEDULE_OUTPUT_FILE = "jsons/schedule.json"
LIVE_GAMES_OUTPUT_FILE = "jsons/live_games.json"
BOXSCORE_OUTPUT_FILE = "jsons/boxscores.json"

# === Start auto-update threads ===
threading.Thread(target=auto_update_standings, args=(STANDINGS_OUTPUT_FILE, 60), daemon=True).start()
#threading.Thread(target=auto_update_mvp_ladder, args=(MVP_LADDER_OUTPUT_FILE, 3600), daemon=True).start()
threading.Thread(target=auto_update_schedule, args=(SCHEDULE_OUTPUT_FILE, 60), daemon=True).start()
threading.Thread(target=auto_update_live_games, args=(LIVE_GAMES_OUTPUT_FILE, 0.5), daemon=True).start()

# === Start Cloudflared tunnel in background ===
tunnel = CloudflareTunnel(tunnel_name="nba-standings", debug=True)
tunnel.run_in_background()

# === Start web server ===
start_web_server("website/index.html", config.get("pc_port", 8000))

