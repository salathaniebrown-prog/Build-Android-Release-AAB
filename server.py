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
                "fleet_count": 6,
                "satellites": [
                    {"name": "SPACE-ISS-(ZARYA)"},
                    {"name": "SPACE-HUBBLE-ST"},
                    {"name": "SAT-ALSTRA-LEO-01"}
                ]
            }
            self.wfile.write(json.dumps(telemetry_payload).encode("utf-8"))

        elif self.path == "/api/artifacts":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            os.makedirs("./artifacts", exist_ok=True)
            artifacts = []
            for fname in os.listdir("./artifacts"):
                if fname.endswith(".py"):
                    fpath = os.path.join("./artifacts", fname)
                    stat = os.stat(fpath)
                    with open(fpath, "r", encoding="utf-8") as f:
                        code = f.read()
                    artifacts.append({
                        "id": fname[:-3],
                        "filename": fname,
                        "size_bytes": stat.st_size,
                        "code": code
                    })
            self.wfile.write(json.dumps({"status": "SUCCESS", "artifacts": artifacts}).encode("utf-8"))

        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/deploy":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")

            try:
                payload = json.loads(body)
                artifact_id = payload.get("id", "unnamed_artifact")
                code = payload.get("code", "")

                os.makedirs("./artifacts", exist_ok=True)
                file_path = f"./artifacts/{artifact_id}.py"

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)

                result = subprocess.run(
                    ["python3", file_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                response_data = {
                    "status": "SUCCESS" if result.returncode == 0 else "FAILED",
                    "artifact_id": artifact_id,
                    "stdout": result.stdout.strip(),
                    "stderr": result.stderr.strip()
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))

            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ERROR", "message": str(e)}).encode("utf-8"))

        elif self.path == "/api/generate-image":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")

            try:
                payload = json.loads(body)
                prompt = payload.get("prompt", "")
                filename = payload.get("filename", "astra_gen_art.png")

                result = subprocess.run(
                    ["python3", "generate_image.py", prompt],
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                response_data = {
                    "status": "SUCCESS" if result.returncode == 0 else "FAILED",
                    "stdout": result.stdout.strip(),
                    "stderr": result.stderr.strip(),
                    "image_url": f"/{filename}"
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))

            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ERROR", "message": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    with ReusableTCPServer(("127.0.0.1", PORT), AstraRequestHandler) as httpd:
        print(f"[ASTRA BACKEND]: Server live on http://127.0.0.1:{PORT}")
        httpd.serve_forever()
