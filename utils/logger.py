import sys
import threading
import os
from datetime import datetime


class Logger:
    _lock = threading.Lock()
    def __init__(self, path, original_stream, max_size_mb=10):
        self.path = path
        self.original_stream = original_stream
        self.max_size = max_size_mb * 1024 * 1024

    def _rotate_if_needed(self):
        if not os.path.exists(self.path):
            return

        if os.path.getsize(self.path) > self.max_size:
            backup_path = f"{self.path}.old"
            if os.path.exists(backup_path):
                os.remove(backup_path)
            os.rename(self.path, backup_path)

    def write(self, msg):
        with Logger._lock:
            if msg.strip():
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                thread_name = threading.current_thread().name

                # Ensure single newline
                if not msg.endswith("\n"):
                    msg += "\n"

                formatted_msg = f"[{timestamp}] [{thread_name}] {msg}"

                self._rotate_if_needed()

                with open(self.path, "a", encoding="utf-8") as f:
                    f.write(formatted_msg)

                if self.original_stream:
                    self.original_stream.write(formatted_msg)
            else:
                if self.original_stream:
                    self.original_stream.write(msg)

    def flush(self):
        if self.original_stream:
            self.original_stream.flush()


def setup_logging(log_file, max_size_mb=10):
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    sys.stdout = Logger(log_file, original_stdout, max_size_mb)
    sys.stderr = Logger(log_file, original_stderr, max_size_mb)