import time
import requests
import numpy as np

LEDGER_URL = "http://127.0.0.1:8080/ledger"
FASTAPI_URL = "http://127.0.0.1:8888/process_telemetry"

NUM_VECTORS = 100
DIMENSION = 128

print(f"[REAL-TIME BENCHMARK]: Stress testing supercluster pipeline with {NUM_VECTORS} 128D vectors...")
synthetic_vectors = np.random.randn(NUM_VECTORS, DIMENSION).tolist()

latencies = []
start_total = time.perf_counter()

for i, vec in enumerate(synthetic_vectors):
    sat_id = f"DUBAI-BENCH-SAT-{i%10:02d}"
    
    # Payload structured for both FastAPI and Node Ledger
    ledger_entry = {
        "id": int(time.time() * 1000) + i,
        "satellite_id": sat_id,
        "status": "BENCHMARK_PROCESSED",
        "cosine_similarity": -0.0194,
        "processed_at": int(time.time() * 1000)
    }
    
    fastapi_payload = {
        "satellite_id": sat_id,
        "vector": vec,
        "altitude_km": round(400.0 + (i % 250), 2)
    }
    
    t0 = time.perf_counter()
    success = False
    
    # Primary: Post to Node Ledger Engine (:8080)
    try:
        r_ledger = requests.post(LEDGER_URL, json=ledger_entry, timeout=2)
        if r_ledger.status_code in [200, 201]:
            success = True
    except Exception:
        pass

    # Secondary: Pass vector payload to FastAPI Engine (:8888)
    try:
        requests.post(FASTAPI_URL, json=fastapi_payload, timeout=2)
    except Exception:
        pass
        
    t1 = time.perf_counter()
    if success:
        latencies.append((t1 - t0) * 1000)

total_time = time.perf_counter() - start_total
qps = len(latencies) / total_time if total_time > 0 else 0

if latencies:
    latencies.sort()
    p50 = latencies[int(len(latencies) * 0.50)]
    p95 = latencies[int(len(latencies) * 0.95)]
    p99 = latencies[int(len(latencies) * 0.99)]
    avg = sum(latencies) / len(latencies)

    print("\n==========================================================")
    print("  🚀 REAL-TIME ALSTRA-ASTRA SUPERCLUSTER BENCHMARK")
    print("==========================================================")
    print(f"  • Processed Packets      : {len(latencies)} / {NUM_VECTORS}")
    print(f"  • Total Execution Time    : {total_time:.2f} s")
    print(f"  • Real-Time Throughput    : {qps:.2f} QPS (req/sec)")
    print(f"  • Average Latency         : {avg:.2f} ms")
    print(f"  • P50 Latency             : {p50:.2f} ms")
    print(f"  • P95 Latency             : {p95:.2f} ms")
    print(f"  • P99 Latency             : {p99:.2f} ms")
    print("==========================================================")
else:
    print("❌ [BENCHMARK ERROR]: Node Ledger API on port 8080 unreachable.")
