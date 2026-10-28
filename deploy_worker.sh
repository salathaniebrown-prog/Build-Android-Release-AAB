#!/data/data/com.termux/files/usr/bin/bash

WORKER_NAME="eagle-eyes-world-data-edge"
CF_ACCOUNT_ID="7449335e43208aea043940080e60ba39"
CF_EMAIL="Salathaniebrown@gmail.com"
CF_KEY="PASTE_YOUR_GLOBAL_API_KEY"

cat << 'META' > metadata.json
{
  "main_module": "index.js",
  "compatibility_date": "2026-10-27"
}
META

echo "Pinging Cloudflare Edge..."
curl -s -X PUT "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/workers/scripts/${WORKER_NAME}" \
  -H "X-Auth-Email: ${CF_EMAIL}" \
  -H "X-Auth-Key: ${CF_KEY}" \
  -F "metadata=@metadata.json;type=application/json" \
  -F "index.js=@index.js;type=application/javascript+module" | jq .

rm -f metadata.json
