#!/bin/bash

WEBPAGES_DIR="web_pages"
UTILS_FILE="utils.py"

# Extract all match IDs (quoted hex strings) inside ignore dict from utils.py
match_ids=($(grep -oP '"[a-f0-9]{8}"' "$UTILS_FILE" | tr -d '"' | sort -u))

echo "Found ${#match_ids[@]} match IDs to delete."

for match_id in "${match_ids[@]}"; do
    # Find files named exactly "$match_id" or "$match_id.*" and delete them
    find "$WEBPAGES_DIR" -type f \( -name "$match_id" -o -name "$match_id" \) -print -exec rm -f {} \;
done
