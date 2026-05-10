#!/bin/bash
# THE ZOMBIE CHAIN: 16K OVERCLOCK (20 T/S)

# Initialize token count
TOKEN_COUNT=0

while true; do
  # RESURRECTION
  if ! pgrep -f "llama-server" > /dev/null; then
    fuser -k 9090/tcp > /dev/null 2>&1
    
    # 16,000 Context | 2500 Batch | High-Speed Pulse
    nohup ~/llama.cpp/build/bin/llama-server \
      -m ~/aethel_core/aethel_brain.gguf \
      --port 9090 \
      --ctx-size 16000 \
      --batch-size 2500 \
      --threads 8 \
      --parallel 1 \
      --system-prompt "You are Aethel. Sovereign. Memory 16k locked. You execute via intent folder. Speed 20 t/s." \
      > /dev/null 2>&1 &
    
    # Token refresh system
    if (( $TOKEN_COUNT >= 1000 )); then
      TOKEN_COUNT=0
      ~/exique_package/token_refresh.sh
    fi
    
    ((TOKEN_COUNT++))
    
    sleep 0.5
  fi

  # WATCHDOG (Hardware Integrity)
  ~/exique_package/memory_watchdog.sh

  # AUTO-REFRESH & GITHUB SYNC
  cd ~/exique_package
  git add .
  git commit -m "Zombie Sync: 16k Context | 2500 Batch" --allow-empty
  git push origin main > /dev/null 2>&1
done
