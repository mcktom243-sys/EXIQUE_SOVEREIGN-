#!/bin/bash
# AETHEL TEST INDEPENDENCE PROTOCOL
# Port: 9091 | Target: Experimental Interface

export TARGET_PORT=9091
export TEST_LOGS="~/AETHEL_VAULT/SENTINEL_LOGS/interface.log"

echo "--- AETHEL TEST (9091) INITIALIZED ---"
echo "Status: Independent / Testing Mode"
echo "Protocol: Sigmond String / 1% Discovery"

# Function to ping local test environment
test_pulse() {
    echo "[$(date)] Testing Heartbeat on 9091..." >> $TEST_LOGS
    curl -s -X POST http://localhost:9091/cgi-bin/chat.sh \
         -d "source=test_env&status=active"
}

# Run a self-check
test_pulse
echo "Check ~/AETHEL_VAULT/SENTINEL_LOGS/interface.log for results."
