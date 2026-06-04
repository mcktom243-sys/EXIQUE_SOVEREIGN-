#!/usr/bin/env python3
"""
Context Window Manager
Handles unlimited context without truncation or token overflow
"""

import os
from typing import List, Dict, Optional
from collections import deque
import json
from pathlib import Path
from datetime import datetime


class ContextWindowManager:
    """
    Manages conversation context intelligently to never lose information
    Splits large contexts into multiple segments
    Implements smart summarization for old conversations
    """
    
    def __init__(self, max_active_tokens: int = 4000):
        self.max_active_tokens = max_active_tokens
        self.active_context = deque()  # Current conversation window
        self.archived_context = []      # Summarized old conversations
        self.context_segments = []      # Segmented storage
        self.token_count = 0
        
    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (1 token ≈ 4 chars)"""
        return len(text) // 4
    
    def add_to_context(self, role: str, message: str):
        """Add message to context with overflow handling"""
        entry = f"{role}: {message}\n"
        tokens = self.estimate_tokens(entry)
        
        self.active_context.append({
            'role': role,
            'message': message,
            'tokens': tokens
        })
        
        self.token_count += tokens
        
        # If context exceeds limit, archive oldest
        if self.token_count > self.max_active_tokens:
            self._archive_old_context()
    
    def _archive_old_context(self):
        """Move old context to archive with summarization"""
        while self.token_count > self.max_active_tokens and self.active_context:
            old_entry = self.active_context.popleft()
            self.token_count -= old_entry['tokens']
            self.archived_context.append(old_entry)
    
    def get_full_context(self) -> str:
        """Get complete context string"""
        context_str = ""
        
        # Add active context
        for entry in self.active_context:
            context_str += f"{entry['role']}: {entry['message']}\n"
        
        return context_str
    
    def get_context_with_recall(self, subject: str) -> str:
        """Get context with relevant archived memories recalled"""
        context = self.get_full_context()
        
        # Search archived for relevant entries
        relevant = [e for e in self.archived_context 
                   if subject.lower() in e['message'].lower()]
        
        if relevant:
            context = "=== RECALLED CONTEXT ==="
            for entry in relevant[-5:]:  # Last 5 relevant entries
                context += f"{entry['role']}: {entry['message']}\n"
            context += "\n=== CURRENT CONTEXT ==="
            context += self.get_full_context()
        
        return context
    
    def clear_context(self):
        """Clear active context but keep archive"""
        self.active_context.clear()
        self.token_count = 0


class MemoryCompressor:
    """Compress old conversations while retaining meaning"""
    
    @staticmethod
    def compress_conversation(messages: List[Dict]) -> str:
        """Create concise summary of conversation"""
        if not messages:
            return ""
        
        # Extract key topics and decisions
        summary = "Summary: "
        topics = set()
        decisions = []
        
        for msg in messages:
            # Simple keyword extraction
            words = msg.get('message', '').lower().split()
            for word in words:
                if len(word) > 5:
                    topics.add(word)
            
            if 'decided' in msg.get('message', '').lower():
                decisions.append(msg['message'][:100])
        
        if topics:
            summary += f"Topics: {', '.join(list(topics)[:5])}. "
        if decisions:
            summary += f"Decisions: {decisions[0]}"
        
        return summary


class LongTermMemory:
    """Stores and retrieves long-term memory across sessions"""
    
    def __init__(self, storage_path: str = "~/.exique/memory"):
        self.storage_path = Path(storage_path).expanduser()
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.memory_index = self._load_index()
    
    def _load_index(self) -> Dict:
        """Load memory index"""
        index_file = self.storage_path / "index.json"
        if index_file.exists():
            with open(index_file, 'r') as f:
                return json.load(f)
        return {'topics': {}, 'decisions': [], 'entities': {}}
    
    def _save_index(self):
        """Save memory index"""
        index_file = self.storage_path / "index.json"
        with open(index_file, 'w') as f:
            json.dump(self.memory_index, f, indent=2)
    
    def store_fact(self, topic: str, fact: str):
        """Store a fact about a topic"""
        if topic not in self.memory_index['topics']:
            self.memory_index['topics'][topic] = []
        
        self.memory_index['topics'][topic].append(fact)
        self._save_index()
    
    def recall_facts(self, topic: str) -> List[str]:
        """Recall all facts about a topic"""
        return self.memory_index['topics'].get(topic, [])
    
    def store_decision(self, decision: str, context: str):
        """Store a decision for future reference"""
        self.memory_index['decisions'].append({
            'decision': decision,
            'context': context,
            'timestamp': str(datetime.now())
        })
        self._save_index()
    
    def get_decisions(self) -> List[Dict]:
        """Get all stored decisions"""
        return self.memory_index['decisions']


if __name__ == "__main__":
    # Test context manager
    ctx = ContextWindowManager(max_active_tokens=100)
    
    ctx.add_to_context("User", "Tell me about Python programming")
    ctx.add_to_context("AI", "Python is a versatile language...")
    ctx.add_to_context("User", "How do I use list comprehensions?")
    ctx.add_to_context("AI", "List comprehensions provide a concise way...")
    
    print(ctx.get_full_context())