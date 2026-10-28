import datetime
from datetime import timezone
import time
import threading
import random
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

EAGLE_EYES_STATE = {
    "system": {
        "node_id": "EAGLE-EYES-ASTRA-CORE",
        "status": "HEALTHY",
        "iteration": 131,
        "cpu_usage": "21%",
        "ram_usage": "31%",
        "net_speed": "1.2 Gbps",
        "containers": "36 / 36 Online"
    },
    "astra_db": {
        "sdk_status": "READY (astrapy-v1.5)",
        "database_id": "DATABASE_ID_RESUMED",
        "keyspace": "KEYSPACE_NAME",
        "collection": "COLLECTION_NAME",
        "last_insert_id": "3f557bef-fd53-47ea-957b-effd53c7eaec"
    },
    "kafka_protocol": {
        "messaging_protocols": "kafka",
        "protocol_handler_dir": "./protocols",
        "auto_topic_creation": "partitioned",
        "listeners": "PLAINTEXT://127.0.0.1:9092"
    },
    "crypto_stream": {
        "btc_price": 82794.38,
        "sol_price": 107.33,
        "btc_change": "+1.16%",
        "sol_change": "+3.20%"
    },
    "satellites": {
        "active_count": 4892,
        "uptime": "99.7%",
        "iss_lat": -12.4,
        "iss_lon": 132.8
    }
}

LOG_STREAM = [
    "[BOOT] Tactical Graphics Pipeline Initialized.",
    "[CRYPTO] Real-time asset synchronization pipeline established."
]

def add_log(tag, msg):
    ts = datetime.datetime.now(timezone.utc).strftime('%H:%M:%S')
    LOG_STREAM.append(f"[{ts}] [{tag}] {msg}")
    if len(LOG_STREAM) > 8: LOG_STREAM.pop(0)

def pipeline_simulation_loop():
    while True:
        EAGLE_EYES_STATE["system"]["iteration"] += 1
        btc = EAGLE_EYES_STATE["crypto_stream"]["btc_price"]
        sol = EAGLE_EYES_STATE["crypto_stream"]["sol_price"]
        EAGLE_EYES_STATE["crypto_stream"]["btc_price"] = round(btc + random.uniform(-4.5, 6.2), 2)
        EAGLE_EYES_STATE["crypto_stream"]["sol_price"] = round(sol + random.uniform(-0.1, 0.2), 2)
        time.sleep(2)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>EAGLE EYES CONSOLE</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: monospace; background: #03050a; color: #00f3ff; margin: 0; padding: 15px; }
        .grid { display: flex; flex-direction: column; gap: 15px; max-width: 700px; margin: 0 auto; }
        .panel { background: rgba(10, 15, 30, 0.9); border: 1px solid #00f3ff; border-radius: 4px; padding: 15px; }
        h1 { margin: 0; font-size: 1.2rem; text-align: center; color: #fff; border-bottom: 2px solid #00f3ff; padding-bottom: 8px; text-transform: uppercase; }
        h2 { font-size: 1rem; color: #ffaa00; text-transform: uppercase; margin-top: 0; border-bottom: 1px solid #1a2636; padding-bottom: 4px; }
        .metric { display: flex; justify-content: space-between; padding: 6px 0; font-size: 0.9rem; border-bottom: 1px solid #0c1524; }
        .label { color: #8fa0b5; }
        .val { font-weight: bold; color: #fff; }
        canvas { width: 100%; height: 140px; background: #050811; border: 1px solid #122236; border-radius: 4px; display: block; margin-top: 10px; }
        .control-group { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 12px; }
        .btn { padding: 12px; background: #00f3ff; color: #03050a; border: none; font-family: monospace; font-weight: bold; cursor: pointer; border-radius: 3px; text-transform: uppercase; }
        .console { background: #020408; border: 1px solid #122236; height: 100px; overflow-y: auto; padding: 8px; color: #a0aec0; }
    </style>
    <script>
        function sendCommand(action) {
            fetch('/admin/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: action })
            }).then(() => window.location.reload());
        }
    </script>
</head>
<body>
    <div class="grid">
        <div class="panel">
            <h1>🦅 EAGLE EYES // ACTIVE OPERATIONS HUB</h1>
        </div>

        <div class="panel">
            <h2>Real-Time Crypto Feed</h2>
            <div class="metric"><span class="label">BTC - Bitcoin:</span><span class="val" id="btc_ticker" style="color: #ffffff;">\$ --</span></div>
            <div class="metric"><span class="label">SOL - Solana Core:</span><span class="val" id="sol_ticker" style="color: #ffaa00;">\$ --</span></div>
        </div>

        <div class="panel">
            <h2>DataStax Astra DB Document Reference</h2>
            <div class="metric"><span class="label">API Status:</span><span class="val" style="color: #00ffaa;">{{ metrics.astra_db.sdk_status }}</span></div>
            <div class="metric"><span class="label">Database:</span><span class="val" style="color: #ffaa00;">{{ metrics.astra_db.database_id }}</span></div>
        </div>

        <div class="panel">
            <h2>Orbital Satellite Vectors</h2>
            <div class="metric"><span class="label">Uptime Baseline:</span><span class="val" style="color: #00ffaa;">99.7%</span></div>
            <canvas id="globeCanvas"></canvas>
        </div>

        <div class="panel">
            <h2>Live Subnet Radar Sweep</h2>
            <div class="metric"><span class="label">Matrix:</span><span class="val" style="color: #00ffaa;">{{ metrics.system.status }}</span></div>
            <div class="metric"><span class="label">Cycle:</span><span class="val" id="iter_counter">#{{ metrics.system.iteration }}</span></div>
            <canvas id="radarCanvas"></canvas>
        </div>

        <div class="panel">
            <h2>System Controls & Commands</h2>
            <div class="control-group">
                <button class="btn" onclick="sendCommand('FORCE_INSERT')">Execute insertMany</button>
                <button class="btn" onclick="sendCommand('CLEAR_LOGS')">Flush Logs</button>
            </div>
        </div>

        <div class="panel">
            <h2>Unified Ingestion Stream Intercept Logs</h2>
            <div class="console" id="term">
                {% for log in logs %}<div>{{ log }}</div>{% endfor %}
            </div>
        </div>
    </div>

    <script>
        const gCanvas = document.getElementById('globeCanvas');
        const gCtx = gCanvas.getContext('2d');
        let angle = 0;
        function drawGlobe() {
            gCanvas.width = gCanvas.offsetWidth; gCanvas.height = gCanvas.offsetHeight;
            const cx = gCanvas.width / 2; const cy = gCanvas.height / 2;
            gCtx.strokeStyle = 'rgba(0, 243, 255, 0.4)';
            for (let i = 0; i < 4; i++) {
                gCtx.beginPath(); gCtx.ellipse(cx, cy, 45, Math.abs(45 * Math.sin(angle + (i * Math.PI / 4))), 0, 0, 2 * Math.PI); gCtx.stroke();
            }
            angle += 0.015; requestAnimationFrame(drawGlobe);
        }

        const rCanvas = document.getElementById('radarCanvas');
        const rCtx = rCanvas.getContext('2d');
        let sweepAngle = 0;
        function drawRadar() {
            rCanvas.width = rCanvas.offsetWidth; rCanvas.height = rCanvas.offsetHeight;
            const cx = rCanvas.width / 2; const cy = rCanvas.height / 2;
            rCtx.strokeStyle = 'rgba(0, 255, 170, 0.2)';
            rCtx.beginPath(); rCtx.arc(cx, cy, 50, 0, 2 * Math.PI); rCtx.stroke();
            rCtx.strokeStyle = 'rgba(0, 255, 170, 0.8)'; rCtx.lineWidth = 2;
            rCtx.beginPath(); rCtx.moveTo(cx, cy); rCtx.lineTo(cx + 50 * Math.cos(sweepAngle), cy + 50 * Math.sin(sweepAngle)); rCtx.stroke();
            sweepAngle += 0.02; requestAnimationFrame(drawRadar);
        }
        drawGlobe(); drawRadar();

        setInterval(() => {
            fetch('/status').then(res => res.json()).then(data => {
                let btcVal = data.crypto_stream.btc_price.toFixed(2);
                let solVal = data.crypto_stream.sol_price.toFixed(2);
                document.getElementById("btc_ticker").innerText = "\$ " + btcVal + " USD";
                document.getElementById("sol_ticker").innerText = "\$ " + solVal + " USD";
                document.getElementById("iter_counter").innerText = "#" + data.system.iteration;
                document.getElementById("term").innerHTML = data.logs.map(l => `<div>${l}</div>`).join('');
            });
        }, 1500);
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index(): return render_template_string(HTML_TEMPLATE, metrics=EAGLE_EYES_STATE, logs=LOG_STREAM)

@app.route('/status', methods=['GET'])
def status(): return jsonify({**EAGLE_EYES_STATE, "logs": LOG_STREAM})

@app.route('/admin/command', methods=['POST'])
def admin_command():
    data = request.get_json() or {}
    action = data.get("action")
    if action == "FORCE_INSERT":
        add_log("KAFKA_BROKER", "Dispatched packet buffer stream events to local endpoints.")
    elif action == "CLEAR_LOGS":
        global LOG_STREAM
        LOG_STREAM = ["[SYSTEM] Operations log dashboard traces flushed by admin."]
    return jsonify({"status": "PROCESSED"})

if __name__ == "__main__":
    threading.Thread(target=pipeline_simulation_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
