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
                    "Standings": load_standings("jsons/standings.json"),
                    "Standings_Predictions": load_standings_predictions("jsons/standings_predictions.json"),
                    "MVP_Ladder": load_mvp_ladder("jsons/mvp_ladder.json"),
                    "MVP_Predictions": load_mvp_predictions("jsons/mvp_predictions.json")
                }

                match path:
                    case "/":
                        body = template.encode()
                        content_type = "text/html"
                    case "/data.json":
                        body = json.dumps(data).encode()
                        content_type = "application/json"
                    case _:
                        fs_path = path.lstrip("/")
                        file_path = os.path.join("website", fs_path)
                        if os.path.isfile(file_path):
                            with open(file_path, "rb") as f:
                                body = f.read()
                            content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
                        else:
                            body = b"404 Not Found"
                            content_type = "text/plain"

                headers = (
                    f"HTTP/1.1 {'200 OK' if path in ['/', '/data.json', '/style.css', '/app.js'] else '404 Not Found'}\r\n"
                    f"Content-Type: {content_type}\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Connection: close\r\n\r\n"
                ).encode()

                cl.sendall(headers + body)

            except Exception as e:
                print("Error handling request:", e)
