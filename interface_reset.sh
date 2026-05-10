#!/bin/bash
echo "Closing Jukebox. Restoring Sentinel logic..."
# Restart her server without the 'Jukebox' UI files
nice -n 19 python3 -m http.server 9090 --directory ~/AETHEL_VAULT/ &
