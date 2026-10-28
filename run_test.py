import asyncio
import hmac
import hashlib
from models import brain_matrix

async def main():
    payload = "execute_consensus_action"
    nonce = 1
    
    # Compute valid HMAC-SHA256 signature using the secret key
    valid_sig = hmac.new(
        brain_matrix.secret_key, 
        payload.encode(), 
        hashlib.sha256
    ).hexdigest()

    print(f"[TEST] Sending command with valid signature: {valid_sig[:12]}...")
    
    # Dispatch execution loop
    result = await brain_matrix.execute_merged_loop(payload, valid_sig, nonce)
    print("\n[RESULT] Execution Output:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
