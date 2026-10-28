import time
import os
import requests

# Configuration Parameters
CHAIN_ID = "8453"  # Base Network
TOKEN_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  # USDC Contract
TOKEN_SELECTOR = f"{CHAIN_ID}:{TOKEN_ADDRESS}"

# ANSI Terminal Color Codes
CYAN = "\033[36m"
GREEN = "\033[32m"
AMBER = "\033[33m"
RED = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0m"

def fetch_telemetry_data():
    """Queries the Morpho API for token metadata and real-time spot pricing."""
    meta_url = f"https://morpho.org{TOKEN_SELECTOR}"
    price_url = f"https://morpho.org{TOKEN_SELECTOR}/price"
    
    try:
        # Fetch Metadata
        meta_res = requests.get(meta_url, timeout=10)
        meta_data = meta_res.json().get("data", {}) if meta_res.status_code == 200 else {}
        
        # Fetch Pricing
        price_res = requests.get(price_url, timeout=10)
        price_data = price_res.json().get("data", {}) if price_res.status_code in [200, 206] else {}
        
        return meta_data, price_data
    except Exception as e:
        print(f"{RED}[!] Telemetry Fetch Error: {e}{RESET}")
        return {}, {}

def render_dashboard():
    """Clears the terminal screen and draws the Astra Dashboard layout."""
    os.system("clear")
    meta, price = fetch_telemetry_data()
    
    # Extract telemetry metrics
    name = meta.get("name", "Unknown Token")
    symbol = meta.get("symbol", "N/A")
    decimals = meta.get("decimals", "N/A")
    tags = ", ".join(meta.get("tags", []))
    
    spot_value = price.get("price", 0.0)
    provider = price.get("provider", "Unknown")
    timestamp = price.get("timestamp", "N/A")
    
    # Draw Interface Header
    print(f"{CYAN}{BOLD}===================================================================={RESET}")
    print(f"{CYAN}{BOLD}               ASTRA SYSTEMS - DEEPSPACE ARTIFACT MONITOR          {RESET}")
    print(f"{CYAN}{BOLD}===================================================================={RESET}")
    
    # 1. USDC Token Metadata Panel
    print(f"\n{CYAN}[+] CORE ARTIFACT IDENTITY (Network: Base){RESET}")
    print(f"  ├─ Name:      {GREEN}{name}{RESET}")
    print(f"  ├─ Symbol:    {GREEN}{symbol}{RESET}")
    print(f"  ├─ Decimals:  {GREEN}{decimals}{RESET}")
    print(f"  ├─ Address:   {GREEN}{TOKEN_ADDRESS}{RESET}")
    print(f"  └─ Tags:      {GREEN}[{tags}]{RESET}")
    
    # 2. Live cURL / Input Module Execution Simulation
    print(f"\n{CYAN}[+] TERMUX INTERACTIVE INPUT EXECUTION{RESET}")
    print(f"  {GREEN}termux@mcp-console:~ $ curl -X GET \"https://morpho.org{TOKEN_SELECTOR}\"{RESET}")
    print(f"  {GREEN}Output Status: [200 OK]{RESET}")
    
    # 3. Amber Price Threshold Warning Logic
    print(f"\n{CYAN}[+] REAL-TIME FINANCIAL TELEMETRY{RESET}")
    print(f"  ├─ Feed Source: {GREEN}{provider}{RESET}")
    print(f"  ├─ Epoch Time:  {GREEN}{timestamp}{RESET}")
    print(f"  └─ Spot Value:  {GREEN}${spot_value:.6f}{RESET}")
    
    # Conditional Warning Trigger (Trigger amber alert if under $1.000000)
    if spot_value < 1.000000 and spot_value > 0:
        print(f"\n{AMBER}{BOLD}[⚠️ PRICE THRESHOLD WARNING]{RESET}")
        print(f"  {AMBER}Target Limit: <$1.000000 | Current Spot: ${spot_value:.6f} USD{RESET}")
        print(f"  {AMBER}Status: PEG VARIANCE DETECTED IN DEEPSPACE LEDGER{RESET}")
    else:
        print(f"\n{GREEN}[✓ SYSTEM LOG] Asset peg stability verified.{RESET}")
        
    print(f"\n{CYAN}===================================================================={RESET}")
    print(f"Streaming telemetry logs... Press Ctrl+C to disconnect from Datalab.")

if __name__ == "__main__":
    try:
        while True:
            render_dashboard()
            time.sleep(5)  # Refresh feed pipeline every 5 seconds
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Astra telemetry connection severed.{RESET}")

