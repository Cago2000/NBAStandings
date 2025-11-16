import subprocess
import threading
import time
import shutil

class CloudflareTunnel:
    def __init__(self, tunnel_name, debug=False):
        self.tunnel_name = tunnel_name
        self.process = None
        self.public_url = None
        self.debug = debug

    def _print_debug(self, msg):
        if self.debug:
            print(f"[DEBUG] {msg}")

    def check_cloudflared_installed(self):
        """Verify that the cloudflared binary is installed and executable."""
        if shutil.which("cloudflared") is None:
            self._print_debug("ERROR: cloudflared is not installed or not in PATH.")
            return False
        self._print_debug("cloudflared binary found.")
        return True

    def start_tunnel(self):
        """Start Cloudflared tunnel and parse public URL if using quick tunnel."""
        if not self.check_cloudflared_installed():
            return

        cmd = ["cloudflared", "tunnel", "run", self.tunnel_name]

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

                    # Detect the public URL in logs
                    if "https://" in line and ".trycloudflare.com" in line:
                        self.public_url = line.split()[0]
                        self._print_debug(f"Tunnel public URL detected: {self.public_url}")

                self._print_debug("Tunnel process exited unexpectedly, restarting in 5 seconds...")
                time.sleep(5)

            except Exception as e:
                self._print_debug(f"Exception while starting tunnel: {e}")
                time.sleep(5)

    def run_in_background(self):
        self._print_debug("Launching Cloudflare tunnel in background thread...")
        thread = threading.Thread(target=self.start_tunnel, daemon=True)
        thread.start()

    def is_running(self):
        """Check if the tunnel process is still running."""
        if self.process is None:
            self._print_debug("Tunnel process not started yet.")
            return False
        running = self.process.poll() is None
        self._print_debug(f"Tunnel running: {running}")
        return running

    def get_public_url(self):
        """Return the current public URL (if detected)."""
        if self.public_url:
            self._print_debug(f"Current public URL: {self.public_url}")
        else:
            self._print_debug("Public URL not detected yet.")
        return self.public_url
