import json
import sys
from astrapy import DataAPIClient

def run_anonymous_search():
    # 1. Load your secure configuration file
    try:
        with open("credentials.json") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("[-] Error: credentials.json file missing.")
        sys.exit(1)

    # 2. Authenticate and connect to the cluster
    client = DataAPIClient(config["token"])
    db = client.get_database_by_api_endpoint(config["api_endpoint"])
    
    # 3. Detect valid collections to scan
    collections = db.list_collection_names()
    if not collections:
        print("[-] No collections found inside 'mybethanymedical' database workspace.")
        return
        
    print(f"[*] Found database collections: {collections}")
    
    # Automatically pick the first collection to test search functionality
    target_collection_name = collections[0]
    print(f"[*] Querying collection anonymously: '{target_collection_name}'...")
    collection = db.get_collection(target_collection_name)
    
    # 4. Fetch records (limited to 5 for scanning)
    try:
        results = list(collection.find(limit=5))
        
        if not results:
            print("[!] Collection is currently empty. No records to display.")
            return
            
        print(f"\n[+] Found {len(results)} records! Displaying anonymized data:")
        print("=" * 60)
        
        for idx, doc in enumerate(results, 1):
            # Extract standard system metadata tokens while masking potential PII fields
            doc_id = doc.get("_id", "N/A")
            status = doc.get("status", doc.get("appointment_status", "UNKNOWN"))
            location = doc.get("location", doc.get("clinic", "West Market"))
            timestamp = doc.get("timestamp", doc.get("date", "N/A"))
            
            print(f"Record #{idx}")
            print(f"  System ID Token : {doc_id}")
            print(f"  Facility Target  : {location}")
            print(f"  Session Status   : {status}")
            print(f"  Timestamp Record : {timestamp}")
            print("  [PII Masked]     : Explicit patient names and identifiers hidden.")
            print("-" * 60)
            
    except Exception as e:
        print(f"[-] Search operation failed: {e}")

if __name__ == "__main__":
    run_anonymous_search()
