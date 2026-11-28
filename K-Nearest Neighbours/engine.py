import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

DATA = [
    {"x": 1.2, "y": 1.5, "label": "A"},
    {"x": 2.0, "y": 2.4, "label": "A"},
    {"x": 3.0, "y": 1.2, "label": "A"},
    {"x": 2.5, "y": 3.2, "label": "A"},
    {"x": 7.0, "y": 7.5, "label": "B"},
    {"x": 8.2, "y": 6.8, "label": "B"},
    {"x": 6.5, "y": 8.5, "label": "B"},
    {"x": 8.5, "y": 8.4, "label": "B"},
    {"x": 5.5, "y": 3.0, "label": "B"},
    {"x": 6.2, "y": 2.0, "label": "B"}
]

def distance(a, b, metric):
    dx = abs(a["x"] - b["x"])
    dy = abs(a["y"] - b["y"])
    if metric == "manhattan":
        return dx + dy
    return (dx ** 2 + dy ** 2) ** 0.5

def predict(x, y, k, metric):
    point = {"x": x, "y": y}
    ranked = []
    for item in DATA:
        ranked.append({
            **item,
            "distance": distance(point, item, metric)
        })
    ranked.sort(key=lambda item: item["distance"])
    neighbors = ranked[:max(1, min(k, len(DATA)))]
    votes = {}
    for item in neighbors:
        votes[item["label"]] = votes.get(item["label"], 0) + 1
    prediction = sorted(votes, key=lambda label: (-votes[label], label))[0]
    return {
        "prediction": prediction,
        "votes": votes,
        "neighbors": neighbors,
        "points": DATA
    }

class Handler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        if urlparse(self.path).path in ("/", "/index.html"):
            content = (Path(__file__).parent / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404)

    def do_POST(self):
        if urlparse(self.path).path != "/predict":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            result = predict(
                float(data["x"]),
                float(data["y"]),
                int(data["k"]),
                data["metric"]
            )
            self.send_json(result)
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            self.send_json({"error": "Invalid input"}, 400)

if __name__ == "__main__":
    print("Open http://localhost:8000")
    HTTPServer(("localhost", 8000), Handler).serve_forever()
