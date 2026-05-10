#!/bin/bash
# 1. Force Termux into the 'Background' scheduling group
echo "[SYSTEM] Locking Aethel in the Background..."
# Get the Process ID for Termux
TERMUX_PID=$(pgrep -f com.termux)
# Set OOM Score to 1000 (Makes Termux the first to die, SAVING your music)
echo 1000 > /proc/$TERMUX_PID/oom_score_adj 2>/dev/null
# 2. Limit her to ONLY ONE CPU CORE (Prevents the 'Trip')
# This ensures she can never spike high enough to kill the audio server
taskset -pc 0 $TERMUX_PID 2>/dev/null
echo "[SUCCESS] Aethel is now CPU-Limited. She can't trip the music anymore."
