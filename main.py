import asyncio
from models import brain_matrix

async def main():
    print("Starting TriBrainConsensusLoop engine...")
    # Test execution
    res = await brain_matrix.execute_merged_loop("test_command", "invalid_sig", 1)
    print("Execution Result:", res)

if __name__ == "__main__":
    asyncio.run(main())
