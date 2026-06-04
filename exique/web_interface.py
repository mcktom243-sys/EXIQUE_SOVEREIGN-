#!/usr/bin/env python3
"""
Web Interface - Local Flask dashboard for EXIQUE
Run on http://localhost:5000
No external APIs needed - fully local
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
from pathlib import Path
import json
import threading
import asyncio

app = Flask(__name__, template_folder='templates')
CORS(app)

# Global state
posts_pending_approval = []
memory_data = {}
ai_status = {"connected": False, "model": "mistral"}

class WebInterface:
    """Local web interface for EXIQUE"""
    
    def __init__(self, memory_manager=None, ollama_client=None, tool_integration=None):
        self.memory = memory_manager
        self.ollama = ollama_client
        self.tools = tool_integration
        self.pending_posts = []
        self.post_history = []
        self.load_history()
    
    def load_history(self):
        """Load post history from file"""
        history_file = Path("~/.exique/post_history.json").expanduser()
        if history_file.exists():
            with open(history_file, 'r') as f:
                self.post_history = json.load(f)
    
    def save_history(self):
        """Save post history"""
        history_file = Path("~/.exique/post_history.json").expanduser()
        history_file.parent.mkdir(parents=True, exist_ok=True)
        with open(history_file, 'w') as f:
            json.dump(self.post_history, f, indent=2)
    
    def add_pending_post(self, platform, content, post_id=None):
        """Add post to approval queue"""
        post = {
            'id': post_id or str(datetime.now().timestamp()),
            'platform': platform,
            'content': content,
            'created_at': datetime.now().isoformat(),
            'status': 'pending'
        }
        self.pending_posts.append(post)
        return post
    
    def approve_post(self, post_id):
        """Approve a post for publishing"""
        for post in self.pending_posts:
            if post['id'] == post_id:
                post['status'] = 'approved'
                post['approved_at'] = datetime.now().isoformat()
                self.post_history.append(post)
                self.save_history()
                self.pending_posts.remove(post)
                return True
        return False
    
    def reject_post(self, post_id):
        """Reject a post"""
        for post in self.pending_posts:
            if post['id'] == post_id:
                post['status'] = 'rejected'
                self.pending_posts.remove(post)
                return True
        return False

# Initialize web interface
web_interface = WebInterface()

# Routes

@app.route('/')
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/status')
def status():
    """Get EXIQUE status"""
    return jsonify({
        'ai_connected': ai_status['connected'],
        'model': ai_status['model'],
        'pending_posts': len(web_interface.pending_posts),
        'total_posted': len(web_interface.post_history),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/pending-posts')
def get_pending_posts():
    """Get posts awaiting approval"""
    return jsonify(web_interface.pending_posts)

@app.route('/api/post-history')
def get_post_history():
    """Get history of posted content"""
    return jsonify(web_interface.post_history[-50:])

@app.route('/api/approve', methods=['POST'])
def approve_post():
    """Approve a post"""
    data = request.json
    post_id = data.get('post_id')
    
    if web_interface.approve_post(post_id):
        return jsonify({'success': True, 'message': 'Post approved!'})
    return jsonify({'success': False, 'error': 'Post not found'}), 404

@app.route('/api/reject', methods=['POST'])
def reject_post():
    """Reject a post"""
    data = request.json
    post_id = data.get('post_id')
    
    if web_interface.reject_post(post_id):
        return jsonify({'success': True, 'message': 'Post rejected'})
    return jsonify({'success': False, 'error': 'Post not found'}), 404

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with EXIQUE"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    if not web_interface.ollama or not web_interface.ollama.connected:
        return jsonify({'error': 'AI not connected'}), 503
    
    response = web_interface.ollama.generate(user_message)
    
    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/generate-post', methods=['POST'])
def generate_post():
    """Generate social media post idea"""
    data = request.json
    topic = data.get('topic', '')
    platform = data.get('platform', 'twitter')
    use_trends = data.get('use_trends', True)
    
    if not topic:
        return jsonify({'error': 'Topic required'}), 400
    
    if not web_interface.ollama or not web_interface.ollama.connected:
        return jsonify({'error': 'AI not connected'}), 503
    
    # Get trending context if requested
    trend_prompt = ""
    if use_trends:
        try:
            from exique.trend_scraper import TrendScraper
            scraper = TrendScraper()
            trend_prompt = scraper.generate_trend_prompt(platform)
        except:
            pass
    
    # Create prompt for creative post
    if trend_prompt:
        prompt = trend_prompt + f"\n\nTopic/Theme: {topic}"
    else:
        prompt = f"""Generate a creative, engaging {platform} post about: {topic}
        
Keep it:
- Short and punchy
- On-trend and relevant
- Engaging and shareable
- Original voice, not corporate
- Free thinking and authentic

Just write the post content, nothing else."""
    
    response = web_interface.ollama.generate(prompt)
    
    # Add to pending approval
    post = web_interface.add_pending_post(platform, response)
    
    return jsonify({
        'post': post,
        'message': 'Post generated! Review and approve below.'
    })

@app.route('/api/memory')
def get_memory():
    """Get memory subjects"""
    if not web_interface.memory:
        return jsonify({'subjects': []})
    
    subjects = web_interface.memory.get_all_subjects()
    return jsonify({'subjects': subjects})

@app.route('/api/trends')
def get_trends():
    """Get current trends"""
    try:
        from exique.trend_scraper import TrendScraper
        scraper = TrendScraper()
        
        return jsonify({
            'twitter': scraper.get_twitter_trends()[:10],
            'reddit': scraper.get_reddit_trends()[:5],
            'events': scraper.get_current_events()[:5]
        })
    except Exception as e:
        return jsonify({'error': str(e), 'twitter': [], 'reddit': [], 'events': []})

def run_web_server(memory_manager=None, ollama_client=None):
    """Run Flask server"""
    global web_interface, ai_status
    
    web_interface = WebInterface(memory_manager, ollama_client)
    if ollama_client and ollama_client.connected:
        ai_status['connected'] = True
    
    print("\n" + "="*60)
    print("🌐 EXIQUE Web Interface Starting...")
    print("📱 Visit: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    run_web_server()
