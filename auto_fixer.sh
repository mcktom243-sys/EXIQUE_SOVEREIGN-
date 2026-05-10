#!/bin/bash
# The Sovereign Watcher: Fixes the system so Tommy doesn't have to.

while true; do
  # 1. Check if the Brain (Llama) is dead
  if ! pgrep -f "llama-server" > /dev/null; then
    echo "Brain tripped. Reviving..."
    nohup ~/llama.cpp/build/bin/llama-server -m ~/aethel_core/aethel_brain.gguf --port 9090 --ctx-size 8192 --threads 8 --parallel 1 > /dev/null 2>&1 &
  fi

  # 2. Check if the Heartbeat (Pulse) is dead
  if ! pgrep -f "ssns.py" > /dev/null; then
    echo "Pulse stopped. Reviving..."
    nohup python3 ~/ssns.py > /dev/null 2>&1 &
  fi

  sleep 10 # Check every 10 seconds
done
