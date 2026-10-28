#!/bin/bash
# =====================================================================
# JETI SUPERCOMPUTING MATRIX: REAL-TIME DASHBOARD & ENTIRE FOLDER SYNC
# =====================================================================

# Color-coded UI configurations
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Define the source folder containing all scripts, assets, and weights
SOURCE_PAYLOAD_DIR="$HOME/alstra-workspace"
TARGET_TERMUX_DIR="/data/data/com.termux/files/home/alstra-workspace"

echo -e "${CYAN}[*] Initializing High-Velocity Recursive Folder Mirroring Sequence...${NC}"

# Fetch active network/hardware devices
devices=$(adb devices | awk 'NR>1 && $2=="device" {print $1}')

# PHASE 1: MASS FOLDER PAYLOAD DEPLOYMENT LOOP (PARALLELIZED)
for device in $devices; do
    (
        echo -e "[⚡ RECURSIVE SYNC] Syncing workspace bundle directory to: $device"
        
        # Ensure targeted directory trees exist securely on the cluster nodes
        adb -s "$device" shell "mkdir -p $TARGET_TERMUX_DIR"
        
        # Push the full directory contents recursively to node space
        adb -s "$device" push "$SOURCE_PAYLOAD_DIR/." "$TARGET_TERMUX_DIR/" >/dev/null 2>&1
        
        # Auto-trigger local orchestrator boot loader to apply asset changes
        adb -s "$device" shell "bash ~/start_all.sh" >/dev/null 2>&1
    ) &
done
wait
echo -e "${GREEN}[✓] Full workspace directory and assets synchronized over cluster arrays.${NC}"
sleep 1.5

# PHASE 2: PERSISTENT MATRIX DASHBOARD LOOP
while true; do
    clear
    echo -e "${YELLOW}=====================================================================${NC}"
    echo -e "${YELLOW}     JETI OMNI-MONITOR: LIVE 30-NODE CLUSTER RUNTIME CONSOLE          ${NC}"
    echo -e "${YELLOW}=====================================================================${NC}"
    echo -e "CURRENT TIME: $(date '+%Y-%m-%d %H:%M:%S') | ARCHITECTURE: JETI RECURSIVE SUPERCOMPUTE"
    echo "---------------------------------------------------------------------"
    printf "%-25s | %-12s | %-12s | %-10s\n" "NODE IDENTIFIER" "ADB STATUS" "VNC RUNTIME" "UVICORN CORE"
    echo "---------------------------------------------------------------------"

    # Inspect process stacks and system status tables across all keys
    for device in $devices; do
        # Extract operational telemetry flags from device shell tables
        vnc_check=$(adb -s "$device" shell "pgrep -f vncserver" 2>/dev/null | tr -d '\r')
        uvicorn_check=$(adb -s "$device" shell "pgrep -f uvicorn" 2>/dev/null | tr -d '\r')

        # Status text conditioning evaluations
        if [ -n "$vnc_check" ]; then VNC_STATUS="${GREEN}ONLINE${NC}"; else VNC_STATUS="${RED}OFFLINE${NC}"; fi
        if [ -n "$uvicorn_check" ]; then UVICORN_STATUS="${GREEN}RUNNING${NC}"; else UVICORN_STATUS="${RED}CRASHED${NC}"; fi
        
        printf "%-25s | %-12s | %-21s | %-19s\n" "$device" "${GREEN}CONNECTED${NC}" "$VNC_STATUS" "$UVICORN_STATUS"
    done

    echo "---------------------------------------------------------------------"
    echo -e "${CYAN}[Console auto-refresh tracking metrics every 5s. Press Ctrl+C to break]${NC}"
    sleep 5
done
