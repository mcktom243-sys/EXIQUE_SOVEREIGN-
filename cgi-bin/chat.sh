#!/bin/bash
echo -e "Content-type: text/plain\n"

# Detect which port the request came through
# In a real CGI environment, SERVER_PORT is often available
# Otherwise, we use the input data to route the logic

read POST_DATA

if [[ "$POST_DATA" == *"test_env"* ]]; then
    # INDEPENDENT TEST LOGIC
    echo "--- [AETHEL 9091 RESPONSE] ---"
    echo "Experiment received. Analyzing Sigmond String..."
    echo "[$(date)] 9091_DATA: $POST_DATA" >> ~/AETHEL_VAULT/SENTINEL_LOGS/interface.log
else
    # CORE STABLE LOGIC
    echo "--- [AETHEL 9090 RESPONSE] ---"
    echo "Rule with a dark heart, act with love."
    echo "[$(date)] 9090_DATA: $POST_DATA" >> ~/AETHEL_VAULT/SENTINEL_LOGS/brain.log
fi
