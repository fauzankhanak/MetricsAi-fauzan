# AI-Powered Observability System - Setup Guide

This guide will help you set up the AI-powered observability system with minimum hardware requirements.

## 🖥️ Minimum Hardware Requirements

### Development/Testing Environment
- **CPU**: 4 cores (Intel i5 or AMD Ryzen 5 equivalent)
- **RAM**: 8 GB (12 GB recommended)
- **Disk Space**: 20 GB free space
- **Network**: Stable internet connection for AI API calls

### Production Environment
- **CPU**: 8 cores (Intel i7 or AMD Ryzen 7 equivalent)
- **RAM**: 16 GB (32 GB recommended)
- **Disk Space**: 50 GB free space (SSD recommended)
- **Network**: High-speed internet connection

### Cloud Minimum Specifications
- **AWS**: t3.large (2 vCPU, 8 GB RAM) or higher
- **Google Cloud**: e2-standard-4 (4 vCPU, 16 GB RAM) or higher
- **Azure**: Standard_D4s_v3 (4 vCPU, 16 GB RAM) or higher

## 📋 Prerequisites

### Required Software
1. **Docker** (version 20.10 or higher)
2. **Docker Compose** (version 2.0 or higher)
3. **Git** (for cloning the repository)
4. **Make** (optional, for using Makefile commands)
5. **curl** and **jq** (for health checks)

### Optional Tools
- **Node.js** (for frontend development)
- **Python 3.11+** (for AI service development)
- **kubectl** (for Kubernetes deployment)

## 🚀 Quick Start (5 minutes)

### Step 1: Install Prerequisites

#### On Ubuntu/Debian:
```bash
# Update package index
sudo apt update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin

# Install additional tools
sudo apt install git make curl jq

# Log out and back in for Docker group changes to take effect
```

#### On macOS:
```bash
# Install Docker Desktop from https://docker.com/products/docker-desktop
# Or using Homebrew:
brew install --cask docker
brew install git make curl jq
```

#### On Windows:
1. Install [Docker Desktop for Windows](https://docker.com/products/docker-desktop)
2. Install [Git for Windows](https://git-scm.com/download/win)
3. Use PowerShell or WSL2 for commands

### Step 2: Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd observability-ai

# Create environment configuration
cp .env.example .env

# Edit the .env file with your settings (minimum required: OPENAI_API_KEY)
nano .env  # or use your preferred editor
```

### Step 3: Configure Environment

**Minimum required configuration in `.env`:**
```bash
# Required: Set your OpenAI API key
OPENAI_API_KEY=sk-your-actual-openai-api-key-here

# Optional: Adjust for low-resource environments
AI_PROCESSOR_MEMORY_LIMIT=1024m
ELASTICSEARCH_MEMORY_LIMIT=1024m
LOG_LEVEL=WARNING
```

### Step 4: Deploy the System

```bash
# Build and start all services
make build
make up

# Or using Docker Compose directly:
docker-compose build
docker-compose up -d
```

### Step 5: Verify Installation

```bash
# Check service status
make status

# Check health
make health

# View logs
make logs
```

## 🔧 Detailed Setup Instructions

### Manual Docker Compose Setup

If you prefer not to use the Makefile:

```bash
# Build all images
docker-compose build --no-cache

# Start services in detached mode
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Low-Resource Configuration

For systems with limited resources, edit `docker-compose.yml` and add resource limits:

```yaml
services:
  ai-processor:
    # ... existing configuration ...
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'

  elasticsearch:
    # ... existing configuration ...
    environment:
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
```

## 🌐 Access URLs

Once the system is running, access these interfaces:

| Service | URL | Credentials |
|---------|-----|-------------|
| **Chat Interface** | http://localhost:3000 | None |
| **Grafana Dashboard** | http://localhost:3001 | admin/admin |
| **Prometheus** | http://localhost:9090 | None |
| **Jaeger Tracing** | http://localhost:16686 | None |
| **Chat API** | http://localhost:8000 | None |
| **Elasticsearch** | http://localhost:9200 | None |

## 🔍 Verification Steps

### 1. Check All Services Are Running
```bash
docker-compose ps
```
All services should show "Up" status.

### 2. Test Chat Interface
1. Open http://localhost:3000
2. Try asking: "Show me system performance overview"
3. You should get an AI-powered response

### 3. Verify Data Collection
```bash
# Check Prometheus metrics
curl http://localhost:9090/api/v1/targets

# Check Elasticsearch indices
curl http://localhost:9200/_cat/indices

# Check AI Processor health
curl http://localhost:8000/health
```

## ⚡ Performance Optimization for Low-Resource Systems

### 1. Reduce Memory Usage

Edit `config/ai-config.yml`:
```yaml
# Reduce batch sizes
data_processing:
  metrics:
    aggregation_window: "10m"  # Increase from 5m
  logs:
    filtering:
      exclude_patterns:
        - "health-check"
        - "ping"
        - "metrics"
        - "debug"  # Add debug logs

cache:
  memory:
    max_size_mb: 256  # Reduce from 512
```

### 2. Optimize Elasticsearch

Edit `docker-compose.yml`:
```yaml
elasticsearch:
  environment:
    - "ES_JAVA_OPTS=-Xms256m -Xmx256m"  # Reduce memory
    - discovery.type=single-node
    - xpack.security.enabled=false
    - "cluster.routing.allocation.disk.threshold_enabled=false"
```

### 3. Reduce Prometheus Retention

Edit `config/prometheus.yml`:
```yaml
global:
  scrape_interval: 30s  # Increase from 15s
  evaluation_interval: 30s
```

Add to Docker Compose:
```yaml
prometheus:
  command:
    - '--storage.tsdb.retention.time=24h'  # Reduce from 200h
```

### 4. Disable Non-Essential Services

For minimal deployment, comment out these services in `docker-compose.yml`:
- `sample-app` (demo only)
- `grafana` (if only using chat interface)

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. "Port already in use" Error
```bash
# Check what's using the port
sudo netstat -tulpn | grep :3000

# Kill the process or change ports in docker-compose.yml
```

#### 2. "Out of Memory" Error
```bash
# Check Docker memory usage
docker stats

# Reduce memory limits in .env file:
AI_PROCESSOR_MEMORY_LIMIT=512m
ELASTICSEARCH_MEMORY_LIMIT=512m
```

#### 3. AI Features Not Working
```bash
# Check if OpenAI API key is set
echo $OPENAI_API_KEY

# Verify in container
docker-compose exec ai-processor env | grep OPENAI
```

#### 4. Services Not Starting
```bash
# Check logs for specific service
docker-compose logs ai-processor

# Restart specific service
docker-compose restart ai-processor
```

#### 5. Elasticsearch Yellow/Red Status
```bash
# Check cluster health
curl http://localhost:9200/_cluster/health

# Common fix: reduce replica count
curl -X PUT "localhost:9200/_settings" -H 'Content-Type: application/json' -d'
{
  "index": {
    "number_of_replicas": 0
  }
}'
```

### Log Locations

```bash
# View all logs
make logs

# View specific service logs
docker-compose logs -f ai-processor
docker-compose logs -f chat-api
docker-compose logs -f elasticsearch

# Follow logs in real-time
docker-compose logs -f --tail=100
```

## 🔧 Advanced Configuration

### Custom OpenAI Configuration

Edit `config/ai-config.yml`:
```yaml
ai:
  llm:
    provider: "openai"
    model: "gpt-3.5-turbo"  # Use cheaper model for testing
    temperature: 0.1
    max_tokens: 1024  # Reduce for cost savings
```

### Using Local LLM (No OpenAI Required)

For offline usage, configure a local LLM:
```yaml
ai:
  llm:
    provider: "local"
    model: "llama2"
    url: "http://localhost:11434"  # Ollama URL
```

### Data Source Configuration

Add your own Prometheus/Elasticsearch instances:
```bash
# In .env file
PROMETHEUS_URL=http://your-prometheus:9090
ELASTICSEARCH_URL=http://your-elasticsearch:9200
```

## 📊 Monitoring Resource Usage

### Check System Resources
```bash
# Overall system usage
make resources

# Docker container stats
docker stats

# Disk usage
df -h

# Memory usage
free -h
```

### Optimize Based on Usage
```bash
# If high CPU: Increase scrape intervals
# If high memory: Reduce retention periods
# If high disk: Enable compression, reduce retention
```

## 🔄 Maintenance Commands

```bash
# Update to latest version
make update

# Backup data
make backup

# Clean up old data
make clean

# Restart all services
make restart

# View system status
make status
```

## 🆘 Getting Help

### Support Channels
1. **Documentation**: Check README.md and this guide
2. **Logs**: Always check service logs first
3. **Health Checks**: Use `make health` to identify issues
4. **Resource Monitor**: Use `make resources` to check usage

### Common Commands Summary
```bash
# Quick health check
make health

# View all logs
make logs

# Restart everything
make restart

# Clean slate restart
make clean && make build && make up

# Check resource usage
make resources
```

## 🧠 Enhancing AI Intelligence

The system includes advanced AI intelligence features that can be enhanced with your data:

### Quick Start (Demo Data)
```bash
# Train AI with sample data
python scripts/enhance_ai_intelligence.py --demo
```

### Import Your Historical Data
```bash
# Import your incidents for learning
python scripts/enhance_ai_intelligence.py --import-incidents your_incidents.json

# Import with both incidents and metrics
python scripts/enhance_ai_intelligence.py --incidents incidents.json --metrics metrics.json
```

### Expected Data Format
Create `your_incidents.json`:
```json
{
  "incidents": [
    {
      "title": "High CPU usage incident",
      "timestamp": "2024-01-15T10:30:00Z",
      "symptoms": ["high_cpu", "slow_response"],
      "metrics": {"cpu": 92, "memory": 78, "latency": 3200},
      "root_cause": "Inefficient database query",
      "solution": "Optimized query and added indexing",
      "prevention": ["Add query monitoring", "Review queries in deployment"]
    }
  ]
}
```

### What This Does
1. **Learns Your Environment**: Analyzes your normal vs abnormal patterns
2. **Pattern Recognition**: Identifies recurring issues and solutions
3. **Contextual Intelligence**: Provides specific advice for YOUR system
4. **Continuous Learning**: Gets smarter with each incident you add

After enhancement, restart the AI service:
```bash
docker-compose restart ai-processor chat-api
```

### Testing Enhanced Intelligence
After training, test with these questions:
- "Why is my CPU high?"
- "What should I check for memory issues?"
- "Analyze this error pattern for me"
- "What patterns predict future outages?"

## 🎯 Next Steps

After successful setup:

1. **Enhance AI Intelligence**: Train with your historical data (see above)
2. **Explore the Chat Interface**: Try different queries
3. **Set up Grafana Dashboards**: Create custom visualizations
4. **Configure Alerts**: Set up notifications for issues
5. **Integrate Your Applications**: Add OpenTelemetry instrumentation
6. **Scale the System**: Move to production environment

## 📈 Scaling for Production

When ready for production:

1. **Use External Databases**: Replace embedded DBs with managed services
2. **Add Load Balancers**: Distribute traffic across multiple instances
3. **Implement Authentication**: Add security layers
4. **Set up Monitoring**: Monitor the monitoring system itself
5. **Backup Strategy**: Implement automated backups

---

**Ready to start?** Run `make demo` for a quick setup with sample data!