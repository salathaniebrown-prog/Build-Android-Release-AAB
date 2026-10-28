import sqlite3

conn = sqlite3.connect('/root/datacenter_ledger.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS satellite_telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        node_id TEXT,
        architecture TEXT,
        adb_status TEXT,
        uvicorn_core TEXT,
        vnc_runtime TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()
print("SQLite Database Table 'satellite_telemetry' Ready.")
