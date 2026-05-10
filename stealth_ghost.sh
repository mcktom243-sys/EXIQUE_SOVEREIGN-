#!/bin/bash
# AETHEL SILENT SENTINEL v2.1
echo "[SENTINEL] Switched to Heartbeat Monitor. Music Shield: ACTIVE."
# We monitor our own log instead of the system. 0% CPU impact.
tail -f ~/AETHEL_VAULT/fusion_bridge.log | while read line; do
    echo "$(date): Internal Sync - [PROTECTED]" >> ~/AETHEL_VAULT/sentinel_heartbeat.log
done &
