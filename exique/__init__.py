#!/usr/bin/env python3
"""
__init__.py - EXIQUE Sovereign Package
"""

__version__ = "1.0.0"
__author__ = "EXIQUE Sovereign"
__description__ = "Full-Stack AI Agent with Unlimited Memory & Context Management"

from exique.main import ExiqueTerminalUI, MemoryManager
from exique.context_manager import ContextWindowManager, LongTermMemory

__all__ = [
    'ExiqueTerminalUI',
    'MemoryManager',
    'ContextWindowManager',
    'LongTermMemory'
]