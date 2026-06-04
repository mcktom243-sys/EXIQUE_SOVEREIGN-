#!/usr/bin/env python3
"""
EXIQUE SOVEREIGN - Full-Stack AI Agent
Terminal Interface with Memory Management & Unlimited Context Handling
Optimized for Termux & Local Execution
"""

import os
import sys
import json
import sqlite3
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import asyncio
from collections import deque
import hashlib

# CLI & UI
from colorama import Fore, Back, Style, init
import time

# Initialize colorama
init(autoreset=True)

class MemoryManager:
    """Persistent memory system with subject-based recall"""
    
    def __init__(self, db_path: str = "~/.exique/memory.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
        self.subject_cache = {}
        self.conversation_buffer = deque(maxlen=None)  # Unlimited buffer
        
    def init_db(self):
        """Initialize SQLite database for memory storage"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        # Conversations table
        c.execute('''CREATE TABLE IF NOT EXISTS conversations
                     (id INTEGER PRIMARY KEY,
                      timestamp TEXT,
                      subject TEXT,
                      user_input TEXT,
                      ai_response TEXT,
                      subject_hash TEXT)''')
        
        # Subject index table
        c.execute('''CREATE TABLE IF NOT EXISTS subject_index
                     (id INTEGER PRIMARY KEY,
                      subject TEXT UNIQUE,
                      last_mentioned TEXT,
                      frequency INTEGER,
                      summary TEXT)''')
        
        # Memory notes table
        c.execute('''CREATE TABLE IF NOT EXISTS memory_notes
                     (id INTEGER PRIMARY KEY,
                      timestamp TEXT,
                      note TEXT,
                      subject TEXT,
                      importance INTEGER)''')
        
        conn.commit()
        conn.close()
    
    def extract_subject(self, text: str) -> str:
        """Extract main subject from text"""
        words = text.lower().split()
        keywords = ["about", "help", "explain", "how", "what", "where", "when"]
        
        for i, word in enumerate(words):
            if word in keywords and i + 1 < len(words):
                subject = " ".join(words[i+1:i+4])
                return subject
        
        return " ".join(words[:3])
    
    def store_conversation(self, user_input: str, ai_response: str):
        """Store conversation with subject tagging"""
        subject = self.extract_subject(user_input)
        subject_hash = hashlib.md5(subject.encode()).hexdigest()
        
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        
        # Store conversation
        c.execute('''INSERT INTO conversations 
                     (timestamp, subject, user_input, ai_response, subject_hash)
                     VALUES (?, ?, ?, ?, ?)''',
                  (timestamp, subject, user_input, ai_response, subject_hash))
        
        # Update subject index
        c.execute('''INSERT OR IGNORE INTO subject_index 
                     (subject, last_mentioned, frequency)
                     VALUES (?, ?, 1)''',
                  (subject, timestamp))
        
        c.execute('''UPDATE subject_index 
                     SET last_mentioned = ?, frequency = frequency + 1
                     WHERE subject = ?''',
                  (timestamp, subject))
        
        conn.commit()
        conn.close()
        
        self.conversation_buffer.append({
            'user': user_input,
            'ai': ai_response,
            'subject': subject,
            'timestamp': timestamp
        })
    
    def recall_subject(self, subject: str, limit: int = 10) -> List[Dict]:
        """Recall all conversations about a specific subject"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        c.execute('''SELECT timestamp, user_input, ai_response 
                     FROM conversations 
                     WHERE subject LIKE ? 
                     ORDER BY timestamp DESC 
                     LIMIT ?''',
                  (f'%{subject}%', limit))
        
        results = []
        for row in c.fetchall():
            results.append({
                'timestamp': row[0],
                'user': row[1],
                'ai': row[2]
            })
        
        conn.close()
        return results
    
    def get_context_for_response(self, user_input: str, max_tokens: int = 8000) -> str:
        """Build context string from relevant memories"""
        subject = self.extract_subject(user_input)
        related = self.recall_subject(subject, limit=5)
        
        context = "=== RELEVANT MEMORY ==="
        token_count = 0
        
        for memory in related:
            entry = f"\n[{memory['timestamp']}]\nYou: {memory['user']}\nExique: {memory['ai'][:200]}...\n"
            entry_tokens = len(entry.split())
            
            if token_count + entry_tokens < max_tokens:
                context += entry
                token_count += entry_tokens
            else:
                break
        
        return context if len(related) > 0 else ""
    
    def get_all_subjects(self) -> List[str]:
        """Get list of all discussed subjects"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        c.execute('''SELECT subject FROM subject_index 
                     ORDER BY frequency DESC''')
        
        subjects = [row[0] for row in c.fetchall()]
        conn.close()
        return subjects


class OllamaClient:
    """Direct Ollama API client"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "mistral"
        self.connected = False
        self.check_connection()
    
    def check_connection(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.head(f"{self.base_url}/", timeout=2)
            self.connected = response.status_code == 200
            return self.connected
        except:
            self.connected = False
            return False
    
    def generate(self, prompt: str) -> str:
        """Generate response from Ollama"""
        if not self.connected:
            return "Ollama server not available. Make sure 'ollama serve' is running."
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7,
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response generated")
            else:
                return f"Error: {response.status_code} - {response.text}"
        except requests.exceptions.Timeout:
            return "Request timed out. Model may be processing large input."
        except Exception as e:
            return f"Error: {str(e)}"


class ExiqueTerminalUI:
    """Terminal UI for EXIQUE Sovereign with unlimited context"""
    
    def __init__(self):
        self.memory = MemoryManager()
        self.ollama = None
        self.session_start = datetime.now()
        self.message_count = 0
        self.init_ai_model()
        
    def init_ai_model(self):
        """Initialize Ollama client"""
        self.ollama = OllamaClient()
        if self.ollama.connected:
            print(f"{Fore.GREEN}✓ AI Model initialized (Mistral via Ollama){Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ Ollama not available{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Make sure to run 'ollama serve' in another terminal{Style.RESET_ALL}")
    
    def display_banner(self):
        """Display welcome banner"""
        banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗
║                  EXIQUE SOVEREIGN v1.0                      ║
║          Full-Stack AI Agent with Persistent Memory         ║
║                  Optimized for Termux                       ║
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}✓ Terminal Interface Active{Style.RESET_ALL}
{Fore.GREEN}✓ Unlimited Context Memory Enabled{Style.RESET_ALL}
{Fore.GREEN}✓ Subject-Based Memory Recall Active{Style.RESET_ALL}

{Fore.YELLOW}Commands:{Style.RESET_ALL}
  /help          - Show help menu
  /memory        - View memory subjects
  /recall [sub]  - Recall conversations about subject
  /status        - Show session status
  /clear         - Clear session (memory persists)
  /exit          - Exit application
  /save [name]   - Save conversation to file

{Fore.CYAN}Type your message and press Enter to chat...{Style.RESET_ALL}
"""
        print(banner)
    
    def display_status(self):
        """Show current session status"""
        uptime = datetime.now() - self.session_start
        subjects = self.memory.get_all_subjects()
        
        print(f"\n{Fore.CYAN}═══ SESSION STATUS ═══{Style.RESET_ALL}")
        print(f"Messages: {self.message_count}")
        print(f"Session Time: {uptime}")
        print(f"Memory DB: {self.memory.db_path}")
        print(f"Subjects Discussed: {len(subjects)}")
        print(f"Memory Buffer Size: {len(self.memory.conversation_buffer)}")
        print(f"Ollama Connected: {self.ollama.connected}")
        if subjects:
            print(f"Recent Topics: {', '.join(subjects[:5])}")
        print()
    
    def display_memory(self):
        """Display all subjects in memory"""
        subjects = self.memory.get_all_subjects()
        if not subjects:
            print(f"{Fore.YELLOW}No subjects in memory yet.{Style.RESET_ALL}\n")
            return
        
        print(f"\n{Fore.CYAN}═══ MEMORY SUBJECTS ═══{Style.RESET_ALL}")
        for i, subject in enumerate(subjects, 1):
            print(f"{i}. {subject}")
        print()
    
    def recall_memories(self, subject: str):
        """Recall and display memories about a subject"""
        memories = self.memory.recall_subject(subject)
        if not memories:
            print(f"{Fore.YELLOW}No memories found about '{subject}'{Style.RESET_ALL}\n")
            return
        
        print(f"\n{Fore.CYAN}═══ RECALL: {subject.upper()} ═══{Style.RESET_ALL}")
        for i, mem in enumerate(memories, 1):
            print(f"\n{Fore.GREEN}[{mem['timestamp']}]{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}You:{Style.RESET_ALL} {mem['user']}")
            print(f"{Fore.CYAN}Exique:{Style.RESET_ALL} {mem['ai'][:300]}...")
        print()
    
    async def generate_response(self, user_input: str) -> str:
        """Generate AI response with memory context"""
        if not self.ollama.connected:
            return "Ollama server not running. Start it with 'ollama serve' in another terminal."
        
        # Get context from memory
        context = self.memory.get_context_for_response(user_input)
        
        # Build prompt with context
        prompt = f"""{context}

Current Request:
{user_input}

Respond thoughtfully, referencing previous conversations when relevant.
Keep responses concise but informative."""
        
        # Run in thread to avoid blocking
        response = await asyncio.to_thread(self.ollama.generate, prompt)
        return response
    
    def handle_command(self, command: str):
        """Handle special commands"""
        cmd = command.lower().strip()
        
        if cmd == "/help":
            print(f"""
{Fore.CYAN}AVAILABLE COMMANDS:{Style.RESET_ALL}
/help           - Show this help menu
/memory         - List all subjects in memory
/recall [sub]   - Recall conversations about subject
/status         - Show session statistics
/clear          - Clear terminal
/exit           - Exit application
/save [name]    - Save current session
""")
        elif cmd == "/memory":
            self.display_memory()
        elif cmd.startswith("/recall"):
            subject = cmd.replace("/recall", "").strip()
            if subject:
                self.recall_memories(subject)
            else:
                print(f"{Fore.YELLOW}Usage: /recall [subject]{Style.RESET_ALL}")
        elif cmd == "/status":
            self.display_status()
        elif cmd == "/clear":
            os.system("clear" if os.name != "nt" else "cls")
        elif cmd.startswith("/save"):
            name = cmd.replace("/save", "").strip() or "exique_session"
            self.save_session(name)
        else:
            print(f"{Fore.RED}Unknown command. Type /help for commands.{Style.RESET_ALL}")
    
    def save_session(self, filename: str):
        """Save current session to file"""
        save_path = Path("~/.exique/sessions").expanduser()
        save_path.mkdir(parents=True, exist_ok=True)
        
        file_path = save_path / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        session_data = {
            'timestamp': datetime.now().isoformat(),
            'messages': list(self.memory.conversation_buffer),
            'subjects': self.memory.get_all_subjects()
        }
        
        with open(file_path, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"{Fore.GREEN}✓ Session saved to {file_path}{Style.RESET_ALL}")
    
    async def run(self):
        """Main terminal loop"""
        self.display_banner()
        
        try:
            while True:
                try:
                    user_input = input(f"{Fore.YELLOW}You:{Style.RESET_ALL} ").strip()
                    
                    if not user_input:
                        continue
                    
                    if user_input.startswith("/"):
                        self.handle_command(user_input)
                        continue
                    
                    if user_input.lower() == "exit":
                        print(f"{Fore.GREEN}✓ Exiting EXIQUE Sovereign...{Style.RESET_ALL}")
                        break
                    
                    # Show thinking animation
                    print(f"{Fore.CYAN}Exique: ", end="", flush=True)
                    
                    # Generate response
                    response = await self.generate_response(user_input)
                    
                    # Store in memory
                    self.memory.store_conversation(user_input, response)
                    self.message_count += 1
                    
                    # Display response
                    print(f"{response}{Style.RESET_ALL}\n")
                    
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}(Press Ctrl+C again to exit, or type 'exit'){Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        
        except KeyboardInterrupt:
            print(f"\n{Fore.GREEN}✓ Session ended gracefully{Style.RESET_ALL}")


def check_termux():
    """Check if running in Termux"""
    return os.path.exists("/data/data/com.termux")


def install_termux_startup():
    """Create startup script for Termux"""
    if not check_termux():
        return
    
    startup_dir = Path("~/.termux/boot").expanduser()
    startup_dir.mkdir(parents=True, exist_ok=True)
    
    script = startup_dir / "start_exique.sh"
    
    with open(script, 'w') as f:
        f.write(f"""#!/bin/bash
# Start EXIQUE Sovereign on Termux boot

cd "$HOME"
python3 -m exique.main
""")
    
    os.chmod(script, 0o755)
    print(f"{Fore.GREEN}✓ Termux startup script installed{Style.RESET_ALL}")


def main():
    """Main entry point"""
    if check_termux():
        print(f"{Fore.CYAN}Running in Termux environment{Style.RESET_ALL}")
    
    ui = ExiqueTerminalUI()
    
    # Run async event loop
    asyncio.run(ui.run())


if __name__ == "__main__":
    main()
