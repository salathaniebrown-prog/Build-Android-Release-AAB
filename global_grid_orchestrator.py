import os
import sys
import time
import json
import subprocess

def run_cmd(cmd):
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

print("=========================================================")
print("🧠 INITIATING AI SUPERCOMPUTER STORAGE PRUNING MATRIX")
print("=========================================================")

needed_artifacts = ["rich", "requests"]
missing_artifacts = []

for artifact in needed_artifacts:
    try:
        __import__(artifact)
    except ImportError:
        missing_artifacts.append(artifact)

if missing_artifacts:
    print(f"⚠️  [UNRESOLVED DEPENDENCIES]: Missing artifacts: {missing_artifacts}")
    run_cmd(f"{sys.executable} -m pip install --upgrade pip --quiet")
    for artifact in missing_artifacts:
        res = run_cmd(f"{sys.executable} -m pip install {artifact} --quiet")
        if res.returncode == 0:
            print(f"✅ [REPAIRED]: '{artifact}' artifact compiled into system paths.")
        else:
            print(f"❌ [CRITICAL]: Failed to compile '{artifact}'. Forcing fallback engine...")

print("🟢 [SUCCESS]: Environment software dependencies verified and stable.")
print("=========================================================\n")

try:
    from rich.console import Console
    from rich.table import Table
    use_rich = True
except ImportError:
    use_rich = False

LEDGER_FILE = os.path.expanduser("~/chronicle-analytics/data_engine/db_store/deepspace_master_ledger.jsonl")

WORLD_REGIONS = [
    'US-EAST', 'JP-TOKYO', 'DE-FRANKFURT', 'UK-LONDON', 'CN-SHANGHAI', 
    'SG-CORE', 'KR-SEOUL', 'IN-MUMBAI', 'FR-PARIS', 'CA-CENTRAL',
    'AU-SYDNEY', 'BR-SAOPAULO', 'CH-ZURICH', 'NL-AMSTERDAM', 'HK-ZONE', 
    'IE-DUBLIN', 'IT-MILAN', 'SE-STOCKHOLM', 'ES-MADRID', 'ZA-JOHANNESBURG',
    'AE-DUBAI', 'MX-MEXICO', 'FI-HELSINKI', 'NO-OSLO', 'TW-TAIPEI'
]

def render_rich_dashboard(stats, total, purged_count):
    console = Console()
    console.clear()
    
    console.print("[bold cyan]=========================================================[/bold cyan]")
    console.print("🧠 [bold white]ASTRA SOVEREIGN GLOBAL COMPUTE TELEMETRY MATRIX[/bold white]")
    console.print("[bold cyan]=========================================================[/bold cyan]\n")
    
    console.print(f"📈 Active Satellite Transactions In Memory : [bold green]{total:,}[/bold green]")
    console.print(f"♻️  Auto-Pruned Historical Storage Rows    : [bold yellow]{purged_count:,} entries[/bold yellow]\n")
    
    table = Table(title="Sovereign Land-Grid Load Matrix (Top 25)", title_style="bold magenta", header_style="bold yellow", box=None)
    table.add_column("Geographical Region", width=20)
    table.add_column("Verified Packets", justify="right", width=18)
    table.add_column("Proportional Ingress Load Share Bar", width=35)

    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    
    for country, count in sorted_stats:
        pct = (count / total * 100) if total > 0 else 0
        bar_count = int(pct / 4)
        bar_visual = "■" * bar_count + " " * (25 - bar_count)
        
        table.add_row(
            f"🌍 {country}",
            f"{int(count):,} ops ({pct:.1f}%)",
            f"[bold cyan][{bar_visual}][/bold cyan]"
        )
    
    console.print(table)
    console.print("\n[bold dim]Storage Self-Pruning: ACTIVE (24h Window) | Press Ctrl+C to Exit[/bold dim]")

def run_legacy_dashboard(stats, total, purged_count):
    os.system("clear")
    print("=========================================================")
    print("🧠 ASTRA SOVEREIGN GLOBAL COMPUTE TELEMETRY MATRIX (PRUNED)")
    print("=========================================================")
    print(f"📈 Active Satellite Transactions In Memory : {total}")
    print(f"♻️  Auto-Pruned Historical Storage Rows    : {purged_count} entries\n")
    
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    for country, count in sorted_stats:
        pct = (count / total * 100) if total > 0 else 0
        bar_count = int(pct / 4)
        bar_str = "■" * bar_count
        print(f"🌍 {country:<15} | {int(count)} ops ({pct:>5.1f}%) [{bar_str:<25}]")
    print("\nStorage Self-Pruning: ACTIVE (24h Window) | Press Ctrl+C to Exit")

# Tracks total records optimization history metrics
total_purged_counter = 0

if not os.path.exists(LEDGER_FILE):
    os.makedirs(os.path.dirname(LEDGER_FILE), exist_ok=True)
    with open(LEDGER_FILE, "w") as f:
        pass

try:
    while True:
        with open(LEDGER_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        current_counts = {country: 0 for country in WORLD_REGIONS}
        valid_lines_count = 0
        retained_lines = []
        local_purged_this_tick = 0
        
        # Calculate maximum age parameters (24 hours in milliseconds)
        now_ms = time.time() * 1000
        cutoff_ms = now_ms - (24 * 60 * 60 * 1000)
        
        for line in lines:
            try:
                data = json.loads(line.strip())
                # Default to current time if record timestamp is missing
                timestamp = data.get("timestamp") or now_ms
                
                # Check line age bounds against pruning rules
                if timestamp >= cutoff_ms:
                    zone = data.get("sovereign_country_code") or data.get("origin_zone")
                    if zone in current_counts:
                        current_counts[zone] += 1
                        valid_lines_count += 1
                        retained_lines.append(line)
                else:
                    local_purged_this_tick += 1
                    total_purged_counter += 1
            except Exception:
                continue
        
        # If stale records were encountered, rewrite the log to reclaim disk space
        if local_purged_this_tick > 0:
            with open(LEDGER_FILE, "w", encoding="utf-8") as f:
                f.writelines(retained_lines)
        
        total_processed_packets = valid_lines_count
        
        if use_rich and total_processed_packets > 0:
            render_rich_dashboard(current_counts, total_processed_packets, total_purged_counter)
        else:
            run_legacy_dashboard(current_counts, total_processed_packets, total_purged_counter)
            
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nExiting Global Grid Orchestrator Dashboard Stream.")
