#!/bin/bash
# ALSTRA DATACENTER CORE STARTUP DAEMON
echo "=================================================="
echo "🚀 INITIALIZING ALSTRA AI SUPER DATACENTER CORE"
echo "=================================================="

# Step 1: Forcefully purge existing port binds
echo "🧹 Clearing network socket locks on 3000, 8090, 8095..."
pkill -9 -f vector_datacenter_core.py 2>/dev/null
pkill -9 -f satellite_streamer.py 2>/dev/null
pkill -9 -f uvicorn 2>/dev/null
pkill -9 -f node 2>/dev/null

# Step 2: Spin up the core database layer
echo "🧠 Activating AI Vector Engine Matrix (Port 8095)..."
nohup python3 ~/alstra-workspace/vector_datacenter_core.py > ~/alstra-workspace/vector_core.log 2>&1 &

# Give the python sockets a moment to securely bind
sleep 2

# Step 3: Spin up the live telemetry array
echo "📡 Engaging Sovereign Satellite Streamer (Port 3000)..."
nohup python3 ~/alstra-workspace/satellite_streamer.py > ~/alstra-workspace/satellite_uplink.log 2>&1 &

sleep 2

# Step 4: Verify health checks
echo "🛡️ Running internal infrastructure validation loop..."
STATUS_3000=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:3000)
if [ "$STATUS_3000" == "200" ] || [ "$STATUS_3000" == "404" ]; then
    echo "✅ Cluster Operational. Streaming live telemetry feeds."
else
    echo "⚠️ Sockets active but unverified. Monitoring required."
fi

echo "=================================================="
echo "📊 Tailing satellite_uplink.log (Press CTRL+C to exit background shell)"
echo "=================================================="
tail -f ~/alstra-workspace/satellite_uplink.log

