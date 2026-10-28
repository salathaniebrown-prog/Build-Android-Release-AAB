#!/bin/bash
echo "[*] Watchdog daemon activated. Monitoring Uvicorn infrastructure..."

while true; do
    # Check if uvicorn process is currently running
    if ! pgrep -f "uvicorn server:app" > /dev/null; then
        echo "[!] CRASH DETECTED: Uvicorn backend offline at $(date). Reviving..."
        
        # Navigate to workspace, activate environment, and restart headless process
        cd ~/alstra-workspace
        source venv/bin/activate
        nohup uvicorn server:app --host 0.0.0.0 --port 3000 > server.log 2>&1 &
        
        echo "[+] Infrastructure revived successfully."
    fi
    # Wait 10 seconds before inspecting process table again
    sleep 10
done
