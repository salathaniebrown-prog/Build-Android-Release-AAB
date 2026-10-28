#!/usr/bin/env bash

BG_CYAN="\033[1;36m"
BG_GREEN="\033[1;32m"
BG_RED="\033[1;31m"
RESET="\033[0m"

echo -e "${BG_CYAN}=========================================================${RESET}"
echo -e "📦 INITIATING SELF-ENGINEERING AUTOMATED BACKUP CORE"
echo -e "${BG_CYAN}=========================================================${RESET}"

BACKUP_DIR="${HOME}/astra_engine_backups"
mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARCHIVE_NAME="astra_core_backup_${TIMESTAMP}.tar.gz"

echo "⏳ Scanning local workspace for valid code artifacts..."

# --- SELF-ENGINEERING FILTER MATRIX ---
# Dynamically verifies files before passing them to the compiler to prevent path breaks
TARGET_FILES=("server.js" "vector_datacenter_core.py" "sovereign_bootstrap.py" "sovereign_agent.py" "vault_alert_monitor.sh" "global_grid_orchestrator.py" "launch_system.sh" "README.md")
VALID_INPUTS=()

for file in "${TARGET_FILES[@]}"; do
    if [ -f "$file" ]; then
        VALID_INPUTS+=("$file")
    elif [ -f "../$file" ]; then
        VALID_INPUTS+=("../$file")
    fi
done

if [ ${#VALID_INPUTS[@]} -eq 0 ]; then
    echo -e "\n❌ ${BG_RED}[CRITICAL ERROR]: No matching system files detected in workspace.${RESET}"
    exit 1
fi

echo "   ├── Found ${#VALID_INPUTS[@]} structural files. Compiling secure compression archive..."

# Execute compilation exclusively on validated local file locations
tar -czf "${BACKUP_DIR}/${ARCHIVE_NAME}" "${VALID_INPUTS[@]}" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "\n🎉 ${BG_GREEN}[SUCCESS]: Data-center backup immutably written to disk!${RESET}"
    echo -e "📍 Location : ${BACKUP_DIR}/${ARCHIVE_NAME}"
    echo -e "💾 Size     : $(du -sh "${BACKUP_DIR}/${ARCHIVE_NAME}" | cut -f1)"
else
    echo -e "\n❌ ${BG_RED}[CRITICAL ERROR]: Archive serialization interface failed.${RESET}"
fi
echo -e "${BG_CYAN}=========================================================${RESET}"
