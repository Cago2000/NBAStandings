import os
import json
import threading
from fetcher.auto_update import auto_update_standings
from server.web_server import start_web_server
from utils.logger import setup_logging
from cloudflare.cloudflare_tunnel import CloudflareTunnel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "jsons/config.json")

with open(CONFIG_FILE) as f:
    config = json.load(f)

DATA_DIR = os.path.join(BASE_DIR, "jsons")
os.makedirs(DATA_DIR, exist_ok=True)

LOG_FILE = os.path.join(BASE_DIR, "logs/fetcher.log")
setup_logging(LOG_FILE)

OUTPUT_FILE = os.path.join(DATA_DIR, "standings.json")
PORT = config.get("pc_port", 8000)
UPDATE_INTERVAL = config.get("update_interval", 600)

# === Start auto-update thread ===
threading.Thread(target=auto_update_standings, args=(OUTPUT_FILE, UPDATE_INTERVAL), daemon=True).start()

# === Start Cloudflared tunnel in background ===
tunnel = CloudflareTunnel(tunnel_name="nba-standings", debug=False)
tunnel.run_in_background()

# === Start web server ===
start_web_server(OUTPUT_FILE, os.path.join(BASE_DIR, "template.html"), PORT)
