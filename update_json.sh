#!/data/data/com.termux/files/usr/bin/bash

# Usage: ./update_json.sh <json_file> <jq_filter>
# Example: ./update_json.sh astra_manifest.json '(.artifacts[] | select(.phase == 3)).status = "VERIFIED"'

FILE="$1"
FILTER="$2"

# 1. Check if both arguments are provided
if [ -z "$FILE" ] || [ -z "$FILTER" ]; then
    echo "Error: Missing arguments."
    echo "Usage: $0 <file.json> '<jq_filter>'"
    exit 1
fi

# 2. Check if file exists
if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found."
    exit 1
fi

# 3. Create a secure temporary file
TMP_FILE=$(mktemp)

# 4. Process JSON via jq and capture exit code
if jq "$FILTER" "$FILE" > "$TMP_FILE"; then
    # Validate that the resulting temp file is valid JSON before overwriting
    if jq empty "$TMP_FILE" 2>/dev/null; then
        mv "$TMP_FILE" "$FILE"
        echo "Successfully updated '$FILE'."
    else
        echo "Error: Filter output generated invalid JSON. Aborting write."
        rm -f "$TMP_FILE"
        exit 1
    fi
else
    echo "Error: jq failed to process filter. File remained untouched."
    rm -f "$TMP_FILE"
    exit 1
fi
