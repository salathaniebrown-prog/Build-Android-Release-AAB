import json
import csv
import os
from collections import defaultdict

LEDGER_FILE = "telemetry_ledger.jsonl"
CSV_FILE = "telemetry_report.csv"

if not os.path.exists(LEDGER_FILE):
    print(f"[ERROR]: Ledger file '{LEDGER_FILE}' not found.")
    exit(1)

records = []
fleet_stats = defaultdict(lambda: {"total": 0, "anomalies": 0, "similarities": []})

with open(LEDGER_FILE, "r") as f:
    for line in f:
        if line.strip():
            data = json.loads(line)
            records.append(data)
            sat_id = data.get("satellite_id", "UNKNOWN")
            status = data.get("status", "UNKNOWN")
            sim = data.get("cosine_similarity", 0.0)
            
            fleet_stats[sat_id]["total"] += 1
            if status == "ISOLATED_ANOMALY":
                fleet_stats[sat_id]["anomalies"] += 1
            fleet_stats[sat_id]["similarities"].append(sim)

# Print Summary Report
print("=" * 65)
print("           ALSTRA TELEMETRY FLEET ANALYTICS REPORT           ")
print("=" * 65)
print(f"{'SATELLITE ID':<20} | {'TOTAL':<8} | {'ANOMALIES':<10} | {'AVG SIMILARITY'}")
print("-" * 65)

for sat_id, stats in sorted(fleet_stats.items()):
    avg_sim = sum(stats["similarities"]) / len(stats["similarities"]) if stats["similarities"] else 0.0
    print(f"{sat_id:<20} | {stats['total']:<8} | {stats['anomalies']:<10} | {avg_sim:.4f}")

print("=" * 65)

# Export to CSV
with open(CSV_FILE, "w", newline="") as csvfile:
    fieldnames = ["id", "satellite_id", "status", "cosine_similarity", "processed_at"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in records:
        writer.writerow(row)

print(f"[EXPORTER SUCCESS]: Exported {len(records)} records to '{CSV_FILE}'.\n")

