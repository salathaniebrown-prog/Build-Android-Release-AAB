import asyncio
import hmac
import hashlib
import time
from models import brain_matrix

class PackageBatchRunner:
    def __init__(self, batch_size=5):
        self.batch_size = batch_size
        self.nonce_tracker = int(time.time())

    def generate_signature(self, payload: str, nonce: int) -> str:
        return hmac.new(
            brain_matrix.secret_key,
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

    async def execute_package_program(self, prog_id: int, program_name: str):
        self.nonce_tracker += 1
        nonce = self.nonce_tracker
        signature = self.generate_signature(program_name, nonce)
        
        print(f"[PROG-{prog_id:02d}] Executing: '{program_name}' | Nonce: {nonce}")
        
        start_t = time.perf_counter()
        res = await brain_matrix.execute_merged_loop(program_name, signature, nonce)
        elapsed = (time.perf_counter() - start_t) * 1000
        
        status = res.get("status")
        consensus = res.get("consensus")
        print(f"[PROG-{prog_id:02d}] -> Status: {status} | Consensus: {consensus} ({elapsed:.1f}ms)")
        return res

    async def run_queue(self, program_list: list):
        print(f"=== Starting Package System Execution (Total Jobs: {len(program_list)}) ===")
        print(f"=== Max Concurrent Programs Per Batch: {self.batch_size} ===")
        
        # Split program workload into concurrent batches
        for i in range(0, len(program_list), self.batch_size):
            chunk = program_list[i:i + self.batch_size]
            print(f"\n--- Batch Workload [{i+1} to {i+len(chunk)}] ---")
            tasks = [self.execute_package_program(i + idx + 1, prog) for idx, prog in enumerate(chunk)]
            await asyncio.gather(*tasks)
            
        print("\n=== All Package Programs Completed Successfully ===")

if __name__ == "__main__":
    # Define multi-program execution queue
    programs_to_run = [
        "core_telemetry_collector",
        "ed25519_key_rotation",
        "state_spine_synchronizer",
        "edge_node_heartbeat_ping",
        "database_snapshot_archiver",
        "consensus_matrix_auditor",
        "high_priority_routing_pipeline",
        "security_policy_validator"
    ]

    runner = PackageBatchRunner(batch_size=4)
    asyncio.run(runner.run_queue(programs_to_run))
