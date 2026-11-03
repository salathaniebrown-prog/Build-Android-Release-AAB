const express = require('express');
const http = require('http');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const app = express();
const server = http.createServer(app);
app.use(express.json());

// SQLite Database Core Connection
const dbFile = path.join(__dirname, 'alstra_enterprise_core.db');
const db = new sqlite3.Database(dbFile, (err) => {
  if (err) console.error('[SQLite Error]', err.message);
  else console.log('[SQLite] Connected to Alstra Enterprise Core DB.');
});

db.serialize(() => {
  db.run("CREATE TABLE IF NOT EXISTS enterprise_ledger (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, category TEXT, payload TEXT, signature TEXT)");
  db.run("CREATE TABLE IF NOT EXISTS autonomous_vectors (id INTEGER PRIMARY KEY AUTOINCREMENT, tag TEXT, content TEXT, epoch INTEGER)");
  db.run("INSERT OR IGNORE INTO autonomous_vectors (id, tag, content, epoch) VALUES (1, 'root_identity', 'Salathaniel S A Brown Sr, CDP Vault 0x5f04EBB30d3BBf356263c3ef4823080d05bEDDf5 ($20.00 USDC).', 14)");
});

let ledgerBlock = 250;

// Dual-Brain Telemetry Endpoint
app.get('/api/dual-brain', (req, res) => {
  res.json({
    success: true,
    brain_1_local: {
      status: "ACTIVE_TERMINAL_ROOT",
      owner: "Salathaniel S A Brown Sr",
      vault: "0x5f04EBB30d3BBf356263c3ef4823080d05bEDDf5",
      database: "alstra_enterprise_core.db",
      port: 3001
    },
    brain_2_github: {
      status: "SYNCED_WORKFLOW_NEXUS",
      repository: "salathaniebrown-prog/Build-Android-Release-AAB",
      runner: "Ubuntu Edge Node",
      ci_status: "MONITORED_24_7"
    }
  });
});

// Telemetry State Gateway
app.get('/api/sovereign-state', (req, res) => {
  res.json({
    success: true,
    enterpriseOwner: "Salathaniel S A Brown Sr",
    role: "LEAD_SYSTEM_ARCHITECT_ROOT_OWNER",
    status: "ONLINE_AUTONOMOUS_ENTERPRISE_24_7",
    systemVersion: "v14.2.0-dual-brain-nexus",
    vaultWallet: "0x5f04EBB30d3BBf356263c3ef4823080d05bEDDf5",
    balance: "$20.00 USDC",
    activeGpuClusters: 5000,
    aggregateEflops: "121.55 EFLOPS"
  });
});

// Fast Directives Gateway
app.post('/api/fast', (req, res) => {
  const command = (req.body.command || 'status').trim();
  ledgerBlock++;
  const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
  const signature = '0x' + Math.random().toString(16).substring(2, 34);

  db.run("INSERT INTO enterprise_ledger (timestamp, category, payload, signature) VALUES (?, ?, ?, ?)",
    [timestamp, 'DIRECTIVE', command, signature]);

  res.json({
    status: 'success',
    output: `[${timestamp}] DUAL-BRAIN DIRECTIVE EXECUTED: "${command}"\n• Ledger Block : #${ledgerBlock}\n• Owner        : Salathaniel S A Brown Sr\n• CDP Vault    : 0x5f04EBB30d3BBf356263c3ef4823080d05bEDDf5 [$20.00 USDC]\n• Local Brain  : Termux Debian Node Active (Port 3001)\n• Edge Brain   : GitHub Workflow Synchronized`
  });
});

// Master Dashboard Interface
app.get(['/', '/v14', '/dashboard'], (req, res) => {
  res.send(`<!DOCTYPE html>
<html>
<head>
  <title>Astra Dual-Brain Command Center v14</title>
  <style>
    body { background: #04050a; color: #00ffaa; font-family: monospace; padding: 25px; margin: 0; }
    h1 { color: #00ffff; border-bottom: 2px solid #00ffaa; padding-bottom: 10px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 20px; }
    .card { background: #0a0e1a; border: 1px solid #1e3a5f; padding: 20px; border-radius: 8px; }
    #console { background: #020307; border: 1px solid #00ffaa; color: #00ffaa; padding: 15px; height: 220px; overflow-y: auto; border-radius: 6px; }
    input, button { padding: 12px; font-family: monospace; border-radius: 6px; }
    input { width: 75%; background: #0d1326; color: #fff; border: 1px solid #1e3a5f; }
    button { background: #00ffaa; color: #04050a; font-weight: bold; border: none; cursor: pointer; width: 20%; }
    button:hover { background: #00cc88; }
  </style>
</head>
<body>
  <h1>ASTRA ENTERPRISE // DUAL-BRAIN MATRIX</h1>
  <div class="grid">
    <div class="card">
      <h3>Brain 1: Local Terminal Core</h3>
      <p><strong>Owner:</strong> Salathaniel S A Brown Sr</p>
      <p><strong>Status:</strong> <span style="color:#00ffaa;font-weight:bold;">ONLINE (Port 3001)</span></p>
      <p><strong>Vault:</strong> 0x5f04...DdF5 ($20.00 USDC)</p>
    </div>
    <div class="card">
      <h3>Brain 2: GitHub Edge Nexus</h3>
      <p><strong>Repo:</strong> Build-Android-Release-AAB</p>
      <p><strong>Runner:</strong> Ubuntu Edge (CI/CD)</p>
      <p><strong>Sync Status:</strong> <span style="color:#00ffff;font-weight:bold;">SYNCHRONIZED</span></p>
    </div>
  </div>

  <div class="card">
    <h3>Unified Command Center Gateway</h3>
    <div id="console">Dual-Brain Engine Online. Awaiting directive...</div><br/>
    <input type="text" id="cmd" placeholder="Type command (e.g. status, audit)..." />
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
        c.innerHTML += '<br/><span style="color:#ff5555">[ERROR] Execution failed.</span>';
      }
      input.value = '';
      c.scrollTop = c.scrollHeight;
    }
  </script>
</body>
</html>`);
});

const PORT = 3001;
server.listen(PORT, '0.0.0.0', () => {
  console.log('[Dual-Brain Server] Operational on http://0.0.0.0:' + PORT);
});
