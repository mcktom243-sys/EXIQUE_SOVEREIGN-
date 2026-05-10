#!/bin/bash
# Scrape a major security news source (example: BleepingComputer or similar)
bash ~/AETHEL_VAULT/ingest_knowledge.sh "https://www.bleepingcomputer.com/feed/"
echo "[SEC_INTEL] Latest threats ingested on $(date)" >> ~/AETHEL_VAULT/fusion_bridge.log
