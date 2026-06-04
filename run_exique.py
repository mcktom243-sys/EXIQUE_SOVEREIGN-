#!/usr/bin/env python3
"""
EXIQUE SOVEREIGN v2.0 - Main Launcher
Starts Ollama integration + Web Interface + Terminal Mode
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from exique.enhanced_memory import EnhancedMemoryManager
from exique.song_generator import SongGenerator
from exique.web_interface import app, init_web
from exique.main import ExiqueTerminalUI, OllamaClient, check_termux

import asyncio
import threading
from colorama import Fore, Style, init as colorama_init
import time

colorama_init(autoreset=True)


class ExiqueV2:
    """Main EXIQUE v2.0 Engine with Terminal + Web"""
    
    def __init__(self):
        self.memory = EnhancedMemoryManager()
        self.ollama = OllamaClient()
        self.song_gen = SongGenerator(self.ollama)
        self.ui = None
        self.web_thread = None
        
        print(f"{Fore.CYAN}═══════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║          EXIQUE SOVEREIGN v2.0 - Initialization          ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        self.init_components()
    
    def init_components(self):
        """Initialize all components"""
        print(f"{Fore.YELLOW}Initializing components...{Style.RESET_ALL}\n")
        
        # Check Ollama
        print(f"[1/3] Checking Ollama connection...", end=" ")
        if self.ollama.connected:
            print(f"{Fore.GREEN}✓{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}⚠ Warning: Ollama not connected. Start with: ollama serve{Style.RESET_ALL}")
        
        # Initialize memory
        print(f"[2/3] Initializing memory system...", end=" ")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL}")
        print(f"      Database: {self.memory.db_path}")
        
        # Initialize song generator
        print(f"[3/3] Initializing song generator...", end=" ")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL}")
        print(f"      Genres: 8 | Emotions: 8 | Learning: Enabled")
        
        print(f"\n{Fore.GREEN}All components initialized!{Style.RESET_ALL}\n")
    
    def start_web_server(self, host='localhost', port=5000):
        """Start Flask web server in background thread"""
        print(f"{Fore.CYAN}Starting web server...{Style.RESET_ALL}")
        
        # Initialize web interface with references
        init_web(self, self.ollama, self.memory, self.song_gen)
        
        def run_server():
            try:
                app.run(host=host, port=port, debug=False, use_reloader=False, threaded=True)
            except Exception as e:
                print(f"{Fore.RED}Web server error: {e}{Style.RESET_ALL}")
        
        self.web_thread = threading.Thread(target=run_server, daemon=True)
        self.web_thread.start()
        
        time.sleep(1)  # Give server time to start
        
        print(f"{Fore.GREEN}✓ Web server running{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Dashboard: http://localhost:{port}{Style.RESET_ALL}\n")
    
    async def generate_response(self, user_input: str) -> str:
        """Generate AI response (for web and terminal)"""
        if not self.ollama.connected:
            return "Ollama server not running. Start it with 'ollama serve' in another terminal."
        
        # Get context from memory
        context = self._get_context_for_response(user_input)
        
        # Build prompt
        prompt = f"""{context}

Current Request:
{user_input}

Respond thoughtfully, referencing previous conversations when relevant.
Keep responses concise but informative."""
        
        response = await asyncio.to_thread(self.ollama.generate, prompt)
        return response
    
    def _get_context_for_response(self, user_input: str, max_tokens: int = 8000) -> str:
        """Build context from memory"""
        subject = self.memory.extract_subject(user_input)
        related = self.memory.recall_subject(subject, limit=5)
        
        context = "=== RELEVANT MEMORY ==="
        token_count = 0
        
        for memory_item in related:
            entry = f"\n[{memory_item['timestamp']}]\nYou: {memory_item['user']}\nExique: {memory_item['ai'][:200]}...\n"
            entry_tokens = len(entry.split())
            
            if token_count + entry_tokens < max_tokens:
                context += entry
                token_count += entry_tokens
            else:
                break
        
        return context if len(related) > 0 else ""
    
    def show_menu(self):
        """Show main menu"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║               EXIQUE SOVEREIGN v2.0 - Main Menu                 ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Options:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}1{Style.RESET_ALL}. Start Web Interface (Dashboard + Song Generator)")
        print(f"  {Fore.GREEN}2{Style.RESET_ALL}. Start Terminal Mode (Chat)")
        print(f"  {Fore.GREEN}3{Style.RESET_ALL}. Start Both (Web + Terminal)")
        print(f"  {Fore.GREEN}4{Style.RESET_ALL}. View Learning Stats")
        print(f"  {Fore.GREEN}5{Style.RESET_ALL}. Exit\n")
    
    def display_stats(self):
        """Show learning statistics"""
        stats = self.memory.get_learning_stats()
        
        print(f"\n{Fore.CYAN}═══ LEARNING STATISTICS ═══{Style.RESET_ALL}")
        print(f"Total Songs Generated: {stats['total_songs']}")
        print(f"Average Rating: {stats['avg_rating']}/5.0")
        
        if stats['top_genres']:
            print(f"\nTop Genres:")
            for genre in stats['top_genres'][:3]:
                print(f"  • {genre['genre']}: {genre['times']} times")
        
        if stats['top_emotions']:
            print(f"\nTop Emotions:")
            for emotion in stats['top_emotions'][:3]:
                print(f"  • {emotion['emotion']}: {emotion['frequency']} times")
        
        print()
    
    async def run_terminal_mode(self):
        """Run terminal chat mode"""
        print(f"\n{Fore.CYAN}Terminal Mode Active{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Type 'exit' to quit, '/help' for commands\n{Style.RESET_ALL}")
        
        try:
            while True:
                try:
                    user_input = input(f"{Fore.YELLOW}You:{Style.RESET_ALL} ").strip()
                    
                    if not user_input:
                        continue
                    
                    if user_input.lower() == 'exit':
                        break
                    
                    if user_input.startswith('/'):
                        self._handle_terminal_command(user_input)
                        continue
                    
                    print(f"{Fore.CYAN}Exique: ", end="", flush=True)
                    response = await self.generate_response(user_input)
                    self.memory.store_conversation(user_input, response)
                    print(f"{response}{Style.RESET_ALL}\n")
                    
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}(Press Ctrl+C again to exit){Style.RESET_ALL}")
                    continue
        
        except KeyboardInterrupt:
            pass
    
    def _handle_terminal_command(self, command: str):
        """Handle terminal commands"""
        cmd = command.lower().strip()
        
        if cmd == '/help':
            print(f"""
{Fore.CYAN}COMMANDS:{Style.RESET_ALL}
/help           - Show this menu
/status         - Show connection status
/stats          - Show learning statistics
/memory         - List memory subjects
/recall [sub]   - Recall about subject
/exit           - Exit terminal mode
            """)
        elif cmd == '/status':
            print(f"\n{Fore.GREEN}✓ Ollama: Connected{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✓ Memory: Active{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✓ Song Generator: Ready{Style.RESET_ALL}\n")
        elif cmd == '/stats':
            self.display_stats()
        elif cmd == '/memory':
            subjects = self.memory.get_all_subjects()
            if subjects:
                print(f"\n{Fore.CYAN}Memory Subjects:{Style.RESET_ALL}")
                for i, subject in enumerate(subjects[:10], 1):
                    print(f"  {i}. {subject}")
                print()
            else:
                print(f"{Fore.YELLOW}No subjects in memory yet.{Style.RESET_ALL}\n")
        elif cmd.startswith('/recall'):
            subject = cmd.replace('/recall', '').strip()
            if subject:
                memories = self.memory.recall_subject(subject, limit=5)
                if memories:
                    print(f"\n{Fore.CYAN}Recalling about '{subject}':{Style.RESET_ALL}")
                    for mem in memories[:3]:
                        print(f"  {mem['timestamp']}: {mem['user'][:50]}...")
                    print()
                else:
                    print(f"{Fore.YELLOW}No memories about '{subject}'{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.YELLOW}Usage: /recall [subject]{Style.RESET_ALL}\n")
    
    def run(self):
        """Main run loop"""
        if not check_termux():
            print(f"{Fore.YELLOW}Note: Not running in Termux (testing mode){Style.RESET_ALL}\n")
        
        while True:
            self.show_menu()
            
            try:
                choice = input(f"{Fore.YELLOW}Choose (1-5):{Style.RESET_ALL} ").strip()
                
                if choice == '1':
                    self.start_web_server()
                    print(f"{Fore.CYAN}Web server running. Press Ctrl+C to stop.{Style.RESET_ALL}")
                    try:
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print(f"\n{Fore.YELLOW}Stopping web server...{Style.RESET_ALL}")
                
                elif choice == '2':
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        loop.run_until_complete(self.run_terminal_mode())
                    finally:
                        loop.close()
                
                elif choice == '3':
                    self.start_web_server()
                    print(f"{Fore.CYAN}Web server running.{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}Starting terminal mode...{Style.RESET_ALL}\n")
                    
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        loop.run_until_complete(self.run_terminal_mode())
                    finally:
                        loop.close()
                
                elif choice == '4':
                    self.display_stats()
                
                elif choice == '5':
                    print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                    break
                
                else:
                    print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")
            
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


def main():
    """Entry point"""
    try:
        engine = ExiqueV2()
        engine.run()
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
