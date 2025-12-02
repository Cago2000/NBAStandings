import threading
from server.web_server import start_web_server
from fetcher.auto_update import *
from utils.logger import setup_logging
from cloudflare.cloudflare_tunnel import CloudflareTunnel
import socket

print("Running on:", socket.gethostname())

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(BASE_DIR, "jsons/config.json")
with open(CONFIG_FILE) as f:
    config = json.load(f)

LOG_FILE = os.path.join(BASE_DIR, "logs/fetcher.log")
if config["log_to_file"]:
    setup_logging(LOG_FILE)


# === Start auto-update threads ===
threading.Thread(target=auto_update_standings, args=(60,), daemon=True).start()
threading.Thread(target=auto_update_mvp_ladder, args=(3600,), daemon=True).start()
threading.Thread(target=auto_update_schedule, args=(60,), daemon=True).start()
threading.Thread(target=auto_update_live_games, args=(0.5,), daemon=True).start()
threading.Thread(target=auto_update_boxscores, args=(2,), daemon=True).start()
threading.Thread(target=auto_update_live_boxscores, args=(5,), daemon=True).start()

# === Start Cloudflared tunnel in background ===
tunnel = CloudflareTunnel(tunnel_name="nba-standings", debug=False)
tunnel.run_in_background()

# === Start web server ===
start_web_server("website/index.html", config.get("pc_port", 8000))

