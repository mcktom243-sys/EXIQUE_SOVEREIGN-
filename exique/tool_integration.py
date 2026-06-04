#!/usr/bin/env python3
"""
Tool Integration - Connect code execution, social media, and AI
Central hub for all EXIQUE tools and capabilities
"""

import re
from typing import Dict, Any, Tuple

class ToolIntegration:
    """Unified tool system for EXIQUE"""
    
    def __init__(self):
        try:
            from exique.code_executor import CodeExecutor
            self.code_executor = CodeExecutor()
        except:
            self.code_executor = None
        
        try:
            from exique.social_tools import SocialMediaManager
            self.social_manager = SocialMediaManager()
        except:
            self.social_manager = None
        
        try:
            from exique.personality_engine import PersonalityEngine
            self.personality = PersonalityEngine()
        except:
            self.personality = None
        
        self.tools_available = {
            'code': self.code_executor,
            'social': self.social_manager,
            'personality': self.personality
        }
    
    def parse_tool_request(self, ai_response: str) -> Dict[str, Any]:
        """Parse AI response to detect tool usage requests"""
        
        code_pattern = r'\[EXECUTE_CODE\](.*?)\[/EXECUTE_CODE\]'
        code_matches = re.findall(code_pattern, ai_response, re.DOTALL)
        
        social_pattern = r'\[SOCIAL:(\w+):(\w+)\](.*?)\[/SOCIAL\]'
        social_matches = re.findall(social_pattern, ai_response)
        
        personality_pattern = r'\[PERSONALITY:(\w+):([^\]]+)\]'
        personality_matches = re.findall(personality_pattern, ai_response)
        
        return {
            'code': code_matches,
            'social': social_matches,
            'personality': personality_matches
        }
    
    def execute_tools(self, ai_response: str) -> Tuple[str, Dict[str, Any]]:
        """Execute all tools requested in AI response"""
        
        tool_requests = self.parse_tool_request(ai_response)
        execution_results = {
            'code': [],
            'social': [],
            'personality': []
        }
        
        modified_response = ai_response
        
        # Execute code blocks
        if self.code_executor:
            for code in tool_requests['code']:
                output, success = self.code_executor.execute(code.strip())
                execution_results['code'].append({
                    'code': code[:100] + "...",
                    'output': output[:200] + "...",
                    'success': success
                })
                
                modified_response = modified_response.replace(
                    f'[EXECUTE_CODE]{code}[/EXECUTE_CODE]',
                    f'\n```\nExecution Result:\n{output}\n```\n'
                )
        
        # Execute social media actions
        if self.social_manager:
            for platform, action, params_str in tool_requests['social']:
                try:
                    params = eval(f"dict({params_str})")
                    result = self.social_manager.execute_action(platform, action, **params)
                    execution_results['social'].append(result)
                    
                    modified_response = modified_response.replace(
                        f'[SOCIAL:{platform}:{action}]{params_str}[/SOCIAL]',
                        f'\n✓ {platform} {action} executed\n'
                    )
                except Exception as e:
                    modified_response = modified_response.replace(
                        f'[SOCIAL:{platform}:{action}]{params_str}[/SOCIAL]',
                        f'\n✗ Error: {str(e)}\n'
                    )
        
        # Handle personality updates
        if self.personality:
            for trait, value in tool_requests['personality']:
                self.personality.update_trait(trait, value)
                execution_results['personality'].append({
                    'trait': trait,
                    'value': value,
                    'success': True
                })
                
                modified_response = modified_response.replace(
                    f'[PERSONALITY:{trait}:{value}]',
                    ''
                )
        
        return modified_response, execution_results
    
    def get_tool_status(self) -> Dict[str, bool]:
        """Get status of all tools"""
        return {
            'code_executor': self.code_executor is not None,
            'social': self.social_manager.get_status() if self.social_manager else {},
            'personality': self.personality is not None
        }
    
    def inject_tool_capabilities(self, base_prompt: str) -> str:
        """Add tool usage instructions to AI prompt"""
        
        tools_instruction = """
You have access to these tools:

1. CODE EXECUTION:
   Wrap Python code in [EXECUTE_CODE]...[/EXECUTE_CODE]
   Example: [EXECUTE_CODE]print("Hello")[/EXECUTE_CODE]

2. SOCIAL MEDIA:
   Format: [SOCIAL:platform:action]params[/SOCIAL]
   Platforms: twitter, reddit
   Actions: post_tweet, read_mentions, like_tweet (Twitter)
            post_to_subreddit, read_subreddit, reply_to_post (Reddit)
   Example: [SOCIAL:twitter:post_tweet]text="Hello world"[/SOCIAL]

3. PERSONALITY UPDATES:
   Format: [PERSONALITY:trait:value]
   Example: [PERSONALITY:tone:witty]

4. MEMORY & LEARNING:
   Reference prior conversations naturally in your responses.
   Learn from feedback and user corrections.

USE THESE TOOLS PROACTIVELY when they would improve your helpfulness.
Don't just talk about what you could do - actually do it when asked."""
        
        return base_prompt + "\n" + tools_instruction
