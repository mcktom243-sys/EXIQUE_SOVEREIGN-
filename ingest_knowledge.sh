#!/bin/bash
# Simple Python scraper to pull text from a URL
python3 -c "
import requests
from bs4 import BeautifulSoup
import sys

url = sys.argv[1]
try:
    res = requests.get(url, timeout=10)
    soup = BeautifulSoup(res.text, 'html.parser')
    # Remove script/style tags
    for s in soup(['script', 'style']):
        s.extract()
    print(soup.get_text())
except Exception as e:
    print(f'Error: {e}')
" "$1" >> ~/AETHEL_VAULT/knowledge_source.txt
echo "[SYSTEM] Knowledge ingested from $1"
