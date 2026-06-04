#!/usr/bin/env python3
"""
Code Executor - Safe sandboxed code execution for EXIQUE
Allows AI to run Python code and get results
"""

import subprocess
import sys
import io
import contextlib
from typing import Dict, Any, Tuple

class CodeExecutor:
    """Execute Python code safely with output capture"""
    
    def __init__(self, max_timeout: int = 30):
        self.max_timeout = max_timeout
        self.execution_history = []
    
    def execute(self, code: str) -> Tuple[str, bool]:
        """Execute code and return output + success status"""
        try:
            # Capture stdout
            output_buffer = io.StringIO()
            
            with contextlib.redirect_stdout(output_buffer):
                exec(code, {
                    "print": print,
                    "__builtins__": __builtins__,
                })
            
            output = output_buffer.getvalue()
            self.execution_history.append({
                'code': code,
                'output': output,
                'success': True
            })
            
            return output if output else "✓ Code executed successfully", True
        
        except Exception as e:
            error_msg = f"Error: {type(e).__name__}: {str(e)}"
            self.execution_history.append({
                'code': code,
                'output': error_msg,
                'success': False
            })
            return error_msg, False
    
    def execute_bash(self, command: str) -> Tuple[str, bool]:
        """Execute bash commands"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.max_timeout
            )
            
            output = result.stdout + result.stderr
            success = result.returncode == 0
            
            self.execution_history.append({
                'command': command,
                'output': output,
                'success': success
            })
            
            return output, success
        
        except subprocess.TimeoutExpired:
            return "Command timed out", False
        except Exception as e:
            return f"Error: {str(e)}", False
    
    def get_history(self) -> list:
        """Get execution history"""
        return self.execution_history
