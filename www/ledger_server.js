const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8080;
const FILE_PATH = path.join(__dirname, 'telemetry_ledger.jsonl');

const server = http.createServer((req, res) => {
    if (req.method === 'POST') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                const record = {
                    id: Date.now(),
                    satellite_id: data.satellite_id,
                    status: data.status,
                    cosine_similarity: data.cosine_similarity,
                    processed_at: data.processed_at_epoch || Date.now()
                };

                // Append record to JSONL file
                fs.appendFile(FILE_PATH, JSON.stringify(record) + '\n', (err) => {
                    if (err) {
                        console.error('[STORAGE ERROR]:', err.message);
                        res.writeHead(500, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ error: err.message }));
                        return;
                    }

                    console.log(`[LEDGER STORED]: Satellite=${data.satellite_id} | Status=${data.status} | Similarity=${data.cosine_similarity}`);
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ ledger_status: "SUCCESS", record_id: record.id }));
                });
            } catch (e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: "Invalid JSON payload" }));
            }
        });
    } else if (req.method === 'GET' && req.url === '/ledger/stats') {
        fs.readFile(FILE_PATH, 'utf8', (err, fileData) => {
            if (err) {
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ total_records: 0, avg_similarity: 0.0 }));
                return;
            }

            const lines = fileData.trim().split('\n').filter(Boolean);
            let totalSim = 0;

            lines.forEach(line => {
                try {
                    const parsed = JSON.parse(line);
                    totalSim += parsed.cosine_similarity || 0;
                } catch (e) {}
            });

            const count = lines.length;
            const avg = count > 0 ? totalSim / count : 0.0;

            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ total_records: count, avg_similarity: Number(avg.toFixed(4)) }));
        });
    } else {
        res.writeHead(404);
        res.end();
    }
});

server.listen(PORT, () => {
    console.log(`[NODE LEDGER LISTENING]: Persistent Engine active on http://127.0.0.1:${PORT}`);
});
