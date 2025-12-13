import sys
import threading
from datetime import datetime


class Logger:
    def __init__(self, path, original_stream):
        self.path = path
        self.original_stream = original_stream

    def write(self, msg):
        if msg.strip():
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            thread_name = threading.current_thread().name
            formatted_msg = f"[{timestamp}] [{thread_name}] {msg}"

            with open(self.path, "a", encoding="utf-8") as f:
                f.write(formatted_msg)

            if self.original_stream:
                self.original_stream.write(formatted_msg)
        else:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(msg)
            if self.original_stream:
                self.original_stream.write(msg)

    def flush(self):
        if self.original_stream:
            self.original_stream.flush()


def setup_logging(log_file):
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    sys.stdout = Logger(log_file, original_stdout)
    sys.stderr = Logger(log_file, original_stderr)