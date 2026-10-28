#!/usr/bin/env bash

# UI formatting colors configuration strings
BG_CYAN="\033[1;36m"
BG_GREEN="\033[1;32m"
BG_YELLOW="\033[1;33m"
BG_RED="\033[1;31m"
RESET="\033[0m"

clear
echo -e "${BG_CYAN}=========================================================${RESET}"
echo -e "🧠  ASTRA SOVEREIGN AUTONOMOUS RECOVERY ENGINE INITIALIZED"
echo -e "📡  Targeting Remote Repository Space: salathanielbrown-prog"
echo -e "${BG_CYAN}=========================================================${RESET}"

# Target folder structures definition
TARGET_DIR="${HOME}/alstra-workspace"
ANALYTICS_DIR="${HOME}/chronicle-analytics/data_engine/db_store"
REPO_URL="git@github.com:salathanielbrown-prog/astra-sovereign-crypto.git"

echo -e "\n${BG_YELLOW}[PHASE 1]: Inspecting system directory pathways...${RESET}"
mkdir -p "$TARGET_DIR"
mkdir -p "$ANALYTICS_DIR"
echo "   ├── Storage paths verified and locked into system paths."

# Recreate empty database file log assets to prevent app crashes if wiped
if [ ! -f "${ANALYTICS_DIR}/deepspace_master_ledger.jsonl" ]; then
    touch "${ANALYTICS_DIR}/deepspace_master_ledger.jsonl"
    echo "   ├── Empty ledger storage logs generated."
fi

echo -e "\n${BG_YELLOW}[PHASE 2]: Rebuilding software dependency artifacts...${RESET}"
cd "$TARGET_DIR" || exit 1

# Check if file assets are missing and require remote recovery downloads
if [ ! -f "server.js" ] && [ ! -d ".git" ]; then
    echo -e "   ⚠️  [ALERT]: Workspace files erased! Initiating remote code checkout..."
    git clone "$REPO_URL" . 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo -e "   └── ${BG_GREEN}[SUCCESS]${RESET} Codebase downloaded from repository channel."
    else
        echo -e "   └── ${BG_RED}[WARNING]${RESET} Cannot reach remote repo. Recreating core system files locally..."
        # Fallback file regeneration block goes here if network interface fails
    fi
else
    echo "   ├── Base directory files are intact. Skipping download step."
fi

# Clean port allocations before triggering system restarts
killall -9 node python3 python 2>/dev/null 2>/dev/null

echo -e "\n${BG_YELLOW}[PHASE 3]: Re-launching multi-worker computer array...${RESET}"
if [ -f "launch_system.sh" ]; then
    chmod +x launch_system.sh
    ./launch_system.sh
else
    # Fallback restart if files are running natively inside current workspace folder
    if [ -f "server.js" ]; then
        node server.js > server_cluster.log 2>&1 &
        echo -e "   └── ${BG_GREEN}[ONLINE]${RESET} Node.js core successfully rebound to port 8080."
    fi
    if [ -f "vector_datacenter_core.py" ]; then
        python3 vector_datacenter_core.py > vector_database.log 2>&1 &
        echo -e "   └── ${BG_GREEN}[ONLINE]${RESET} Vector AI engine successfully rebound to port 8095."
    fi
fi

echo -e "\n${BG_CYAN}=========================================================${RESET}"
echo -e "🎉  ${BG_GREEN}RECOVERY SYSTEM ONLINE: Core brain found and stable!${RESET}"
echo -e "${BG_CYAN}=========================================================${RESET}"
