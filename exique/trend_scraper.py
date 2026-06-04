#!/usr/bin/env python3
"""
Trend Scraper - Get free trending topics and hashtags
Uses DuckDuckGo and Reddit for free trend data (no API key needed)
"""

import requests
from typing import List, Dict, Any
from datetime import datetime
from bs4 import BeautifulSoup

class TrendScraper:
    """Scrape trending topics from free sources"""
    
    def __init__(self):
        self.trends_cache = {}
        self.cache_time = 3600  # 1 hour cache
    
    def get_twitter_trends(self) -> List[str]:
        """Get trending topics (simulated - using DuckDuckGo)"""
        try:
            # Search for trending on DuckDuckGo
            url = "https://duckduckgo.com/?q=trending+now&t=h"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # For now, return mock trending topics
            # In production, you'd scrape trending.com or similar
            return [
                "#AI",
                "#Technology", 
                "#Crypto",
                "#Python",
                "#StartupLife",
                "#Innovation",
                "#OpenSource",
                "#Coding"
            ]
        except Exception as e:
            print(f"Error fetching trends: {e}")
            return []
    
    def get_reddit_trends(self) -> List[Dict[str, Any]]:
        """Get trending Reddit posts"""
        try:
            # Get trending subreddits
            url = "https://www.reddit.com/r/all/hot.json"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                posts = []
                
                for post in data['data']['children'][:10]:
                    post_data = post['data']
                    posts.append({
                        'title': post_data['title'],
                        'subreddit': post_data['subreddit'],
                        'score': post_data['score'],
                        'url': f"https://reddit.com{post_data['permalink']}"
                    })
                
                return posts
            
            return []
        
        except Exception as e:
            print(f"Error fetching Reddit trends: {e}")
            return []
    
    def generate_trend_prompt(self, platform: str = "twitter") -> str:
        """Generate AI prompt with trending context"""
        
        if platform == "twitter":
            trends = self.get_twitter_trends()
            trend_str = ", ".join(trends[:5])
            prompt = f"""You are a social media expert. Here are current trending topics: {trend_str}

Generate an engaging, creative post that:
- References or relates to these trends
- Is authentic and not spammy
- Has personality and voice
- Encourages engagement
- Uses relevant hashtags

Write ONLY the post content, nothing else."""
        
        elif platform == "reddit":
            trends = self.get_reddit_trends()
            trend_str = "\n".join([f"- {p['title']} (r/{p['subreddit']})" for p in trends[:3]])
            prompt = f"""You are a Reddit expert. Here's what's trending now:

{trend_str}

Generate a thoughtful comment or post that:
- Adds value to the conversation
- Is genuine and helpful
- Fits the subreddit culture
- Doesn't come across as promotional

Write ONLY the content, nothing else."""
        
        else:
            prompt = """Generate an engaging, trending social media post that's:
- Current and relevant
- Authentic and fun
- Likely to spark engagement
- Original and creative"""
        
        return prompt
    
    def get_current_events(self) -> List[str]:
        """Get current events/memes from Reddit"""
        try:
            # Check r/news and r/worldnews for current events
            events = []
            
            for subreddit in ['news', 'worldnews', 'technology']:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    for post in data['data']['children'][:3]:
                        events.append(post['data']['title'])
            
            return events[:5]
        
        except Exception as e:
            print(f"Error fetching events: {e}")
            return []
    
    def is_trending(self, topic: str) -> bool:
        """Check if a topic is currently trending"""
        trends = self.get_twitter_trends()
        return any(trend.lower() in topic.lower() for trend in trends)
