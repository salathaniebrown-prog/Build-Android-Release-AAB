import os
from astrapy import DataAPIClient

token = "os.getenv("ASTRA_DB_TOKEN", "PLACEHOLDER")"
endpoint = "https://datastax.com"

client = DataAPIClient()
db = client.get_database(endpoint, token=token, keyspace="default_keyspace")
collection = db.get_collection("super_agent_intelligence_vault")

print("📥 Posting testing documentation package directly...")
collection.insert_one({
    "_id": "doc_01",
    "$vectorize": "Supercomputer node-01 metrics are within optimal parameters.",
    "metadata": {"status": "nominal", "node": "NEXUS-NODE-BROWN"}
})
print("💾 Payload accepted by cloud registry.")

print("🔍 Validating index contents...")
for doc in collection.find(limit=1):
    print(f"🎉 Retrieved: {doc}")
