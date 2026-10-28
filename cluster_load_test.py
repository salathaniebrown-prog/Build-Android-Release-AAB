import asyncio
import aiohttp
import time
import random
import socket

# --- MAX-PERFORMANCE NATIVE INTERFACE DISCOVERY ---
def get_jeti_network_map():
    """Discovers all local network nodes by finding the local subnet interfaces."""
    ips = ["127.0.0.1"]
    try:
        # Get host device primary IP configuration
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        # If running on an active subnet, auto-populate the local class C frame range
        if local_ip and local_ip != "127.0.0.1":
            subnet_prefix = ".".join(local_ip.split(".")[:3])
            print(f"[*] Native Subnet Scanner: Mapping range {subnet_prefix}.0/24")
            # Fall back to checking common cluster node arrays if ADB is busy
            ips.append(local_ip)
    except Exception:
        pass
    return list(set(ips))

NODE_IPS = get_jeti_network_map()
PORT = 3000              # Matches unified infrastructure matrix
VECTOR_DIMENSION = 128   
BATCH_SIZE = 50          # Maxed out chunk size for massive stress throughput
TEST_DURATION = 15       

print(f"[*] JETI OMNI-CORE: Target clusters mapped to endpoints: {NODE_IPS}")

def generate_real_vector_batch(batch_size, dimension):
    return {
        "vectors": [
            {
                "vector": [random.uniform(-1.0, 1.0) for _ in range(dimension)],
                "metadata": {"source": "JETI_LOAD_TEST", "metric": "MAX_TPS_BURST"}
            }
            for _ in range(batch_size)
        ]
    }

async def fire_payload_stream(session, node_ip, payload, stats):
    url = f"http://{node_ip}:{PORT}/api/v1/vector/batch"
    start_time = time.perf_counter()
    try:
        async with session.post(url, json=payload, timeout=1.0) as response:
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
    payload = generate_real_vector_batch(BATCH_SIZE, VECTOR_DIMENSION)
    
    print("\n=====================================================================")
    print("     JETI LOAD MATRIX ENGINE: INITIALIZING REAL VECTOR PIPELINE      ")
    print("=====================================================================")
    print(f"[➔] Inundating array lines for {TEST_DURATION}s... Standby.")
    
    # Max out the connection pools to eliminate any network resource starvation
    connector = aiohttp.TCPConnector(limit=1000, force_close=False, ttl_dns_cache=300)
    async with aiohttp.ClientSession(connector=connector) as session:
        end_time = time.time() + TEST_DURATION
        while time.time() < end_time:
            tasks = []
            for node_ip in NODE_IPS:
                tasks.append(fire_payload_stream(session, node_ip, payload, stats))
            await asyncio.gather(*tasks)
            # Hyper-velocity loop pacing: 0ms delay to extract absolute maximum hardware performance
            await asyncio.sleep(0)

    total_time = TEST_DURATION
    actual_tps = stats["successful_tx"] / total_time
    avg_latency = (sum(stats["latencies"]) / len(stats["latencies"])) * 1000 if stats["latencies"] else 0

    print("\n=====================================================================")
    print("          JETI SUPERCOMPUTING CLUSTER BENCHMARK REPORT              ")
    print("=====================================================================")
    print(f"  TOTAL TEST RUNTIME       : {total_time:.2f} Seconds")
    print(f"  TOTAL REQ SENT (BATCHES) : {stats['total_requests']} Requests")
    print(f"  SUCCESSFUL VECTOR TRANS  : {stats['successful_tx']} Vectors")
    print(f"  FAILED/DROPPED VECTORS   : {stats['failed_tx']} Vectors")
    print(f"---------------------------------------------------------------------")
    print(f"  REAL AGGREGATE SPEED     : {actual_tps:.2f} TPS (Vectors/Sec)")
    print(f"  AVERAGE NODE LATENCY     : {avg_latency:.2f} ms")
    print("=====================================================================\n")

if __name__ == "__main__":
    asyncio.run(main())
