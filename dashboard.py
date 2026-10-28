import time
import requests
import os

def check_endpoint(url):
    try:
        r = requests.get(url, timeout=1)
        return "ONLINE" if r.status_code == 200 else f"ERR ({r.status_code})"
    except Exception:
        return "OFFLINE"

while True:
    os.system("clear")
    print("==========================================================")
    print("  📡 ALSTRA-ASTRA REAL-TIME DEEPSPACE COMMAND CENTER")
    print("==========================================================")
    
    # 1. Fetch Node Ledger Metrics
    ledger_status = check_endpoint("http://127.0.0.1:8080/ledger/stats")
    total_records = "N/A"
    avg_sim = "N/A"
    
    if ledger_status == "ONLINE":
        try:
            res = requests.get("http://127.0.0.1:8080/ledger/stats", timeout=1).json()
            total_records = res.get("total_records", "N/A")
            avg_sim = f"{res.get('avg_similarity', 0):.4f}"
        except Exception:
            pass

    # 2. Fetch FastAPI Vector Engine Metrics
    fastapi_status = check_endpoint("http://127.0.0.1:8888/docs")

    print(f"  • Node Ledger Engine (:8080) : {ledger_status}")
    print(f"  • FastAPI Vector Engine (:8888): {fastapi_status}")
    print("----------------------------------------------------------")
    print(f"  • Total Ledger Records Persisted: {total_records}")
    print(f"  • Cluster Mean Vector Sim       : {avg_sim}")
    print("==========================================================")
    print("  [Ctrl+C to exit dashboard view]")
    time.sleep(2)
