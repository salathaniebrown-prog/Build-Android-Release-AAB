import requests
import os
import time
import subprocess

def check_service(url, name):
    try:
        r = requests.get(url, timeout=2)
        print(f"[WATCHDOG]: {name} operational ({r.status_code})")
        return True
    except Exception:
        print(f"[WATCHDOG WARNING]: {name} un-responsive.")
        return False

if __name__ == "__main__":
    node_ok = check_service("http://127.0.0.1:8080/ledger/stats", "Node Ledger Engine")
    
    if not node_ok:
        print("[WATCHDOG]: Recovering Node Ledger Service...")
        os.system("pkill -f node")
        os.system("nohup node ledger_server.js > ledger.log 2>&1 &")
