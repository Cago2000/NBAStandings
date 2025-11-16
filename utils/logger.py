import sys

class Logger:
    def __init__(self, path):
        self.path = path

    def write(self, msg):
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(msg)

    def flush(self):
        pass

def setup_logging(log_file):
    sys.stdout = Logger(log_file)
    sys.stderr = Logger(log_file)
