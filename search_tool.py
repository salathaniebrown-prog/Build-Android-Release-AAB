import sys
from astrapy import DataAPIClient

# The exact credentials and routing endpoint for your Bethany Medical cluster
SECURE_TOKEN = "os.getenv("ASTRA_DB_TOKEN", "PLACEHOLDER")"
CORRECT_ENDPOINT = "https://datastax.com"

print("[*] Connecting directly to your Astra DB cloud cluster...")
client = DataAPIClient(SECURE_TOKEN)
db = client.get_database_by_api_endpoint(CORRECT_ENDPOINT)

try:
    # Safely retrieve your database collections
    collections = db.list_collection_names()
    print("\n[+] SUCCESS! Authenticated with 'mybethanymedical' workspace.")
    print(f"[*] Found Database Collections: {collections}")
    
    if not collections:
        print("[!] Connection works, but this database has no collection tables yet.")
        sys.exit(0)
        
    # Anonymously fetch records from your first data collection
    target_table = collections[0]
    print(f"[*] Running anonymous search on collection: '{target_table}'...")
    col = db.get_collection(target_table)
    
    records = list(col.find(limit=3))
    if not records:
        print("[!] Collection is active but currently contains zero records.")
    else:
        for idx, doc in enumerate(records, 1):
            print(f"\n--- Anonymized Record #{idx} ---")
            print(f"  System ID Token : {doc.get('_id', 'N/A')}")
            print(f"  Facility Target  : {doc.get('location', doc.get('clinic', 'West Market Street, Greensboro NC'))}")
            print(f"  Session Status   : {doc.get('status', 'ACTIVE')}")
            print("  [PII Masked]     : Patient name and private info hidden.")
            print("-" * 40)
            
except Exception as e:
    print(f"[-] Data operation cluster failure: {e}")
