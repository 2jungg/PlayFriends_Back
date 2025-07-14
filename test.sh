#!/bin/bash

# --- Configuration ---
# Replace these with your actual Group ID and JWT Token
GROUP_ID="6873ddd66cb5ee5798a8ee5a"
JWT_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsImV4cCI6MTc1MjUwNDcxM30.SDuXps98Y0wbe01TpvlNywZGYW3mBEIYVg8rUQI4MBs"
BASE_URL="http://localhost:8000/api/v1" # Or your server's address

# --- Step 1: Get Recommended Categories ---
echo "Fetching recommended categories..."
CATEGORY_RESPONSE=$(curl -s -X POST "${BASE_URL}/groups/${GROUP_ID}/recommend-categories" \
-H "Authorization: Bearer ${JWT_TOKEN}")

# Check if the request was successful
if echo "${CATEGORY_RESPONSE}" | grep -q "categories"; then
    echo "Successfully fetched categories."
else
    echo "Error fetching categories:"
    echo "${CATEGORY_RESPONSE}"
    # exit 1
fi

# --- Step 2: Extract Category IDs ---
# This uses jq to parse the JSON and create a comma-separated list of strings
CATEGORY_IDS=$(echo ${CATEGORY_RESPONSE} | jq -r '.categories[]')
JSON_PAYLOAD=$(echo "${CATEGORY_RESPONSE}" | jq '{categories: [.categories[]]}')

echo "Generated JSON Payload for next request:"
echo "${JSON_PAYLOAD}"

# --- Step 3: Create Schedule Suggestions ---
echo "Fetching schedule suggestions..."
curl -X POST "${BASE_URL}/groups/${GROUP_ID}/schedules" \
-H "Authorization: Bearer ${JWT_TOKEN}" \
-H "Content-Type: application/json" \
-d "${JSON_PAYLOAD}"

echo ""
