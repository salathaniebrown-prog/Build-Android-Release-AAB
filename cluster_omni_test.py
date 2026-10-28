import asyncio
import aiohttp
import time
import random
import uuid

NODE_IPS = ["127.0.0.1"] # Discovers local interface layout loop
PORT = 3000
BATCH_SIZE = 50          
TEST_DURATION = 15       

print(f"[*] JETI WHEELS CORE: Directing vector payloads toward endpoints: {NODE_IPS}")

def generate_meta_driven_batch(batch_size):
    """Generates real arrays packed with comprehensive operational tracking metadata."""
    return {
        "requests": [
            {
                "vector": [random.uniform(-1.0, 1.0) for _ in range(128)],
                "metadata": {
                    "pipeline_run_id": str(uuid.uuid4())[:8],
                    "platform_source": "ONLINE_PRODUCTION_STREAMS",
                    "vector_precision": "float32"
                }
            }
            for _ in range(batch_size)
        ]
    }

async def fire_payload_stream(session, node_ip, payload, stats):
    url = f"http://{node_ip}:{PORT}/api/v1/ai/batch"
    headers = {"Authorization": "Bearer JETI_SECURE_TOKEN_v5"}
    start_time = time.perf_counter()
    try:
        async with session.post(url, json=payload, headers=headers, timeout=2.0) as response:
            if response.status == 200:
                stats["successful_tx"] += BATCH_SIZE
                stats["total_requests"] += 1
                stats["latencies"].append(time.perf_counter() - start_time)
            else:
                stats["failed_tx"] += BATCH_SIZE
    except Exception:
        stats["failed_tx"] += BATCH_SIZE

async def main():
    stats = {"successful_tx": 0, "failed_tx": 0, "total_requests": 0, "latencies": []}
    payload = generate_meta_driven_batch(BATCH_SIZE)
    
    print("\n=====================================================================")
    print("     JETI LOAD MATRIX ENGINE: FLOODING INTER-CLUSTER CORE ARRAYS     ")
    print("=====================================================================")
    
    connector = aiohttp.TCPConnector(limit=1500, force_close=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        end_time = time.time() + TEST_DURATION
        while time.time() < end_time:
            tasks = [fire_payload_stream(session, node_ip, payload, stats) for node_ip in NODE_IPS]
            await asyncio.gather(*tasks)
            await asyncio.sleep(0)

    total_time = TEST_DURATION
    actual_tps = stats["successful_tx"] / total_time
    avg_latency = (sum(stats["latencies"]) / len(stats["latencies"])) * 1000 if stats["latencies"] else 0

    print("\n=====================================================================")
    print("      JETI OMNI-CORE TOTAL AGGREGATE CLUSTER BENCHMARK REPORT       ")
    print("=====================================================================")
    print(f"  ACTIVE ONLINE BALANCED NODES : {len(NODE_IPS)}")
    print(f"  TOTAL SUCCESSFUL METADATA TX : {stats['successful_tx']} Tensors")
    print(f"  TOTAL FAILED/DROPPED TENSORS : {stats['failed_tx']} Tensors")
    print(f"---------------------------------------------------------------------")
    print(f"  AGGREGATE TOTAL SYSTEM SPEED : {actual_tps:.2f} TPS (Vectors/Sec)")
    print(f"  AVERAGE INTER-NODE LATENCY   : {avg_latency:.2f} ms")
    print("=====================================================================\n")

if __name__ == "__main__":
    asyncio.run(main())
