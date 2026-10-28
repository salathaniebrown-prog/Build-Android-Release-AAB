const fs = require('fs');
const path = require('path');
const http = require('http');

const csvFilePath = path.join(__dirname, 'ticker_log.csv');
const backupDir = path.join(__dirname, 'backups');
let updateCounter = 0;

if (!fs.existsSync(csvFilePath)) {
  fs.writeFileSync(csvFilePath, 'Timestamp,Asset,Price_USD\n', 'utf8');
}

function forwardTelemetryToBackend(payload) {
  const dataString = JSON.stringify(payload);
  const options = {
    hostname: '127.0.0.1',
    port: 3000,
    path: '/api/telemetry',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': dataString.length
    }
  };
  const req = http.request(options);
  req.on('error', () => {});
  req.write(dataString);
  req.end();
}

function triggerAutoBackup() {
  if (!fs.existsSync(csvFilePath)) return;
  if (!fs.existsSync(backupDir)) {
    fs.mkdirSync(backupDir, { recursive: true });
  }
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const destinationFile = path.join(backupDir, `ticker_log_bak_${timestamp}.csv`);
  fs.copyFile(csvFilePath, destinationFile, () => {});
}

const ws = new WebSocket('wss://://coinbase.com');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: "subscribe",
    product_ids: ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "DOGE-USD", "ADA-USD"],
    channels: ["ticker"]
  }));
  console.log("[*] Ingestion pipeline synchronized. Forwarding to backend on port 3000...");
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.price) {
    const timestampISO = new Date().toISOString();
    const asset = data.product_id;
    const price = parseFloat(data.price);

    fs.appendFile(csvFilePath, `${timestampISO},${asset},${price.toFixed(4)}\n`, () => {});

    const telemetryPayload = {
      event: "ticker_update",
      source: "coinbase_advanced_feed",
      timestamp: timestampISO,
      telemetry: {
        asset: asset,
        price_usd: price,
        sequence_id: updateCounter
      },
      persistence_layer: {
        local_ledger_updated: true,
        total_batch_count: updateCounter
      },
      hardware_telemetry: {
        node_status: "ONLINE",
        active_threads_allocated: 64
      }
    };

    forwardTelemetryToBackend(telemetryPayload);
    console.log(`[FORWARDED] ${asset} ──> $${price.toFixed(4)}`);

    updateCounter++;
    if (updateCounter >= 1000) {
      updateCounter = 0;
      triggerAutoBackup();
    }
  }
};
