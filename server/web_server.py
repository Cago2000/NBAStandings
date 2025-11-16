import socket
import json

def load_template(template_file):
    try:
        with open(template_file) as f:
            return f.read()
    except Exception as e:
        print("Template load error:", e)
        return "<html><body><p>Template error</p></body></html>"

def load_predictions(pred_file):
    try:
        with open(pred_file) as f:
            return json.load(f)
    except Exception:
        return {u: {"East": [], "West": []} for u in ["Can", "Marlon", "Ole"]}

def build_table_html(truth_data, predictions_data, conf):
    html_rows = {}
    # ... same as your previous build_table_html function
    return html_rows

def start_web_server(json_file, template_file, web_port):
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
                with open(json_file) as f:
                    truth_data = json.load(f)

                predictions_data = load_predictions("jsons/predictions.json")
                combined_data = truth_data.copy()
                combined_data.update(predictions_data)

                if "GET /standings.json" in request:
                    cl.send(b"HTTP/1.0 200 OK\r\nContent-Type: application/json\r\n\r\n")
                    cl.send(json.dumps(combined_data).encode())
                else:
                    html = template
                    for conf in ["East", "West"]:
                        rows = build_table_html(truth_data, predictions_data, conf)
                        for key, v in rows.items():
                            html = html.replace(f"{{{{{key}}}}}", v)
                    cl.send(b"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n")
                    cl.send(html.encode())
            except Exception as e:
                print("Error handling request:", e)
