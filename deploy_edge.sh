#!/data/data/com.termux/files/usr/bin/bash

cd "$(dirname "$0")"

# Grab the most recent tarball snapshot
LATEST_BACKUP=$(ls -t ./backups/consensus_core_*.tar.gz 2>/dev/null | head -n 1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "[ERROR] No backup archive found in ./backups/. Run ./commit_and_push.sh first."
    exit 1
fi

echo "[EDGE DEPLOY] Found bundle: $LATEST_BACKUP"

# Display options to push to Edge Target
echo "--------------------------------------------------"
echo "To transfer this package to your Edge device via SSH/SCP:"
echo "  scp $LATEST_BACKUP user@edge-ip:/path/to/target/"
echo ""
echo "To extract directly on target device:"
echo "  tar -xzf $(basename $LATEST_BACKUP)"
echo "--------------------------------------------------"
