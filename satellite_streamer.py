import requests
import time
import random

API_TARGET = "http://127.0.0.1:8090/node/telemetry"

session_counter = 0

while True:
    session_counter += 1
    sat_num = random.randint(1, 25)
    sat_id = f"SOVEREIGN-SAT-{sat_num:02d}"

    # Matches NodeStatePayload Pydantic schema expected by FastAPI /node/telemetry
    payload = {
        "node_id": sat_id,
        "architecture": "aarch64",
        "adb_status": "CONNECTED",
        "uvicorn_core": "STABLE",
        "vnc_runtime": "JETI_RECURSIVE_SUPERCOMPUTE"
    }

    try:
        response = requests.post(API_TARGET, json=payload, timeout=2)
        if response.status_code in (200, 201):
            print(f"🚀 [TX {session_counter:04d} SUCCESS] Streamed: {sat_id} -> Status {response.status_code}")
        else:
            print(f"⚠️ [UPLINK WARNING]: Frame dropped by edge node. HTTP Status: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ [UPLINK DISCONNECTED]: Cannot reach Core Gateway. Retrying frame sync...")

    time.sleep(1.2)
