import requests
import numpy as np

URL = "http://127.0.0.1:8888/telemetry/analyze"

clean_vec = np.random.normal(0, 1, 128).tolist()
res_clean = requests.post(URL, json={
    "satellite_id": "SAT-ALSTRA-LEO-01",
    "orbit_altitude_km": 542.8,
    "embedding_vector": clean_vec
}).json()

print("--- TEST 1: NOMINAL INGESTION ---")
print(res_clean)

corrupted_vec = (np.random.normal(10, 5, 128)).tolist()
res_anomaly = requests.post(URL, json={
    "satellite_id": "SAT-ALSTRA-LEO-99",
    "orbit_altitude_km": 510.2,
    "embedding_vector": corrupted_vec
}).json()

print("\n--- TEST 2: ANOMALY DETECTION INGESTION ---")
print(res_anomaly)
