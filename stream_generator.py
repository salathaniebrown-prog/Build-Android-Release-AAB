import time
import random
import requests
import numpy as np

API_URL = "http://127.0.0.1:8888/telemetry/analyze"
SATELLITE_FLEET = [f"SAT-ALSTRA-LEO-{i:02d}" for i in range(1, 11)]

print("[STREAM GENERATOR]: Starting live telemetry transmission pipeline...")
print("[STREAM GENERATOR]: Streaming 128D vector payloads every 500ms. Press Ctrl+C to stop.\n")

packet_count = 0

try:
    while True:
        packet_count += 1
        sat_id = random.choice(SATELLITE_FLEET)
        altitude = round(random.uniform(500.0, 600.0), 2)
        
        # 85% chance clean transmission signal, 15% noise distortion anomaly
        is_simulated_anomaly = random.random() < 0.15
        
        if is_simulated_anomaly:
            # Shift signal variance to simulate telemetry perturbation
            vector = np.random.normal(5.0, 3.0, 128).tolist()
        else:
            vector = np.random.normal(0, 1, 128).tolist()

        payload = {
            "satellite_id": sat_id,
            "orbit_altitude_km": altitude,
            "embedding_vector": vector
        }

        start_time = time.perf_counter()
        response = requests.post(API_URL, json=payload, timeout=2)
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        if response.status_code == 200:
            res_json = response.json()
            flag = "⚠️ ANOMALY DETECTED" if res_json.get("anomaly_flag") else "✅ NOMINAL SIGNAL"
            print(f"[STREAM #{packet_count:04d}]: {sat_id} | Alt: {altitude}km | Stat: {res_json.get('status')} | Sim: {res_json.get('cosine_similarity')} | Exec: {elapsed_ms:.2f}ms | {flag}")
        else:
            print(f"[STREAM ERROR]: HTTP {response.status_code} - {response.text}")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n[STREAM GENERATOR]: Pipeline terminated cleanly by user.")
