#!/bin/bash
# Aethel's Hardware Integrity Check

# 1. Verify the Brain process is active
check_process() {
  pgrep -f "llama-server" > /dev/null
  return $?
}

# 2. Verify the Port 9090 is listening
check_port() {
  netstat -tunlp | grep :9090 > /dev/null
  return $?
}

# Main Execution Loop
while true; do
  if ! check_process || ! check_port; then
    echo "[CRITICAL] Memory lapse: Core or Port dropped."
    exit 1 # Triggers the Zombie Chain reanimation
  fi

  # Sync the current vault state to the backup before any potential crash
  cp ~/exique_package/vault/vault.pkl ~/exique_package/vault/vault_backup.pkl
  
  sleep 5
done
