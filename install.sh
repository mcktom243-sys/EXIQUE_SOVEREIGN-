#!/usr/bin/env bash
# EXIQUE Sovereign - Termux Installation & Startup Script
# Run with: bash install.sh

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║       EXIQUE SOVEREIGN - Termux Installation              ║"
echo "╚═══════════════════════════════════════════════════════════╝"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo -e "${YELLOW}Warning: Not running in Termux${NC}"
    echo "This script is optimized for Termux but will work on any Linux system"
fi

echo -e "${CYAN}Step 1: Updating package manager...${NC}"
pkg update -y 2>/dev/null || sudo apt update -y
pkg upgrade -y 2>/dev/null || sudo apt upgrade -y

echo -e "${CYAN}Step 2: Installing system dependencies...${NC}"
pkg install -y python3 pip git sqlite3 build-essential 2>/dev/null || sudo apt install -y python3 pip git sqlite3 build-essential

echo -e "${CYAN}Step 3: Creating EXIQUE directories...${NC}"
mkdir -p ~/.exique/memory
mkdir -p ~/.exique/sessions
mkdir -p ~/.exique/backups

echo -e "${CYAN}Step 4: Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${CYAN}Step 5: Setting up Ollama...${NC}"
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}Ollama not found. Installing...${NC}"
    curl https://ollama.ai/install.sh | sh
    echo -e "${GREEN}✓ Ollama installed${NC}"
    echo -e "${YELLOW}Run 'ollama pull mistral' to download the model${NC}"
else
    echo -e "${GREEN}✓ Ollama already installed${NC}"
fi

echo -e "${CYAN}Step 6: Setting up Termux startup script...${NC}"
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/start_exique.sh << 'EOF'
#!/bin/bash
# Start EXIQUE Sovereign on Termux boot
sleep 3
cd $HOME
python3 -m exique.main
EOF
chmod +x ~/.termux/boot/start_exique.sh
echo -e "${GREEN}✓ Startup script created${NC}"

echo -e "${CYAN}Step 7: Creating convenient aliases...${NC}"
cat >> ~/.bashrc << 'EOF'

# EXIQUE Sovereign Aliases
alias exique="python3 -m exique.main"
alias exique-memory="ls -la ~/.exique/memory/"
alias exique-sessions="ls -la ~/.exique/sessions/"
EOF

source ~/.bashrc

echo -e "${CYAN}Step 8: Making executable...${NC}"
chmod +x exique/main.py
chmod +x exique/context_manager.py

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗"
echo "║     EXIQUE SOVEREIGN Installation Complete!               ║"
echo "╚═══════════════════════════════════════════════════════════╝${NC}"

echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Download Mistral model: ollama pull mistral"
echo "2. Start EXIQUE: python3 -m exique.main"
echo "   (or just type 'exique' after restarting terminal)"
echo ""
echo -e "${CYAN}Memory location:${NC} ~/.exique/memory/"
echo -e "${CYAN}Sessions location:${NC} ~/.exique/sessions/"
echo ""
echo -e "${YELLOW}Features:${NC}"
echo "  • Unlimited context memory with no truncation"
echo "  • Subject-based conversation recall"
echo "  • Persistent memory across sessions"
echo "  • Auto-startup in Termux with /data/data/com.termux/boot"
echo "  • Full terminal interface with command system"
echo ""
echo -e "${CYAN}Type '/help' when running EXIQUE for available commands${NC}"