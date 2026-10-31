#!/usr/bin/env python3
import asyncio
import json
import sqlite3
import os
import websockets
from datetime import datetime

WORKSPACE_DIR = os.path.expanduser("~/alstra-workspace")
DB_PATH = os.path.join(WORKSPACE_DIR, "deepspace_ledgers.db")

async def telemetry_broadcast(websocket, path):
    print(f"[+] Client connected from {websocket.remote_address}")
    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT id, event_type, payload, vector_fidelity, timestamp FROM master_events ORDER BY id DESC LIMIT 1;")
            row = c.fetchone()
            conn.close()
            payload = {
                "system": "BUDA_ALPHA_DUO",
                "status": "MAX_LEVEL_PERFORMANCE",
                "latest_event": dict(row) if row else None,
                "broadcast_timestamp": timestamp
            }
            await websocket.send(json.dumps(payload))
            await asyncio.sleep(1.0)
    except websockets.exceptions.ConnectionClosed:
        print("[-] Client disconnected.")

async def main():
    print("[*] Launching WebSocket Telemetry Bridge on port 8081...")
    async with websockets.serve(telemetry_broadcast, "0.0.0.0", 8081):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
