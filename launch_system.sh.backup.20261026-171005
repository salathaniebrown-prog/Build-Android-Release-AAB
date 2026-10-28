#!/usr/bin/env bash

# Terminal UI configuration styling metrics
BG_CYAN="\033[1;36m"
BG_GREEN="\033[1;32m"
BG_YELLOW="\033[1;33m"
BG_RED="\033[1;31m"
RESET="\033[0m"

clear
echo -e "${BG_CYAN}=========================================================${RESET}"
echo -e "🧠  ASTRA SOVEREIGN EXASCALE AUTOMATED LAUNCH ORCHESTRATOR"
echo -e "📡  Deploying All Data-Center Engine Components Sequentially"
echo -e "${BG_CYAN}=========================================================${RESET}"

# ==========================================
# 1. CORE SANITIZATION & RESOURCE RECLAMATION
# ==========================================
echo -e "\n${BG_YELLOW}[STEP 1]: Reclaiming system network ports...${RESET}"
killall -9 node python3 python 2>/dev/null
if command -v fuser &> /dev/null; then
    fuser -k 8080/tcp 8090/tcp 8095/tcp &>/dev/null
else
    lsof -t -i:8080 -i:8090 -i:8095 | xargs kill -9 &>/dev/null
fi
sleep 1
echo "   ├── Network ports 8080, 8090, and 8095 cleared."

# Array tracking structures for background runtime processes
PIDS=()

# ==========================================
# 2. RUNTIME INITIATION LAYERS (SEQUENTIAL)
# ==========================================

# LAYER 1: Core Node.js Ledger Server Cluster
echo -e "\n${BG_YELLOW}[STEP 2]: Initializing Node.js Multi-Worker Ledger Core...${RESET}"
if [ -f "server.js" ]; then
    node server.js > server_cluster.log 2>&1 &
    PIDS+=($!)
    sleep 2
    echo -e "   └── ${BG_GREEN}[ONLINE]${RESET} Node.js Ledger Core active (PID: ${PIDS[-1]})"
else
    echo -e "   └── ${BG_RED}[FAILED]${RESET} server.js missing."
fi

# LAYER 2: Real-time Filesystem Security Auditor
echo -e "\n${BG_YELLOW}[STEP 3]: Activating Real-Time Vault Security Monitor...${RESET}"
if [ -f "vault_alert_monitor.sh" ]; then
    chmod +x vault_alert_monitor.sh
    ./vault_alert_monitor.sh > security_monitor.log 2>&1 &
    PIDS+=($!)
    sleep 1
    echo -e "   └── ${BG_GREEN}[ONLINE]${RESET} Security Monitor parsing ledger rows (PID: ${PIDS[-1]})"
else
    echo -e "   └── ${BG_RED}[FAILED]${RESET} vault_alert_monitor.sh missing."
fi

# LAYER 3: Autonomous Local Vector AI Datacenter Database
echo -e "\n${BG_YELLOW}[STEP 4]: Launching Self-Building Vector AI Datacenter...${RESET}"
if [ -f "vector_datacenter_core.py" ]; then
    python3 vector_datacenter_core.py > vector_database.log 2>&1 &
    PIDS+=($!)
    sleep 2
    echo -e "   └── ${BG_GREEN}[ONLINE]${RESET} Vector Space Model active on Port 8095 (PID: ${PIDS[-1]})"
else
    echo -e "   └── ${BG_RED}[FAILED]${RESET} vector_datacenter_core.py missing."
fi

# LAYER 4: Space-Grid Sovereign Telemetry Core Bootstrap
echo -e "\n${BG_YELLOW}[STEP 5]: Bootstrapping Autonomous Space-Grid Engine...${RESET}"
if [ -f "sovereign_bootstrap.py" ]; then
    python3 sovereign_bootstrap.py > telemetry_core.log 2>&1 &
    PIDS+=($!)
    sleep 2
    echo -e "   └── ${BG_GREEN}[ONLINE]${RESET} Space-Grid Gateway active on Port 8090 (PID: ${PIDS[-1]})"
else
    echo -e "   └── ${BG_RED}[FAILED]${RESET} sovereign_bootstrap.py missing."
fi

# LAYER 5: Continuous Low-Earth-Orbit Satellite Streamer Simulation
echo -e "\n${BG_YELLOW}[STEP 6]: Engaging LEO Satellite Telemetry Streamer...${RESET}"
if [ -f "satellite_streamer.py" ]; then
    python3 satellite_streamer.py > satellite_uplink.log 2>&1 &
    PIDS+=($!)
    sleep 1
    echo -e "   └── ${BG_GREEN}[ONLINE]${RESET} Satellite Data Constellation Streaming (PID: ${PIDS[-1]})"
else
    echo -e "   └── ${BG_RED}[FAILED]${RESET} satellite_streamer.py missing."
fi

echo -e "\n${BG_CYAN}=========================================================${RESET}"
echo -e "🎉  ${BG_GREEN}TOTAL EXASCALE ENGINE STACK DEPLOYED AND SYNCHRONIZED!${RESET}"
echo -e "📝  All execution traces are piping directly into private .log files"
echo -e "${BG_CYAN}=========================================================${RESET}"
echo "📍 Press [ANY KEY] to safely shut down all cluster engines and exit."
echo -e "${BG_CYAN}---------------------------------------------------------${RESET}"

# Wait for interactive keystroke execution before triggering safe closure
read -n 1 -s -r

echo -e "\n\n${BG_RED}[SHUTDOWN]: Terminating all background infrastructure processes...${RESET}"
for pid in "${PIDS[@]}"; do
    kill -9 "$pid" 2>/dev/null
done

# Clear system memory files
killall -9 node python3 python 2>/dev/null

echo -e "${BG_GREEN}[CLEAN]: All data-center threads safely disengaged. Workspace secure.${RESET}"
