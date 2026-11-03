const express = require('express');
const http = require('http');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const appMaster = express();
appMaster.use(express.json());

const appVector = express();
appVector.use(express.json());

const appLedger = express();
appLedger.use(express.json());

const dbFile = path.join(__dirname, 'alstra_enterprise_core.db');
const db = new sqlite3.Database(dbFile);

db.serialize(() => {
  db.run("CREATE TABLE IF NOT EXISTS enterprise_ledger (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, category TEXT, payload TEXT, signature TEXT)");
  db.run("CREATE TABLE IF NOT EXISTS exoplanet_colonization (id INTEGER PRIMARY KEY AUTOINCREMENT, target_planet TEXT, terraform_stage TEXT, timestamp TEXT)");
});

let ledgerBlock = 400;

// SOVEREIGN STATE TELEMETRY
appMaster.get('/api/sovereign-state', (req, res) => {
  res.json({
    success: true,
    enterpriseOwner: "Salathaniel S A Brown Sr",
    role: "LEAD_SYSTEM_ARCHITECT_ROOT_OWNER",
    status: "BLUE_FIRE_SUPERCOMPUTER_ONLINE",
    vaultWallet: "0x5f04EBB30d3BBf356263c3ef4823080d05bEDDf5",
    balance: "$20.00 USDC",
    activePorts: [3001, 8090, 8099],
    aggregateEflops: "121.55 EFLOPS",
    activeSatellites: 25,
    worldIngestionRate: "148,290 ticks/sec"
  });
});

appMaster.get('/api/dual-brain', (req, res) => {
  res.json({
    success: true,
    brain_1_local: { status: "ACTIVE_ROOT_TERMINAL", port: 3001, mode: "BLUE_FIRE_AGENT" },
    brain_2_github: { status: "SYNCED_EDGE_WORKFLOW", repo: "Build-Android-Release-AAB" }
  });
});

// MASTER COMMAND CENTER UI (BLUE FIRE CYBERNETIC THEME)
appMaster.get(['/', '/v14', '/dashboard'], (req, res) => {
  res.send(`<!DOCTYPE html>
<html>
<head>
  <title>Astra Blue-Fire Supercomputer Nexus</title>
  <style>
    body { background: #02040a; color: #00d9ff; font-family: monospace; padding: 25px; margin: 0; box-sizing: border-box; }
    h1 { color: #0088ff; border-bottom: 2px solid #00d9ff; padding-bottom: 10px; text-shadow: 0 0 10px rgba(0,217,255,0.5); }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 20px; }
    .card { background: #060a17; border: 1px solid #0055ff; padding: 20px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,136,255,0.15); }
    #console { background: #010206; border: 1px solid #00d9ff; color: #00d9ff; padding: 15px; height: 240px; overflow-y: auto; border-radius: 6px; box-shadow: inset 0 0 15px rgba(0,217,255,0.1); }
    input, button { padding: 12px; font-family: monospace; border-radius: 6px; }
    input { width: 72%; background: #040814; color: #fff; border: 1px solid #0088ff; }
    button { background: linear-gradient(135deg, #0055ff, #00d9ff); color: #02040a; font-weight: bold; border: none; cursor: pointer; width: 22%; text-shadow: 0 0 5px rgba(255,255,255,0.5); }
    button:hover { filter: brightness(1.2); }
    .tag { color: #ff0055; font-weight: bold; }
  </style>
</head>
<body>
  <h1>🔥 ASTRA BLUE-FIRE SUPERCOMPUTER // SOVEREIGN AGENT</h1>
  <div class="grid">
    <div class="card">
      <h3>Root Architect Telemetry</h3>
      <p><strong>Owner:</strong> Salathaniel S A Brown Sr</p>
      <p><strong>Vault:</strong> 0x5f04...DdF5 ($20.00 USDC)</p>
      <p><strong>Status:</strong> <span style="color:#00d9ff;font-weight:bold;">BLUE-FIRE ACTIVE 24/7</span></p>
    </div>
    <div class="card">
      <h3>Planetary & Datacenter Mesh</h3>
      <p><strong>Compute Power:</strong> 121.55 EFLOPS (5,000 Clusters)</p>
      <p><strong>Satellites:</strong> 25 Orbital Nodes</p>
      <p><strong>Ingestion:</strong> 148,290 ticks/sec</p>
    </div>
  </div>

  <div class="card">
    <h3>Autonomous Agent Command Center (/api/fast)</h3>
    <div id="console">Blue-Fire Supercomputer Agent Initialized. Try commands like: 'status', 'planet search', 'clone earth TOI-700d', or 'audit'...</div><br/>
    <input type="text" id="cmd" placeholder="Type directive or terraforming command..." />
    <button onclick="send()">EXECUTE</button>
  </div>

  <script>
    async function send() {
      const input = document.getElementById('cmd');
      const c = document.getElementById('console');
      if (!input.value) return;
      c.innerHTML += '<br/><span style="color:#ffffff">> ' + input.value + '</span>';
      try {
        const res = await fetch('/api/fast', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ command: input.value })
        });
        const d = await res.json();
        c.innerHTML += '<br/>' + d.output.replace(/\\n/g, '<br/>');
      } catch(e) {
        c.innerHTML += '<br/><span style="color:#ff0055">[ERROR] Directive transmission failed.</span>';
      }
      input.value = '';
      c.scrollTop = c.scrollHeight;
    }
  </script>
</body>
</html>`);
});

// DIRECTIVE EXECUTION & EXOPLANET/TERRAFORMING GATEWAY
appMaster.post('/api/fast', (req, res) => {
  const rawCmd = (req.body.command || 'status').trim();
  const lowerCmd = rawCmd.toLowerCase();
  ledgerBlock++;
  const ts = new Date().toISOString().replace('T', ' ').substring(0, 19);
  const signature = '0x' + Math.random().toString(16).substring(2, 34);

  db.run("INSERT INTO enterprise_ledger (timestamp, category, payload, signature) VALUES (?, ?, ?, ?)",
    [ts, 'BLUE_FIRE_DIRECTIVE', rawCmd, signature]);

  let outputText = '';

  if (lowerCmd.startsWith('planet search')) {
    outputText = `[${ts}] EXOPLANET RECONNAISSANCE SCAN:\n• Top Target 1 : Kepler-186f (ESI: 0.64, Habitable Zone)\n• Top Target 2 : TOI-700 d (ESI: 0.88, 101.4 light-years)\n• Top Target 3 : Proxima Centauri b (ESI: 0.87, Nearest Candidate)\n• Status       : Atmospheric spectrography locked. Ready for clone protocol.`;
  } else if (lowerCmd.startsWith('clone earth')) {
    const target = rawCmd.split('clone earth')[1]?.trim() || 'TOI-700 d';
    db.run("INSERT INTO exoplanet_colonization (target_planet, terraform_stage, timestamp) VALUES (?, ?, ?)", [target, 'STAGE_1_INITIATED', ts]);
    outputText = `[${ts}] CLONED EARTH TERRAFORMING PROTOCOL: "${target}"\n• Stage 1      : Atmospheric balance adjustment (N2/O2 ratio stabilization)\n• Stage 2      : Magnetic field generator deployment via 25 orbital satellites\n• Stage 3      : Hydrosphere & thermal core heating initiated\n• Vault Backing: 0x5f04EBB30d3BBf356263c3ef4823080d05bEDDf5 [$20.00 USDC]\n• Status       : Terraforming matrix executing successfully.`;
  } else {
    outputText = `[${ts}] BLUE-FIRE SUPERCOMPUTER DIRECTIVE: "${rawCmd}"\n• Ledger Block : #${ledgerBlock}\n• Owner        : Salathaniel S A Brown Sr\n• CDP Vault    : 0x5f04EBB30d3BBf356263c3ef4823080d05bEDDf5 [$20.00 USDC]\n• EFLOPS Power : 121.55 EFLOPS (Autonomous Mesh)\n• Auth Sign    : ${signature}`;
  }

  res.json({ status: 'success', output: outputText });
});

// AUXILIARY PORTS
appVector.get('/vector-status', (req, res) => res.json({ service: "Vector Datacenter Core", status: "BLUE_FIRE_ACTIVE", eflops: "121.55 EFLOPS" }));
appLedger.get('/ledger-status', (req, res) => res.json({ service: "Settlement Ledger", status: "SECURED", wallet: "0x5f04EBB30d3BBf356263c3ef4823080d05bEDDf5" }));

// Launch multi-port listeners
http.createServer(appMaster).listen(3001, '0.0.0.0', () => console.log('[Blue-Fire Master] Live on port 3001'));
http.createServer(appVector).listen(8090, '0.0.0.0', () => console.log('[Vector Core] Live on port 8090'));
http.createServer(appLedger).listen(8099, '0.0.0.0', () => console.log('[Settlement Ledger] Live on port 8099'));
