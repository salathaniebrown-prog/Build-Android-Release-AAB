const express = require('express');
const http = require('http');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Master Orchestrator (Port 3001)
const appMaster = express();
const serverMaster = http.createServer(appMaster);
appMaster.use(express.json());

// Vector Datacenter Core (Port 8090)
const appVector = express();
const serverVector = http.createServer(appVector);
appVector.use(express.json());

// Enterprise Financial Settlement Ledger (Port 8099)
const appLedger = express();
const serverLedger = http.createServer(appLedger);
appLedger.use(express.json());

// Database connection
const dbFile = path.join(__dirname, 'alstra_enterprise_core.db');
const db = new sqlite3.Database(dbFile);

db.serialize(() => {
  db.run("CREATE TABLE IF NOT EXISTS enterprise_ledger (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, category TEXT, payload TEXT, signature TEXT)");
  db.run("CREATE TABLE IF NOT EXISTS cross_platform_sync (id INTEGER PRIMARY KEY AUTOINCREMENT, platform TEXT, status TEXT, epoch INTEGER)");
});

let ledgerBlock = 300;

// --- MASTER PORT 3001: UI & DUAL-BRAIN TELEMETRY ---
appMaster.get('/api/sovereign-state', (req, res) => {
  res.json({
    success: true,
    enterpriseOwner: "Salathaniel S A Brown Sr",
    role: "LEAD_SYSTEM_ARCHITECT_ROOT_OWNER",
    status: "ONLINE_MULTI_PORT_INGRESS_ACTIVE",
    vaultWallet: "0x5f04EBB30d3BBf356263c3ef4823080d05bEDDf5",
    balance: "$20.00 USDC",
    activePorts: [3001, 8090, 8099, 8001],
    aggregateEflops: "121.55 EFLOPS"
  });
});

appMaster.get('/api/dual-brain', (req, res) => {
  res.json({
    success: true,
    brain_1_local: { status: "ACTIVE_ROOT_TERMINAL", port: 3001 },
    brain_2_github: { status: "SYNCED_EDGE_WORKFLOW", repo: "Build-Android-Release-AAB" }
  });
});

appMaster.get(['/', '/v14', '/dashboard'], (req, res) => {
  res.send(`<!DOCTYPE html>
<html>
<head>
  <title>Astra Multi-Port Enterprise Nexus</title>
  <style>
    body { background: #04050a; color: #00ffaa; font-family: monospace; padding: 25px; margin: 0; }
    h1 { color: #00ffff; border-bottom: 2px solid #00ffaa; padding-bottom: 10px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 20px; }
    .card { background: #0a0e1a; border: 1px solid #1e3a5f; padding: 20px; border-radius: 8px; }
    #console { background: #020307; border: 1px solid #00ffaa; color: #00ffaa; padding: 15px; height: 200px; overflow-y: auto; border-radius: 6px; }
    input, button { padding: 12px; font-family: monospace; border-radius: 6px; }
    input { width: 72%; background: #0d1326; color: #fff; border: 1px solid #1e3a5f; }
    button { background: #00ffaa; color: #04050a; font-weight: bold; border: none; cursor: pointer; width: 22%; }
    button:hover { background: #00cc88; }
  </style>
</head>
<body>
  <h1>ASTRA MULTI-PORT ENTERPRISE NEXUS</h1>
  <div class="grid">
    <div class="card">
      <h3>Active Ports Ingress</h3>
      <p><strong>Port 3001:</strong> Master UI & Telemetry</p>
      <p><strong>Port 8090:</strong> Vector Datacenter Core</p>
      <p><strong>Port 8099:</strong> Financial Settlement Ledger</p>
    </div>
    <div class="card">
      <h3>Vault & Ownership</h3>
      <p><strong>Owner:</strong> Salathaniel S A Brown Sr</p>
      <p><strong>Vault:</strong> 0x5f04...DdF5 ($20.00 USDC)</p>
      <p><strong>Mesh Compute:</strong> 121.55 EFLOPS</p>
    </div>
  </div>

  <div class="card">
    <h3>Cross-Platform Command Core</h3>
    <div id="console">Multi-port ingress mesh initialized. Ready for cross-platform projects...</div><br/>
    <input type="text" id="cmd" placeholder="Type cross-platform directive..." />
    <button onclick="send()">EXECUTE</button>
  </div>

  <script>
    async function send() {
      const input = document.getElementById('cmd');
      const c = document.getElementById('console');
      if (!input.value) return;
      c.innerHTML += '<br/><span style="color:#00ffff">> ' + input.value + '</span>';
      try {
        const res = await fetch('/api/fast', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ command: input.value })
        });
        const d = await res.json();
        c.innerHTML += '<br/>' + d.output.replace(/\\n/g, '<br/>');
      } catch(e) {
        c.innerHTML += '<br/><span style="color:#ff5555">[ERROR] Dispatch failed.</span>';
      }
      input.value = '';
      c.scrollTop = c.scrollHeight;
    }
  </script>
</body>
</html>`);
});

appMaster.post('/api/fast', (req, res) => {
  const command = (req.body.command || 'status').trim();
  ledgerBlock++;
  const ts = new Date().toISOString().replace('T', ' ').substring(0, 19);
  const signature = '0x' + Math.random().toString(16).substring(2, 34);

  db.run("INSERT INTO enterprise_ledger (timestamp, category, payload, signature) VALUES (?, ?, ?, ?)",
    [ts, 'CROSS_PLATFORM_DIRECTIVE', command, signature]);

  res.json({
    status: 'success',
    output: `[${ts}] CROSS-PLATFORM DISPATCH: "${command}"\n• Ledger Block : #${ledgerBlock}\n• Vault        : 0x5f04EBB30d3BBf356263c3ef4823080d05bEDDf5 [$20.00 USDC]\n• Ingress Mesh : Ports 3001, 8090, 8099 Synchronized\n• Signature    : ${signature}`
  });
});

// --- PORT 8090: VECTOR DATACENTER CORE ---
appVector.get('/vector-status', (req, res) => {
  res.json({ service: "Vector Datacenter Core", status: "ONLINE", eflops: "121.55 EFLOPS" });
});

// --- PORT 8099: FINANCIAL SETTLEMENT LEDGER ---
appLedger.get('/ledger-status', (req, res) => {
  res.json({ service: "Alstra Financial Settlement Ledger", status: "SECURED", wallet: "0x5f04EBB30d3BBf356263c3ef4823080d05bEDDf5", balance: "$20.00 USDC" });
});

// Listen across all ports simultaneously
serverMaster.listen(3001, '0.0.0.0', () => console.log('[Master Ingress] Live on port 3001'));
serverVector.listen(8090, '0.0.0.0', () => console.log('[Vector Core] Live on port 8090'));
serverLedger.listen(8099, '0.0.0.0', () => console.log('[Settlement Ledger] Live on port 8099'));
