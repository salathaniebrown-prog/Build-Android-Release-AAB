#!/bin/bash

echo "=== ALSTRA-ASTRA CLUSTER BOOTSTRAP ==="

# 1. Enforce Clean Sockets
echo "[BOOT]: Clearing active socket locks on ports 8080 & 8888..."
fuser -k 8080/tcp 8888/tcp >/dev/null 2>&1 || true
pkill -f "node ledger_server.js" >/dev/null 2>&1 || true
pkill -f "uvicorn main:app" >/dev/null 2>&1 || true
sleep 1

# 2. Verify Python Dependencies
echo "[BOOT]: Verifying self-healing Python dependencies..."
python3 bootstrap.py

# 3. Launch Node.js Zero-Dependency Ledger Server (Port 8080)
echo "[BOOT]: Starting Node.js Ledger Server on :8080..."
nohup node ledger_server.js > ledger.log 2>&1 &
sleep 1

# 4. Launch FastAPI Vector Engine (Port 8888)
echo "[BOOT]: Starting FastAPI Vector Engine on :8888..."
nohup uvicorn main:app --host 0.0.0.0 --port 8888 > api.log 2>&1 &
sleep 2

# 5. Cluster Diagnostics Check
echo "[BOOT]: Verifying active services..."
LEDGER_CHECK=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/ledger/stats)
API_CHECK=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8888/docs)

if [ "$LEDGER_CHECK" == "200" ] && [ "$API_CHECK" == "200" ]; then
    echo "=========================================================="
    echo "  ✅ ALSTRA-ASTRA CLUSTER ONLINE AND OPERATIONAL"
    echo "  • Node Ledger Engine  : http://127.0.0.1:8080"
    echo "  • FastAPI Vector API  : http://127.0.0.1:8888"
    echo "  • Logs: tail -f ledger.log | tail -f api.log"
    echo "=========================================================="
else
    echo "❌ [ERROR]: Engine initialization failed."
fi
