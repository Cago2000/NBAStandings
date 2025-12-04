import mimetypes
import os
import socket
from utils.loader import *

def start_web_server(template_file, web_port):
    template = load_template(template_file)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', web_port))
    s.listen(5)
    print(f"Web server running on http://0.0.0.0:{web_port}")

    while True:
        cl, addr = s.accept()
        with cl:
            try:
                request = cl.recv(4096).decode()
                if not request:
                    continue
                path = request.split(" ")[1]
                data = {
                    "Standings": load_standings(),
                    "Standings_Predictions": load_standings_predictions(),
                    "MVP_Ladder": load_mvp_ladder(),
                    "MVP_Predictions": load_mvp_predictions(),
                    "Schedule": load_schedule(),
                    "Boxscore": load_boxscores()
                }
                live_data = {
                    "Live_Games": load_live_games(),
                    "Live_Boxscore": load_live_boxscores()
                }
                status = "200 OK"
                match path:
                    case "/":
                        body = template.encode()
                        content_type = "text/html"
                        cache_control = "no-cache, no-store, must-revalidate"
                    case "/data.json":
                        body = json.dumps(data).encode()
                        content_type = "application/json"
                        cache_control = "no-cache, no-store, must-revalidate"
                    case "/live_data.json":
                        body = json.dumps(live_data).encode()
                        content_type = "application/json"
                        cache_control = "no-cache, no-store, must-revalidate"
                    case _:
                        fs_path = path.lstrip("/")
                        file_path = os.path.join("website", fs_path)
                        if os.path.isfile(file_path):
                            with open(file_path, "rb") as f:
                                body = f.read()
                            content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
                            cache_control = "public, max-age=86400"
                        else:
                            body = b"404 Not Found"
                            content_type = "text/plain"
                            status = "404 Not Found"
                            cache_control = "no-cache"

                headers = (
                    f"HTTP/1.1 {status}\r\n"
                    f"Cache-Control: {cache_control}\r\n"
                    f"Content-Type: {content_type}\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    "Connection: close\r\n"
                    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36\r\n"
                    "Accept: application/json, text/plain, */*\r\n"
                    "Accept-Language: en-US,en;q=0.9\r\n"
                    "Origin: https://www.nba.com\r\n"
                    "Referer: https://www.nba.com/\r\n"
                    "\r\n"
                ).encode()
                cl.sendall(headers + body)

            except Exception as e:
                print("Error handling request:", e)