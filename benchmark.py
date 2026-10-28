import asyncio
import time
import requests

TARGET_URL = "http://127.0.0.1:8888/"
TOTAL_REQUESTS = 500
CONCURRENCY = 20

def fetch(session, url):
    try:
        start = time.perf_counter()
        res = session.get(url, timeout=5)
        latency = (time.perf_counter() - start) * 1000
        return res.status_code, latency
    except Exception as e:
        return 500, 0.0

async def worker(queue, results):
    session = requests.Session()
    while not queue.empty():
        url = await queue.get()
        # Execute request off the event loop thread
        status, latency = await asyncio.to_thread(fetch, session, url)
        results.append((status, latency))
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    for _ in range(TOTAL_REQUESTS):
        queue.put_nowait(TARGET_URL)

    results = []
    start_time = time.perf_counter()

    workers = [asyncio.create_task(worker(queue, results)) for _ in range(CONCURRENCY)]
    await queue.join()

    for w in workers:
        w.cancel()

    total_time = time.perf_counter() - start_time
    successful = [r[1] for r in results if r[0] == 200]
    
    avg_latency = sum(successful) / len(successful) if successful else 0
    rps = len(results) / total_time

    print("=" * 50)
    print("       ALSTRA TELEMETRY ENGINE BENCHMARK        ")
    print("=" * 50)
    print(f"Total Requests Processed : {len(results)}")
    print(f"Concurrent Workers       : {CONCURRENCY}")
    print(f"Total Execution Time     : {total_time:.3f} seconds")
    print(f"Throughput (RPS)         : {rps:.2f} req/sec")
    print(f"Average Node Latency     : {avg_latency:.2f} ms")
    print(f"Success Rate             : {(len(successful)/len(results))*100:.1f}%")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())

