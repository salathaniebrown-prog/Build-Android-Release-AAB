#!/data/data/com.termux/files/usr/bin/bash

FILE="$1"
shift

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
    echo "Error: Target JSON file missing or invalid."
    exit 1
fi

TMP_FILE=$(mktemp)
CP_FILE="${FILE}.bak.$(date +%s)"

JQ_ARGS=()
TRANSFORMS=()

for pair in "$@"; do
    KEY="${pair%%=*}"
    VAL="${pair#*=}"

    if [ -n "$KEY" ] && [ -n "$VAL" ]; then
        if echo "$VAL" | jq empty 2>/dev/null; then
            JQ_ARGS+=(--argjson "$KEY" "$VAL")
        else
            JQ_ARGS+=(--arg "$KEY" "$VAL")
        fi

        case "$KEY" in
            VERSION) TRANSFORMS+=(".version = \$$KEY") ;;
            LEAD_NAME) TRANSFORMS+=(".operatorAuthority.leadOperator = \$$KEY") ;;
            CO_BENEFICIARY) TRANSFORMS+=(".operatorAuthority.coBeneficiary = \$$KEY") ;;
            PRIMARY_SHARE) TRANSFORMS+=(".operatorAuthority.primaryShare = \$$KEY") ;;
            SECONDARY_SHARE) TRANSFORMS+=(".operatorAuthority.secondaryShare = \$$KEY") ;;
            *) TRANSFORMS+=(".$KEY = \$$KEY") ;;
        esac
    fi
done

# Explicitly join array elements with ' | ' pipe operators for jq
JOINED_FILTER=""
for t in "${TRANSFORMS[@]}"; do
    if [ -z "$JOINED_FILTER" ]; then
        JOINED_FILTER="$t"
    else
        JOINED_FILTER="$JOINED_FILTER | $t"
    fi
done

if [ -z "$JOINED_FILTER" ]; then
    echo "Error: No valid KEY=VALUE pairs supplied."
    rm -f "$TMP_FILE"
    exit 1
fi

if jq "${JQ_ARGS[@]}" "$JOINED_FILTER" "$FILE" > "$TMP_FILE"; then
    if jq empty "$TMP_FILE" 2>/dev/null; then
        cp "$FILE" "$CP_FILE"
        mv "$TMP_FILE" "$FILE"
        echo "Successfully updated '$FILE' (Backup: $CP_FILE)."
    else
        echo "Error: Output generated invalid JSON."
        rm -f "$TMP_FILE"
        exit 1
    fi
else
    echo "Error: jq batch processing failed."
    rm -f "$TMP_FILE"
    exit 1
fi
