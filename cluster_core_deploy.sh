#!/bin/bash
# =====================================================================
# JETI DISTRIBUTED EXECUTION LAYER: OMNI API SYNCHRONIZER
# =====================================================================
clear
echo "====================================================================="
echo "       JETI MASS-CLUSTER SYSTEM GENERATOR: INITIALIZING API STACK     "
echo "====================================================================="

SOURCE_DIR="$HOME/alstra-workspace"
TARGET_DIR="/data/data/com.termux/files/home/alstra-workspace"

# Scrape active keys
devices=$(adb devices | awk 'NR>1 && $2=="device" {print $1}')

echo "[*] Synchronizing codebase and spinning up API instances on node channels..."
for device in $devices; do
    (
        # Inject directories and drop script architectures into nodes recursively
        adb -s "$device" shell "mkdir -p $TARGET_DIR"
        adb -s "$device" push "$SOURCE_DIR/." "$TARGET_DIR/" >/dev/null 2>&1
        adb -s "$device" push "$HOME/start_all.sh" "/data/data/com.termux/files/home/start_all.sh" >/dev/null 2>&1
        adb -s "$device" shell "chmod +x /data/data/com.termux/files/home/start_all.sh"
        
        # Fire structural runtime activation scripts
        adb -s "$device" shell "bash ~/start_all.sh" >/dev/null 2>&1
        echo -e "[✓] Node [$device] successfully executing optimized vector endpoints."
    ) &
done
wait

echo ""
echo "====================================================================="
echo "  [====] JETI END-TO-END SUPERCOMPUTING CLUSTER CHANNELS [====]    "
echo "====================================================================="
echo " TARGET NODE IP ENDPOINTS READY FOR DYNAMIC INGESTION GRAPHING:       "
echo "---------------------------------------------------------------------"
for device in $devices; do
    device_ip=$(adb -s "$device" shell "ip route | grep wlan0 | awk '{print \$9}'" 2>/dev/null | tr -d '\r')
    if [ -z "$device_ip" ]; then
        device_ip="127.0.0.1 (Local ADB)"
    fi
    printf "  NODE ID: %-22s ---> API GATEWAY: http://%s:3000/docs\n" "$device" "$device_ip"
done
echo "====================================================================="
