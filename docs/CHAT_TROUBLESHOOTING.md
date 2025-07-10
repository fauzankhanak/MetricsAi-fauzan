# 🔧 Chat Interface Troubleshooting Guide

## 🚨 Solving Blocked Chat Status

If your chat interface is blocked or not responding, follow these systematic troubleshooting steps:

## 🔍 Quick Diagnosis

### Step 1: Check Service Status
```bash
# Check if all services are running
docker-compose ps

# Check specific chat services
docker-compose ps chat-frontend chat-api ai-processor
```

**Expected output**: All services should show "Up" status.

### Step 2: Test Chat API Health
```bash
# Test chat API directly
curl -f http://localhost:8000/health

# Test AI processor health
curl -f http://localhost:5000/health

# Test with verbose output
curl -v http://localhost:8000/health
```

### Step 3: Check Chat Frontend
```bash
# Test frontend is accessible
curl -f http://localhost:3000

# Check if frontend can reach API
curl -f http://localhost:3000/api/health
```

## 🛠️ Common Issues and Solutions

### Issue 1: "Service Unavailable" or 503 Errors

**Symptoms:**
- Chat interface shows "Service Unavailable"
- API returns 503 status codes
- Chat messages not being processed

**Solutions:**

```bash
# Check service logs
docker-compose logs chat-api
docker-compose logs ai-processor

# Restart chat services
docker-compose restart chat-api ai-processor

# If still failing, rebuild and restart
docker-compose down
docker-compose build chat-api ai-processor
docker-compose up -d
```

### Issue 2: "Connection Refused" or Network Errors

**Symptoms:**
- Frontend can't connect to backend
- WebSocket connections failing
- Network timeout errors

**Solutions:**

```bash
# Check port availability
netstat -tulpn | grep -E "(3000|8000|5000)"

# Check Docker network
docker network ls
docker network inspect observability-ai_default

# Restart with fresh network
docker-compose down
docker network prune -f
docker-compose up -d
```

### Issue 3: "Authentication Failed" or API Key Issues

**Symptoms:**
- Chat works but AI responses fail
- "Invalid API key" errors
- Empty or generic responses

**Solutions:**

```bash
# Check environment variables
docker-compose exec chat-api env | grep OPENAI
docker-compose exec ai-processor env | grep OPENAI

# Update .env file
nano .env
# Add: OPENAI_API_KEY=sk-your-actual-key-here

# Restart services to reload environment
docker-compose restart chat-api ai-processor
```

### Issue 4: Memory/Resource Issues

**Symptoms:**
- Services randomly stopping
- Out of memory errors
- Slow response times

**Solutions:**

```bash
# Check resource usage
docker stats

# Reduce memory limits in docker-compose.yml
# For chat-api service:
services:
  chat-api:
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M

# Restart with new limits
docker-compose down
docker-compose up -d
```

### Issue 5: CORS or Frontend Issues

**Symptoms:**
- Frontend loads but chat doesn't work
- Browser console shows CORS errors
- "Access denied" errors

**Solutions:**

```bash
# Check browser console for errors
# Open browser developer tools (F12) and check console

# Restart frontend service
docker-compose restart chat-frontend

# Clear browser cache and cookies
# Or try incognito/private browsing mode
```

## 🔧 Advanced Troubleshooting

### Debug Mode Activation

Enable detailed logging:

```bash
# Create debug environment
cat >> .env << EOF
LOG_LEVEL=DEBUG
CHAT_DEBUG=true
AI_DEBUG=true
EOF

# Restart with debug logging
docker-compose restart chat-api ai-processor

# Monitor logs in real-time
docker-compose logs -f chat-api ai-processor
```

### Manual Service Testing

Test each component individually:

```bash
# 1. Test AI Processor directly
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test message", "context": {}}'

# 2. Test Chat API
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello", "conversation_id": "test-123"}'

# 3. Test WebSocket connection
curl --include \
  --no-buffer \
  --header "Connection: Upgrade" \
  --header "Upgrade: websocket" \
  --header "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" \
  --header "Sec-WebSocket-Version: 13" \
  http://localhost:8000/ws/test-123
```

### Database Connectivity Issues

```bash
# Check if data sources are accessible
docker-compose exec chat-api curl http://prometheus:9090/api/v1/targets
docker-compose exec chat-api curl http://elasticsearch:9200/_cluster/health

# Test vector database
docker-compose exec ai-processor curl http://qdrant:6333/cluster
```

## 🚀 Complete Reset Solution

If all else fails, perform a complete reset:

```bash
# 1. Stop all services
docker-compose down -v

# 2. Remove all containers and volumes
docker system prune -a -f --volumes

# 3. Rebuild everything from scratch
docker-compose build --no-cache

# 4. Start services one by one
docker-compose up -d qdrant elasticsearch prometheus
sleep 30
docker-compose up -d ai-processor
sleep 20
docker-compose up -d chat-api
sleep 10
docker-compose up -d chat-frontend

# 5. Verify each service as it starts
watch -n 2 "docker-compose ps"
```

## 🧪 Verification Script

Create a comprehensive test script:

```bash
# Create verification script
cat > test-chat.sh << 'EOF'
#!/bin/bash

echo "🔍 Testing Chat System Health..."

# Test 1: Service Status
echo "1. Checking service status..."
if docker-compose ps | grep -q "Up"; then
    echo "✅ Services are running"
else
    echo "❌ Some services are down"
    docker-compose ps
    exit 1
fi

# Test 2: API Health
echo "2. Testing API health..."
if curl -f -s http://localhost:8000/health > /dev/null; then
    echo "✅ Chat API is healthy"
else
    echo "❌ Chat API health check failed"
    exit 1
fi

# Test 3: AI Processor Health
echo "3. Testing AI processor..."
if curl -f -s http://localhost:5000/health > /dev/null; then
    echo "✅ AI Processor is healthy"
else
    echo "❌ AI Processor health check failed"
    exit 1
fi

# Test 4: Frontend Access
echo "4. Testing frontend access..."
if curl -f -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is accessible"
else
    echo "❌ Frontend access failed"
    exit 1
fi

# Test 5: End-to-end Chat Test
echo "5. Testing end-to-end chat..."
response=$(curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "health check", "conversation_id": "test"}')

if echo "$response" | grep -q "response"; then
    echo "✅ End-to-end chat test successful"
    echo "🎉 Chat system is fully functional!"
else
    echo "❌ End-to-end chat test failed"
    echo "Response: $response"
    exit 1
fi
EOF

chmod +x test-chat.sh
./test-chat.sh
```

## 📋 Environment Check Script

```bash
# Create environment verification script
cat > check-env.sh << 'EOF'
#!/bin/bash

echo "🔍 Checking Environment Configuration..."

# Check required environment variables
required_vars=("OPENAI_API_KEY")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Missing required environment variable: $var"
        missing_vars=true
    else
        echo "✅ $var is set"
    fi
done

if [ "$missing_vars" = true ]; then
    echo "Please set missing environment variables in .env file"
    exit 1
fi

# Check Docker resources
echo "🐳 Docker Resource Check..."
docker system df

# Check available ports
echo "🔌 Port Availability Check..."
for port in 3000 8000 5000 9090 9200; do
    if lsof -i :$port > /dev/null 2>&1; then
        echo "⚠️  Port $port is in use"
    else
        echo "✅ Port $port is available"
    fi
done

echo "✅ Environment check complete"
EOF

chmod +x check-env.sh
./check-env.sh
```

## 🎯 Quick Fix Commands

**Most Common Solutions:**

```bash
# Quick fix 1: Restart chat services
docker-compose restart chat-api ai-processor chat-frontend

# Quick fix 2: Rebuild and restart
docker-compose down && docker-compose up -d --build

# Quick fix 3: Check and set API key
echo "OPENAI_API_KEY=your-key-here" >> .env
docker-compose restart chat-api ai-processor

# Quick fix 4: Clear browser cache
# Open browser > F12 > Application tab > Clear Storage

# Quick fix 5: Reset everything
docker-compose down -v && docker-compose up -d
```

## 📞 Still Having Issues?

If the chat is still blocked after trying these solutions:

1. **Check the logs**: `docker-compose logs -f chat-api ai-processor`
2. **Verify your .env file**: Ensure OPENAI_API_KEY is set correctly
3. **Test with minimal config**: Use `docker-compose.minimal.yml` if available
4. **Check system resources**: Ensure sufficient RAM/CPU available
5. **Try browser incognito mode**: Rule out browser cache issues

## 📝 Report an Issue

If none of these solutions work, gather this information:

```bash
# Collect diagnostic information
echo "=== System Information ===" > chat-debug.log
uname -a >> chat-debug.log
docker --version >> chat-debug.log
docker-compose --version >> chat-debug.log

echo "=== Service Status ===" >> chat-debug.log
docker-compose ps >> chat-debug.log

echo "=== Service Logs ===" >> chat-debug.log
docker-compose logs chat-api >> chat-debug.log
docker-compose logs ai-processor >> chat-debug.log

echo "=== Environment Variables ===" >> chat-debug.log
env | grep -E "(OPENAI|LOG_LEVEL|HOST|PORT)" >> chat-debug.log

echo "Debug information saved to chat-debug.log"
```

**Your chat should be working now!** 🚀

Try accessing: http://localhost:3000