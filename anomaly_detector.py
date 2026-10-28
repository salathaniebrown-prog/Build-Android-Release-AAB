import time
import requests
import json

GATEWAY_URL = "http://127.0.0.1:8090"
COMMAND_CENTER_URL = "http://127.0.0.1:3000/api/fast"

def run_anomaly_check():
    try:
        res = requests.get(GATEWAY_URL, timeout=3)
        data = res.json()
        cluster = data.get("cluster_matrix", {})
        
        high_load_nodes = []
        for node_id, info in cluster.items():
            if info.get("load_pct", 0) > 85.0:
                high_load_nodes.append((node_id, info.get("load_pct")))
                
        if high_load_nodes:
            prompt = f"ALERT: High load detected on supercompute nodes: {high_load_nodes}. Generate autonomous mitigation and load re-balancing steps."
            requests.post(COMMAND_CENTER_URL, json={"command": prompt}, timeout=5)
            print(f"🤖 [AI BRAIN TRIGGERED]: Sent anomaly alert for {len(high_load_nodes)} node(s).")
    except Exception as e:
        pass

if __name__ == "__main__":
    while True:
        run_anomaly_check()
        time.sleep(10)
