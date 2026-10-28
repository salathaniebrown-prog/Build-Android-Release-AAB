import http.server
import socketserver
import json
import os
import subprocess
import time

PORT = 8001

class AstraRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/telemetry":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            telemetry_payload = {
                "timestamp": time.time(),
                "system": {
                    "cpu_percent": round((time.time() * 100) % 15 + 5, 1),
                    "ram_percent": 42.5,
                    "ram_used_mb": 1024.0,
                    "bytes_sent": 102400,
                    "bytes_recv": 204800
                },
                "fleet_count": 6
            }
            self.wfile.write(json.dumps(telemetry_payload).encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

        # ROUTE 1: Google AI Studio Endpoint
        if self.path == "/api/generate-image":
            try:
                payload = json.loads(body)
                prompt = payload.get("prompt", "")
                filename = payload.get("filename", "station_render.png")

                result = subprocess.run(
                    ["python3", "generate_image.py", prompt, filename],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                self._send_json({"status": "SUCCESS" if result.returncode == 0 else "FAILED", "stdout": result.stdout.strip()})
            except Exception as e:
                self._send_json({"status": "ERROR", "message": str(e)}, code=500)

        # ROUTE 2: Radium AI Endpoint
        elif self.path == "/api/radium":
            try:
                payload = json.loads(body)
                prompt = payload.get("prompt", "")
                
                result = subprocess.run(
                    ["python3", "radium_client.py", prompt],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                self._send_json({"status": "SUCCESS" if result.returncode == 0 else "FAILED", "stdout": result.stdout.strip()})
            except Exception as e:
                self._send_json({"status": "ERROR", "message": str(e)}, code=500)
        else:
            self.send_response(404)
            self.end_headers()

    def _send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    with ReusableTCPServer(("127.0.0.1", PORT), AstraRequestHandler) as httpd:
        print(f"[ASTRA HYBRID BACKEND]: Server live on http://127.0.0.1:{PORT}")
        httpd.serve_forever()
