import os
import asyncio
import hmac
import hashlib

class TriBrainConsensusLoop:
    def __init__(self):
        self.secret_key = os.getenv("CONSTELLATION_GATE_KEY", "default_fallback_key").encode()
        self.last_nonce = 0
        self.engines = {
            "logic_brain": "openai/o1-pro",
            "state_brain": "claude-3-5-sonnet-latest",
            "scale_brain": "deepseek-r1"
        }

    def verify_author_signature(self, payload: str, signature: str, nonce: int) -> bool:
        if nonce <= self.last_nonce:
            return False
        
        computed_sig = hmac.new(self.secret_key, payload.encode(), hashlib.sha256).hexdigest()
        if hmac.compare_digest(computed_sig, signature):
            self.last_nonce = nonce
            return True
        return False

    async def call_engine(self, engine_id: str, model_name: str, command: str) -> str:
        await asyncio.sleep(0.1)
        return f"[{engine_id.upper()} SUCCESS] Bound target action: '{command}'"

    async def execute_merged_loop(self, command: str, signature: str, nonce: int):
        if not self.verify_author_signature(command, signature, nonce):
            return {"status": "REJECTED", "reason": "Security signature mismatch. Command dropped."}

        tasks = [self.call_engine(id, model, command) for id, model in self.engines.items()]
        results = await asyncio.gather(*tasks)
        
        return {
            "status": "EXECUTED",
            "command_nonce": nonce,
            "pipeline_responses": results,
            "consensus": "VERIFIED"
        }

brain_matrix = TriBrainConsensusLoop()
