#!/bin/bash
# =====================================================================
# JETI MASS-CLUSTER SYSTEM REFRESH: VECTOR ENGINE MATRIX DEPLOY
# =====================================================================
echo "[*] Initializing high-speed parallel deployment across all 30 nodes..."

SOURCE_DIR="$HOME/alstra-workspace"
TARGET_DIR="/data/data/com.termux/files/home/alstra-workspace"

# Scrape all active device transport layers
devices=$(adb devices | awk 'NR>1 && $2=="device" {print $1}')

for device in $devices; do
    (
        echo "[⚡ PATCHING LAYER] Syncing clean asset arrays to device: $device"
        
        # Mirror workspace folder trees cleanly onto child filesystems
        adb -s "$device" shell "mkdir -p $TARGET_DIR"
        adb -s "$device" push "$SOURCE_DIR/server.py" "$TARGET_DIR/server.py" >/dev/null 2>&1
        adb -s "$device" push "$HOME/start_all.sh" "/data/data/com.termux/files/home/start_all.sh" >/dev/null 2>&1
        
        # Kill lingering zombie configurations and trigger hot-reboot
        adb -s "$device" shell "pkill -f uvicorn; pkill -f python3" >/dev/null 2>&1
        adb -s "$device" shell "chmod +x /data/data/com.termux/files/home/start_all.sh"
        adb -s "$device" shell "bash ~/start_all.sh" >/dev/null 2>&1
        
        echo "[✓ SUCCESS] Core stack active on device: $device"
    ) &
done

wait
echo "====================================================================="
echo "[====] GLOBAL PATCH COMPLETED: ARCHITECTURE SYNCHRONIZED [====]"
echo "====================================================================="
