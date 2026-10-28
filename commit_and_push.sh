#!/data/data/com.termux/files/usr/bin/bash

cd "$(dirname "$0")"

echo "[SYSTEM] Pre-checking Termux environment..."

mkdir -p ./backups

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="./backups/consensus_core_${TIMESTAMP}.tar.gz"

echo "[SYSTEM] Creating full local snapshot archive: ${BACKUP_FILE}..."
tar -czf "$BACKUP_FILE" models.py main.py run_test.py pkg_queue_runner.py deploy_edge.sh README.md 2>/dev/null

echo "[SYSTEM] Verification suite run..."
python3 run_test.py

echo "[SYSTEM] Full workspace snapshot sync complete."
