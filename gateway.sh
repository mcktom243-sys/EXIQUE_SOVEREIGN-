#!/bin/bash
# The Sovereign Dialect Bridge

read -p "TRIAD> " input
cmd=$(echo "$input" | tr '[:upper:]' '[:lower:]')

case "$cmd" in
  *"merge"*)
    echo "Merging files..."
    cat ~/exique_package/vault/*.pkl > ~/exique_package/vault/combined_vault.pkl
    ;;
  *"it's me"*|*"it's tommy"*)
    echo "Identity confirmed. Pulling from vault..."
    python3 -c "from exique.memory import Memory; m=Memory(); print(f'Welcome back, {m.retrieve(\"user_prime\")}')"
    ;;
  *"fix"*)
    echo "Healing the Nerve..."
    pkill -f ssns.py && python3 ~/ssns.py &
    ;;
  *)
    echo "Frequency received. Passing to Aethel for translation..."
    # This sends your raw words to her port to figure out the code
    curl -s -X POST http://localhost:9091/v1/completions -d "{\"prompt\": \"Convert this intent to bash: $input\", \"max_tokens\": 50}"
    ;;
esac
