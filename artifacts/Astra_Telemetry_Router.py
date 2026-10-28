# ASTRA TELEMETRY ROUTER ARTIFACT
import psutil, json, time

def route_telemetry():
    psutil.cpu_percent(interval=None)
    time.sleep(0.1)
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory()
    payload = {
        "timestamp": round(time.time(), 2),
        "cpu_load_pct": cpu,
        "ram_used_mb": round(ram.used / (1024 * 1024), 2),
        "target_endpoint": "127.0.0.1:8001/api/telemetry"
    }
    print("[ASTRA TELEMETRY ROUTER]: Live metrics sampled ->", json.dumps(payload))
    return payload

if __name__ == "__main__":
    route_telemetry()