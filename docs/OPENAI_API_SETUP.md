# 🔑 OpenAI API Key Setup Guide

## 🚀 Getting Your OpenAI API Key (Step-by-Step)

Your AI observability system needs an OpenAI API key to provide intelligent analysis and chat responses. Here's how to get one:

## 📋 Step 1: Create OpenAI Account

### **Go to OpenAI Platform**
1. Visit: **https://platform.openai.com**
2. Click **"Sign up"** if you don't have an account
3. Or click **"Log in"** if you already have an account

### **Account Verification**
- ✅ Verify your email address
- ✅ Add phone number (required for API access)
- ✅ Complete account setup

## 💳 Step 2: Add Billing Information

**⚠️ Important**: OpenAI requires billing info even for free tier usage.

1. **Go to Billing**: https://platform.openai.com/account/billing
2. **Click**: "Add payment method"
3. **Enter**: Credit card information
4. **Set**: Spending limit (recommended: $5-20 for testing)

### **Free Credits**
- **New accounts**: Usually get $5 in free credits
- **Valid for**: 3 months from account creation
- **Usage**: Perfect for testing and initial setup

## 🔑 Step 3: Generate API Key

### **Navigate to API Keys**
1. **Go to**: https://platform.openai.com/api-keys
2. **Click**: "Create new secret key"
3. **Name**: Give it a descriptive name (e.g., "AI Observability System")
4. **Copy**: The API key **immediately** (you won't see it again!)

### **API Key Format**
Your key will look like this:
```
sk-proj-abcd1234efgh5678ijkl9012mnop3456qrst7890uvwx1234yz56abcd7890efgh
```

**⚠️ Security Warning**: 
- Never share your API key publicly
- Don't commit it to version control
- Store it securely

## ⚙️ Step 4: Configure in Your System

### **Add to .env File**
```bash
# Edit your .env file
nano .env

# Add this line (replace with your actual key):
OPENAI_API_KEY=sk-proj-your-actual-api-key-here

# Save and exit
```

### **Verify Configuration**
```bash
# Check if key is set
grep OPENAI_API_KEY .env

# Should output:
# OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

### **Restart Services**
```bash
# Restart AI services to load new key
docker-compose restart ai-processor chat-api

# Or restart everything
docker-compose down && docker-compose up -d
```

## 🧪 Step 5: Test Your API Key

### **Quick Test**
```bash
# Test API key directly
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY_HERE"

# Should return a list of available models
```

### **Test in Your System**
```bash
# Test chat API with your key
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test openai connection", "conversation_id": "test"}'

# Should return an AI response
```

### **Test in Web Interface**
1. **Open**: http://localhost:3000
2. **Type**: "Hello, test my OpenAI connection"
3. **Expected**: You should get an AI-powered response

## 💰 Pricing Information

### **Current OpenAI Pricing (as of 2024)**

| **Model** | **Input (per 1K tokens)** | **Output (per 1K tokens)** | **Best For** |
|-----------|---------------------------|----------------------------|--------------|
| **GPT-3.5 Turbo** | $0.0005 | $0.0015 | Cost-effective, good performance |
| **GPT-4o mini** | $0.00015 | $0.0006 | Cheapest GPT-4 class model |
| **GPT-4o** | $0.0025 | $0.01 | Highest quality responses |
| **GPT-4 Turbo** | $0.01 | $0.03 | Advanced reasoning |

### **Cost Estimation for Observability System**

**Light Usage** (10 queries/day):
- **Monthly cost**: ~$2-5
- **Model**: GPT-3.5 Turbo or GPT-4o mini

**Moderate Usage** (50 queries/day):
- **Monthly cost**: ~$10-25  
- **Model**: GPT-4o mini or GPT-4o

**Heavy Usage** (200 queries/day):
- **Monthly cost**: ~$50-100
- **Model**: Any model, consider usage optimization

## 🛡️ Step 6: Security Best Practices

### **API Key Security**
```bash
# ✅ DO: Store in .env file (not committed to git)
OPENAI_API_KEY=sk-proj-your-key

# ✅ DO: Use environment variables
export OPENAI_API_KEY=sk-proj-your-key

# ❌ DON'T: Put in code files
const apiKey = "sk-proj-your-key"  // Never do this!

# ❌ DON'T: Commit to version control
# Check .gitignore includes .env
echo ".env" >> .gitignore
```

### **Usage Monitoring**
1. **Set spending limits**: https://platform.openai.com/account/billing/limits
2. **Monitor usage**: https://platform.openai.com/usage
3. **Set up alerts**: Email notifications for usage thresholds

### **Key Rotation**
```bash
# Rotate API keys regularly (monthly recommended)
# 1. Create new key
# 2. Update .env file
# 3. Restart services
# 4. Delete old key from OpenAI dashboard
```

## 🔧 Step 7: Optimize for Cost

### **Model Selection in Config**
```yaml
# Edit config/ai-config.yml
ai:
  llm:
    provider: "openai"
    model: "gpt-3.5-turbo"  # Cheapest option
    # model: "gpt-4o-mini"  # Best value
    # model: "gpt-4o"       # Highest quality
    temperature: 0.1
    max_tokens: 1024        # Limit response length
```

### **Usage Optimization**
```bash
# Set conservative limits in .env
AI_MAX_TOKENS=512          # Shorter responses
AI_TEMPERATURE=0.1         # More focused responses
CHAT_RATE_LIMIT=10         # Requests per minute
```

## 🚨 Troubleshooting

### **"Invalid API Key" Error**
```bash
# Check if key is properly set
echo $OPENAI_API_KEY

# Verify key format (should start with sk-)
# Check for extra spaces or characters
# Try creating a new key
```

### **"Quota Exceeded" Error**
- **Check billing**: https://platform.openai.com/account/billing
- **Add payment method** if missing
- **Increase spending limit** if needed
- **Wait for monthly reset** if on free tier

### **"Model Not Found" Error**
```yaml
# Use supported models in config/ai-config.yml
model: "gpt-3.5-turbo"     # Always available
# model: "gpt-4"           # Requires API access
```

### **Connection Errors**
```bash
# Test connectivity
curl https://api.openai.com/v1/models

# Check firewall/proxy settings
# Verify internet connection
```

## 🎯 Alternative Options

### **If You Don't Want to Use OpenAI**

**Option 1: Use Free/Local Models**
```yaml
# Configure for local LLM (free but requires setup)
ai:
  llm:
    provider: "ollama"      # Or "huggingface"
    model: "llama2"
    url: "http://localhost:11434"
```

**Option 2: Use Azure OpenAI** (if you have Azure credits)
```yaml
ai:
  llm:
    provider: "azure"
    endpoint: "https://your-resource.openai.azure.com/"
    api_key: "your-azure-key"
```

**Option 3: Disable AI Features** (monitoring only)
```yaml
# Set in .env
ENABLE_AI_FEATURES=false
```

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] ✅ OpenAI account created and verified
- [ ] ✅ Billing information added
- [ ] ✅ API key generated and copied
- [ ] ✅ Key added to .env file
- [ ] ✅ Services restarted
- [ ] ✅ Chat interface responds to queries
- [ ] ✅ Usage monitoring set up
- [ ] ✅ Spending limits configured

## 🎉 You're Ready!

Your AI observability system should now be fully functional with OpenAI integration!

### **Test These Queries:**
- "Show me system performance overview"
- "Why is my CPU usage high?"
- "Analyze recent error patterns"
- "What should I monitor for better performance?"

### **Access Points:**
- **Chat Interface**: http://localhost:3000
- **Usage Dashboard**: https://platform.openai.com/usage
- **API Keys**: https://platform.openai.com/api-keys

---

**Need help?** If you encounter any issues, check the troubleshooting section above or refer to `docs/CHAT_TROUBLESHOOTING.md`.

**Want to minimize costs?** Use GPT-3.5 Turbo or GPT-4o mini models for cost-effective performance!