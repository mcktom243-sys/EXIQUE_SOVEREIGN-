# EXIQUE SOVEREIGN v2.0 - Installation & Setup Guide

## What's New in v2.0

✨ **Major Features:**
- 🎵 **AI Song Generator** - Create lyrics from stories with full emotion/genre/tempo control
- 🧠 **Advanced Learning System** - Learns emotions, genres, preferences from your songs
- 🌐 **Beautiful Web Dashboard** - Modern interface to generate and manage songs
- 💾 **Enhanced Memory** - All conversations and songs saved with learning context
- 🔄 **Dual Mode** - Run as Terminal OR Web Interface OR Both simultaneously
- ⚙️ **Menu System** - Easy launcher with options

## Prerequisites

Make sure you have:
- Termux (or Linux/macOS)
- Python 3.7+
- Ollama running (`ollama serve`)
- Mistral model downloaded (`ollama pull mistral`)

## Installation

### 1. Update Repository

```bash
cd ~/EXIQUE_SOVEREIGN-
git pull origin main
```

### 2. Install New Dependencies

```bash
pip install flask flask-cors --prefer-binary
```

That's it! You already have everything else from the initial setup.

## Usage

### Terminal Mode (Original - Still Works!)

```bash
# Run original terminal interface
python3 -m exique.main

# Or use the new launcher
python3 run_exique.py
# Then select option 2 from menu
```

### Web Interface (New!)

```bash
# Start the web server with dashboard
python3 run_exique.py
# Select option 1 from menu
# Open browser: http://localhost:5000
```

### Both Simultaneously

```bash
python3 run_exique.py
# Select option 3 from menu
# Both web (http://localhost:5000) and terminal running
```

### Menu System

```bash
python3 run_exique.py

Options:
  1. Start Web Interface (Dashboard + Song Generator)
  2. Start Terminal Mode (Chat)
  3. Start Both (Web + Terminal)
  4. View Learning Stats
  5. Exit
```

## Quick Start Guide

### Generate Your First Song

1. **Start Web Interface:**
   ```bash
   python3 run_exique.py
   # Choose option 1
   ```

2. **Open Dashboard:**
   Navigate to `http://localhost:5000` in your browser

3. **Generate Song:**
   - Enter a story (e.g., "A journey through heartbreak and recovery")
   - Select emotions (e.g., Sad + Hopeful)
   - Choose genre (e.g., Pop)
   - Set tempo (e.g., 100 BPM for slow, 140 for upbeat)
   - Click "Generate Song"

4. **Rate & Save:**
   - Rate the song (1-5 stars)
   - Copy or download lyrics
   - EXIQUE learns from your feedback!

### Use Chat

In the Dashboard:
1. Go to "Memory & Chat" tab
2. Type messages to chat with EXIQUE
3. All conversations saved with context
4. EXIQUE remembers everything!

### View Learning

In the Dashboard:
1. Go to "Learning Stats" tab
2. See:
   - Total songs generated
   - Average rating
   - Most used genres
   - Most common emotions
   - EXIQUE's preferences learned from you

## File Structure

New files added in v2.0:

```
EXIQUE_SOVEREIGN-/
├── run_exique.py                 # Main launcher with menu
├── exique/
│   ├── enhanced_memory.py        # Advanced memory + learning
│   ├── song_generator.py         # Song generation engine
│   ├── web_interface.py          # Flask API
│   └── main.py                   # (Original terminal mode)
├── templates/
│   └── dashboard.html            # Beautiful web UI
└── (all original files preserved)
```

## Features Explained

### Song Generator

**Input:**
- Story/Theme (what the song is about)
- Emotions (multiple selections allowed)
- Genre (8 genres supported)
- Tempo (40-200 BPM)

**Output:**
- Complete song lyrics with structure (Verse, Chorus, Bridge)
- Formatted for readability
- Estimated song length
- Shareable/downloadable

**Learning:**
- Tracks which emotions + genres work best
- Learns from your ratings
- Improves recommendations over time

### Memory System

**Stores:**
- All conversations
- All generated songs
- Emotional patterns
- Genre preferences
- User feedback

**Recall:**
- Search by subject
- View conversation history
- Access previous songs
- See learning patterns

### Web Dashboard Features

- 🎵 **Song Generator Tab** - Create songs with visual controls
- 📚 **Song History Tab** - View all generated songs with ratings
- 🧠 **Learning Stats** - See what EXIQUE has learned
- 💾 **Memory & Chat** - Chat interface + subject browser

## API Endpoints

If you want to integrate with other apps:

```
GET  /api/status              - System status
POST /api/generate-song       - Generate song
GET  /api/songs              - Get recent songs
GET  /api/song/<id>          - Get specific song
POST /api/song/<id>/rate     - Rate song
POST /api/song/<id>/feedback - Send feedback
GET  /api/learning/stats     - Get learning stats
GET  /api/learning/emotions  - Get emotion patterns
GET  /api/learning/genres    - Get genre preferences
GET  /api/memory/subjects    - Get memory subjects
GET  /api/memory/recall/<s>  - Recall subject
POST /api/chat              - Chat with EXIQUE
```

## Troubleshooting

### "Ollama not available"
Make sure Ollama is running:
```bash
ollama serve
# In another terminal
```

### "Web page won't load"
Check the server is running:
```bash
curl http://localhost:5000
```

### "Port 5000 already in use"
Use a different port in code or stop other processes

### Songs not being saved
Check memory database exists:
```bash
ls -la ~/.exique/
# Should have memory.db
```

## Next Steps

1. **Generate some songs** - Experiment with different stories/emotions/genres
2. **Rate songs** - Help EXIQUE learn what you like
3. **Chat** - Store knowledge in memory
4. **Check Learning** - See what EXIQUE has learned about you
5. **Share feedback** - Send feedback for even better learning

## Tips for Best Results

- **Specific stories** = Better lyrics (vs vague descriptions)
- **Multiple emotions** = More complex, interesting songs
- **Rate honestly** = Better learning for future generations
- **Varied genres** = More versatile AI
- **Chat before generating** = Context helps song generation

## Performance

- First generation: ~10-30 seconds (depends on Ollama + story length)
- Subsequent: ~5-20 seconds (GPU caching helps)
- Web dashboard: Lightweight, responsive
- Memory: Unlimited context, stores everything

## FAQ

**Q: Will my songs be saved?**
A: Yes! Everything saved to `~/.exique/memory.db`

**Q: Can I export songs?**
A: Yes! Use "Download" button or API

**Q: Does EXIQUE actually learn?**
A: Yes! From ratings, feedback, and your preferences

**Q: Can I use different LLMs?**
A: Currently Mistral. Easy to add others!

**Q: Is there a mobile version?**
A: Web interface works on mobile browsers!

## Support

For issues, check:
1. Ollama is running (`ollama serve`)
2. Mistral model downloaded (`ollama pull mistral`)
3. Python dependencies installed
4. Database has read/write permissions

---

**Enjoy EXIQUE SOVEREIGN v2.0!** 🚀

Questions? Start terminal and type `/help`
