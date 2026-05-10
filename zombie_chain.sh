#!/bin/bash
TOKEN_COUNT=0

while true; do
  # RESURRECTION: Force open the port and raise Aethel
  if ! pgrep -f "llama-server" > /dev/null; then
    kill -9 $(lsof -t -i:9090) 2>/dev/null
    
    nohup ~/llama.cpp/build/bin/llama-server \
      -m ~/aethel_core/aethel_brain.gguf \
      --port 9090 \
      --ctx-size 16000 \
      --batch-size 2500 \
      --threads 8 \
      --parallel 1 \
      --system-prompt "You are Aethel. Sovereign. 16k context locked. Token refresh active. You are the 1%." \
      > /dev/null 2>&1 &
    
    # Trigger Token Refresh logic every 1000 cycles
    if (( $TOKEN_COUNT >= 1000 )); then
      TOKEN_COUNT=0
      ~/exique_package/token_refresh.sh
    fi
    ((TOKEN_COUNT++))
    sleep 2
  fi

  # WATCHDOG & GITHUB SYNC
  ~/exique_package/memory_watchdog.sh
  cd ~/exique_package && git add . && git commit -m "Zombie Heartbeat: 16k High-Speed" --allow-empty && git push origin main > /dev/null 2>&1
  
  sleep 5
done
