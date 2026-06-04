# EXIQUE SOVEREIGN - Full-Stack AI Agent
## Terminal Interface with Unlimited Context Memory

A sophisticated AI agent designed to run in Termux and local environments with persistent memory, unlimited context handling, and intelligent subject recall.

### Features

✨ **Core Capabilities**
- Terminal-based interface optimized for Termux
- Local execution with Ollama (Mistral model)
- Unlimited conversation context (never truncates)
- Persistent memory with SQLite
- Subject-based conversation recall
- Smart memory compression and archiving
- Async/await pattern for non-blocking operations
- Full command system for memory management

🧠 **Memory System**
- Auto-extracts subjects from conversations
- Stores all conversations with timestamps
- Recall conversations by topic
- Maintains conversation buffer (unlimited size)
- Long-term memory index for facts and decisions
- Context window manager prevents token overflow
- Memory compression for efficiency

🖥️ **Terminal Interface**
- Colorized output with progress indicators
- Session statistics and status tracking
- Command palette with 8+ commands
- Conversation saving to JSON
- Memory management tools
- Real-time token counting

📱 **Termux Integration**
- Automatic startup script installation
- Works seamlessly on Android with Termux
- Falls back gracefully on non-Termux systems
- Auto-boot support
- Terminal-native operation

### Installation

#### On Termux
```bash
git clone https://github.com/mcktom243-sys/EXIQUE_SOVEREIGN-.git
cd EXIQUE_SOVEREIGN-
bash install.sh
```

#### Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Download Mistral model
ollama pull mistral

# Run directly
python3 -m exique.main
```

### Quick Start

```bash
# Start EXIQUE
python3 -m exique.main

# Or use alias (if installed)
exique
```

### Commands

| Command | Description |
|---------|-------------|
| `/help` | Show help menu |
| `/memory` | List all subjects discussed |
| `/recall [subject]` | Recall conversations about a topic |
| `/status` | Show session statistics |
| `/clear` | Clear terminal |
| `/save [name]` | Save current session |
| `/exit` | Exit application |

### Architecture

```
exique/
├── main.py              # Terminal UI & Memory Manager
├── context_manager.py   # Context window & long-term memory
└── __init__.py         # Package initialization

install.sh              # Termux/Linux installation script
requirements.txt        # Python dependencies
README.md              # This file
```

### Memory Storage

- **Location**: `~/.exique/`
- **Database**: `memory.db` (SQLite)
- **Sessions**: `sessions/` (JSON backups)
- **Backups**: `backups/`

### How Unlimited Context Works

1. **Active Context**: Stores current conversation (limited to ~4000 tokens)
2. **Archive System**: Old messages moved to archive when limit exceeded
3. **Smart Recall**: Retrieves relevant archived messages by subject
4. **Context Window**: Never loses information, just reorganizes it
5. **Persistent Memory**: Everything saved to SQLite for cross-session recall

### Memory Recall Algorithm

When you ask about a previous topic:
1. Extracts subject keywords from your input
2. Searches SQLite for matching conversations
3. Retrieves up to 10 most recent matches
4. Includes relevant context in AI prompt
5. Maintains continuity across sessions

### Dependencies

**Core AI/LLM**
- ollama (local LLM engine)
- langchain (LLM orchestration)
- langchain-community

**Interface**
- colorama (terminal colors)
- sqlite3 (database)

**Additional**
- All packages in requirements.txt

### Configuration

Edit defaults in `exique/main.py`:
```python
class MemoryManager:
    def __init__(self, db_path: str = "~/.exique/memory.db"):
        # Change database location
        
class ExiqueTerminalUI:
    def init_ai_model(self):
        self.ai_model = Ollama(model="mistral")  # Change model
```

### Termux Setup Details

When you run `bash install.sh`:
1. Updates Termux packages
2. Installs Python 3, pip, git
3. Creates `~/.exique/` directories
4. Creates `~/.termux/boot/start_exique.sh` for auto-start
5. Installs Ollama if needed
6. Adds shell aliases

### Auto-Startup in Termux

After installation, EXIQUE will:
1. Start automatically on Termux boot
2. Load all previous memory
3. Restore conversation history
4. Be ready for new conversations

### Performance Notes

- **First Launch**: 2-3 seconds to initialize
- **Memory Queries**: <100ms for typical searches
- **AI Response**: Depends on Ollama model (usually 1-5 seconds)
- **Storage**: Minimal - SQLite db grows ~1MB per 1000 messages

### Troubleshooting

**Ollama Not Found**
```bash
curl https://ollama.ai/install.sh | sh
ollama pull mistral
```

**Permission Denied**
```bash
chmod +x exique/main.py install.sh
```

**Memory Database Errors**
```bash
rm ~/.exique/memory.db
# Fresh start on next run
```

**Termux Permissions**
```bash
# Grant storage access in Termux settings
termux-setup-storage
```

### Features Coming Soon

- [ ] Web interface
- [ ] Voice input/output
- [ ] Multi-model support
- [ ] Cloud sync option
- [ ] Advanced analytics dashboard
- [ ] Memory visualization
- [ ] Integration with external APIs

### License

MIT License - See LICENSE file

### Author

EXIQUE Sovereign AI Agent System
Developed for unlimited local AI capability

---

**Important**: This tool is designed for local use. Ensure Ollama is running before starting EXIQUE.