import subprocess
import threading
import time
import shutil
import os
from pathlib import Path

class CloudflareTunnel:
    def __init__(self, tunnel_name, debug=False):
        self.tunnel_name = tunnel_name
        self.process = None
        self.public_url = None
        self.debug = debug

        # Detect correct user config dir (~/.cloudflared)
        self.config_dir = Path.home() / ".cloudflared"

        # Detect creds file inside ~/.cloudflared (UUID.json)
        self.credentials_file = self._find_credentials()

    def _print_debug(self, msg):
        if self.debug:
            print(f"[DEBUG] {msg}")

    def _find_credentials(self):
        """Find the tunnel credentials file inside ~/.cloudflared."""
        if not self.config_dir.exists():
            self._print_debug(f"ERROR: {self.config_dir} directory does not exist.")
            return None

        # Find any file ending in .json (Cloudflare tunnel creds)
        for file in self.config_dir.glob("*.json"):
            self._print_debug(f"Using credentials file: {file}")
            return str(file)

        self._print_debug("ERROR: No tunnel credentials file found in ~/.cloudflared/")
        return None

    def check_cloudflared_installed(self):
        if shutil.which("cloudflared") is None:
            self._print_debug("ERROR: cloudflared is not installed or not in PATH.")
            return False
        self._print_debug("cloudflared binary found.")
        return True

    def start_tunnel(self):
        if not self.check_cloudflared_installed():
            return

        if self.credentials_file is None:
            self._print_debug("ERROR: No credentials file detected. Run `cloudflared tunnel login` first.")
            return

        cmd = [
            "cloudflared",
            "--credentials-file", self.credentials_file,
            "tunnel",
            "run",
            self.tunnel_name
        ]

        while True:
            self._print_debug(f"Starting Cloudflared tunnel '{self.tunnel_name}'...")
            try:
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )

                for line in self.process.stdout:
                    line = line.strip()
                    self._print_debug(f"[cloudflared] {line}")

                    # Extract public URL for quick tunnels or logs
                    if "trycloudflare.com" in line:
                        for part in line.split():
                            if part.startswith("https://"):
                                self.public_url = part
                                self._print_debug(f"Tunnel public URL detected: {self.public_url}")

                self._print_debug("Tunnel exited unexpectedly. Restarting in 5 seconds...")
                time.sleep(5)

            except Exception as e:
                self._print_debug(f"Exception while starting tunnel: {e}")
                time.sleep(5)

    def run_in_background(self):
        self._print_debug("Launching Cloudflare tunnel in background thread...")
        thread = threading.Thread(target=self.start_tunnel, daemon=True)
        thread.start()

    def is_running(self):
        if self.process is None:
            self._print_debug("Tunnel not started yet.")
            return False
        running = self.process.poll() is None
        self._print_debug(f"Tunnel running: {running}")
        return running

    def get_public_url(self):
        if self.public_url:
            self._print_debug(f"Current public URL: {self.public_url}")
        else:
            self._print_debug("Public URL not detected yet.")
        return self.public_url
