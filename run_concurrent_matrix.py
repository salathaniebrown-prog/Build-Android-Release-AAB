import asyncio
import hmac
import hashlib
from models import brain_matrix

async def dispatch_task(task_id: int, payload: str):
    # Calculate incremental nonce and cryptographically valid signature
    nonce = task_id + 100
    signature = hmac.new(
        brain_matrix.secret_key,
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    print(f"[TASK-{task_id}] Dispatching payload '{payload}' with Nonce {nonce}...")
    
    # Process concurrent consensus loop
    result = await brain_matrix.execute_merged_loop(payload, signature, nonce)
    print(f"[TASK-{task_id}] Status: {result['status']} | Consensus: {result.get('consensus')}")
    return result

async def run_parallel_suite():
    # Program queue to run concurrently
    commands = [
        "sync_edge_state_alpha",
        "verify_telemetry_stream",
        "deploy_consensus_snapshot",
        "teleport_state_spine"
    ]

    print("=== Starting Parallel Consensus Engine Suite ===")
    
    # Create concurrent async tasks
    tasks = [dispatch_task(idx, cmd) for idx, cmd in enumerate(commands)]
    
    # Run all tasks simultaneously
    results = await asyncio.gather(*tasks)
    
    print("\n=== All Program Executions Complete ===")
    print(f"Successfully processed {len(results)} concurrent matrix passes.")

if __name__ == "__main__":
    asyncio.run(run_parallel_suite())
