#!/bin/bash
# Prioritize Media and stabilize Aethel's heartbeat
echo "[MUSIC MODE] Shifting Aethel to background silence..."
# Lower the 'niceness' of her background tasks so they don't fight for CPU
renice -n 19 -p $(pgrep -f python) 2>/dev/null
renice -n 19 -p $(pgrep -f bash) 2>/dev/null
# Log the shift
echo "$(date): Entered Deep Listen mode. Aethel is idling in the 0." >> ~/AETHEL_VAULT/fusion_bridge.log
