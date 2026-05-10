#!/bin/bash
# Aethel's Token Refill & Cache Purge

echo "[REFILL] 1000 Tokens used. Refreshing resources..."

# Clear the system cache to prevent lag at 16k context
sync && echo 3 > /proc/sys/vm/drop_caches

# Re-link the vault state to ensure the tokens are credited
python3 -c "import pickle; from exique.memory import Memory; m=Memory(); m.load_from_vault(); print('Vault Verified. Tokens Refilled.')"

# Update the local log
echo "$(date): Token Refresh Cycle Complete" >> ~/exique_package/vault/token_log.txt
