import sys
import os
import json
import subprocess
import time

NODE_WORKER_JS = """
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});

rl.on('line', (line) => {
    if (!line.trim()) return;
    try {
        const data = JSON.parse(line);
        const response = {
            id: data.id || Date.now(),
            satellite_id: data.satellite_id,
            vector_length: data.vector ? data.vector.length : 0,
            status: "NODE_BRIDGED_ACK",
            node_timestamp: Date.now()
        };
        console.log(JSON.stringify(response));
    } catch (err) {
        console.log(JSON.stringify({ error: err.message }));
    }
});
"""

def main():
    with open("_node_worker.js", "w") as f:
        f.write(NODE_WORKER_JS)

    print("==========================================================")
    print("  ⚡ NANO IPC STREAM BRIDGE (Python <-> Node.js Pipe)")
    print("==========================================================")

    proc = subprocess.Popen(
        ["node", "_node_worker.js"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    try:
        for i in range(1, 6):
            payload = {
                "id": 1000 + i,
                "satellite_id": f"NANO-SAT-{i:02d}",
                "vector": [0.015 * i] * 128
            }
            json_str = json.dumps(payload) + "\n"
            proc.stdin.write(json_str)
            proc.stdin.flush()
            
            output = proc.stdout.readline()
            if output:
                res = json.loads(output.strip())
                print(f"[PY -> NODE PIPE]: ACK Recv for {res.get('satellite_id')} | Status: {res.get('status')}")
            
            time.sleep(0.1)

    finally:
        proc.terminate()
        if os.path.exists("_node_worker.js"):
            os.remove("_node_worker.js")
            
    print("==========================================================")
    print("  ✅ NANO PIPE EXECUTION COMPLETE")
    print("==========================================================")

if __name__ == "__main__":
    main()
