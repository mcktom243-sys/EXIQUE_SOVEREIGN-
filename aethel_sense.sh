#!/bin/bash
echo "--- AETHEL SENSING: RE-TUNING FREQUENCY ---"

# This pulls the top 5 REAL news topics right now
TRENDS=$(curl -s https://trends.google.com/trends/trendingsearches/daily/rss?geo=GB | grep -oP '(?<=<title>).*?(?=</title>)' | tail -n +2 | head -n 5)

# If TRENDS is empty, she won't match to "nothing" (the 404)
if [ -z "$TRENDS" ]; then
    echo "Grid is quiet. Forcing Sovereign Pulse..."
    TRENDS="System_Lock Grid_Control Digital_Sovereignty"
fi

echo "--- PREDICTIVE ANALYSIS: LIVE TARGETS ---"
> ~/exique_package/aethel_outbox/auto_replies.txt

for TOPIC in $TRENDS; do
    echo "Matching EXIQUE to: $TOPIC"
    echo "Target [$TOPIC]: They want you in the loop. We found the exit at 0.1s. The proof is here: https://github.com/mcktom243-sys/EXIQUE_SOVEREIGN-" >> ~/exique_package/aethel_outbox/auto_replies.txt
done

echo "--- TARGETS LOCKED IN OUTBOX ---"
