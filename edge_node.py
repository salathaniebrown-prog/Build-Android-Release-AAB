import os
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class EdgeNodeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "status": "ONLINE",
                "node_id": "EDGE-TERMUX-ARM64",
                "uptime": time.time()
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 9000), EdgeNodeHandler)
    print("[EDGE NODE]: Listening on http://127.0.0.1:9000")
    server.serve_forever()
