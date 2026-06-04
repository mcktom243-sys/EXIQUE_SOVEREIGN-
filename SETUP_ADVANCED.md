# Setup Instructions for EXIQUE SOVEREIGN Advanced Features

## Social Media Credentials Setup

Create a `.env` file in your project root with:

```bash
# Twitter/X API
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
TWITTER_BEARER_TOKEN=your_bearer_token
TWITTER_USER_ID=your_user_id

# Reddit API
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
```

## Getting API Credentials

### Twitter/X
1. Go to https://developer.twitter.com
2. Create an app
3. Go to "Keys and tokens"
4. Copy API Key, API Secret, Access Token, Access Secret
5. Enable API v2 and get Bearer Token

### Reddit
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create another app"
3. Choose "script"
4. Copy Client ID (under app name) and Client Secret
5. Use your Reddit username and password

## Running with All Features

### Terminal 1 - Start Ollama
```bash
ollama serve
```

### Terminal 2 - Start EXIQUE with Tools
```bash
python3 -m exique.main
```

### Terminal 3 (Optional) - Start API Server
```bash
python3 -m exique.api_server
```

## Using Tools in Chat

### Code Execution
```
You: Execute this Python code and show me the result
AI: I'll execute that for you.
[EXECUTE_CODE]
import json
data = {"hello": "world"}
print(json.dumps(data, indent=2))
[/EXECUTE_CODE]
```

### Social Media Posts
```
You: Post "Hello world" on Twitter
AI: I'll post that to Twitter now.
[SOCIAL:twitter:post_tweet]text="Hello world"[/SOCIAL]
```

### Read Social Feed
```
You: Show me what people are saying about AI on Reddit
AI: Let me check r/AI for you.
[SOCIAL:reddit:read_subreddit]subreddit="AI",limit=5[/SOCIAL]
```

## Monetization Setup

### Create API Keys
```bash
curl -X POST http://localhost:5000/api/create-key \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","plan":"pro"}'
```

### API Usage
```bash
# Chat with API
curl -X POST http://localhost:5000/api/generate \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello EXIQUE"}'

# Check usage
curl http://localhost:5000/api/usage \
  -H "X-API-Key: YOUR_API_KEY"
```

## Pricing Tiers (Example)

- **Free**: 100 requests/month
- **Pro**: $10/month - 10,000 requests/month
- **Enterprise**: Custom pricing

## Features Enabled

✅ **Code Execution** - Safe Python code execution
✅ **Social Media** - Read/write to Twitter & Reddit
✅ **Learning** - Learns from interactions and feedback
✅ **Personality** - Customizable tone and traits
✅ **API** - HTTP endpoints for monetization
✅ **Memory** - Persistent conversation memory
✅ **Tool Integration** - Unified tool system

## Customizing EXIQUE

### Change Personality
In chat: `/set-tone witty` or `/set-tone professional`

### View Settings
```bash
cat ~/.exique/personality.json
```

### Access Logs
```bash
# View all interactions
cat ~/.exique/interactions.jsonl

# View execution history
python3 -c "from exique.code_executor import CodeExecutor; e = CodeExecutor(); print(e.get_history())"
```

## Performance Notes

- Code execution: <1 second
- Social media posts: 2-5 seconds (API dependent)
- Memory recall: <100ms
- AI responses: 1-5 seconds (depends on response length)

## Troubleshooting

**Social media not working?**
```bash
python3 -c "from exique.social_tools import SocialMediaManager; s = SocialMediaManager(); print(s.get_status())"
```

**API key not working?**
```bash
# Verify key exists
cat ~/.exique/api_keys.json
```

**Code execution errors?**
- Check Termux permissions
- Some system calls may be restricted

---

**Next Steps:**
1. Add your social media credentials to `.env`
2. Test each tool individually
3. Set up API monetization
4. Customize personality to your brand
