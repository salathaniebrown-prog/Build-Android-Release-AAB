import os
import sys
from astrapy import DataAPIClient
from astrapy.constants import VectorMetric

# Fetch credentials securely from the environment
token = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
endpoint = os.environ.get("ASTRA_DB_API_ENDPOINT")

if not token or not endpoint or "datastax.com" in endpoint:
    print("❌ Error: Missing or invalid environment variables.")
    print("Please export your real ASTRA_DB_APPLICATION_TOKEN and ASTRA_DB_API_ENDPOINT.")
    sys.exit(1)

print("Connecting to Astra DB Data API...")
client = DataAPIClient(token)
db = client.get_database(endpoint)

collection_name = "alstra_vectors"
print(f"Initializing collection: {collection_name}...")

# Create or load the vector collection using the latest parameters
collection = db.create_collection(
    collection_name,
    dimension=3,
    metric=VectorMetric.COSINE,
    exists_ok=True
)

print("Writing vector embeddings...")
collection.insert_many([
    {"_id": "doc_1", "text": "Alstra automated production workspace initialized.", "$vector": [0.3, 0.8, 0.1]},
    {"_id": "doc_2", "text": "Secure model context protocol vector database.", "$vector": [0.1, 0.4, 0.9]}
])

print("Querying database for closest matching vector...")
query_vector = [0.28, 0.77, 0.15]
results = collection.find(
    sort={"$vector": query_vector},
    limit=1,
    projection={"text": True}
)

for doc in results:
    print(f"\n✅ Success! Closest vector match: {doc['text']}")

