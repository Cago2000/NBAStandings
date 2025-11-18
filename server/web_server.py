import socket
import json
from utils.loader import *

def start_web_server(template_file, web_port):
    template = load_template(template_file)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', web_port))
    s.listen(5)
    print(f"Web server running on http://localhost:{web_port}")

    while True:
        cl, addr = s.accept()
        with cl:
            try:
                request = cl.recv(2048).decode()
                path = request.split(" ")[1]  # extract requested path

                data = {
                    "Standings": load_standings("jsons/standings.json"),
                    "Standings_Predictions": load_standings_predictions("jsons/standings_predictions.json"),
                    "MVP_Ladder": load_mvp_ladder("jsons/mvp_ladder.json"),
                    "MVP_Predictions": load_mvp_predictions("jsons/mvp_predictions.json")
                }

                if path == "/data.json":
                    cl.send(b"HTTP/1.0 200 OK\r\nContent-Type: application/json\r\n\r\n")
                    cl.send(json.dumps(data).encode())

                elif path == "/style.css":
                    with open("website/style.css", "rb") as f:
                        cl.send(b"HTTP/1.0 200 OK\r\nContent-Type: text/css\r\n\r\n")
                        cl.send(f.read())

                elif path == "/app.js":
                    with open("website/app.js", "rb") as f:
                        cl.send(b"HTTP/1.0 200 OK\r\nContent-Type: application/javascript\r\n\r\n")
                        cl.send(f.read())

                else:
                    cl.send(b"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n")
                    cl.send(template.encode())

            except Exception as e:
                print("Error handling request:", e)
