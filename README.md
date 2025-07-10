# 🤖 AI-Powered Observability System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/react-%2320232a.svg?style=flat&logo=react&logoColor=%2361DAFB)](https://reactjs.org)

A comprehensive observability platform that collects metrics, logs, and traces from various sources and provides **AI-powered insights** through a conversational interface. Chat with your infrastructure to understand performance, troubleshoot issues, and get intelligent recommendations.

## 🌟 Key Features

✅ **Natural Language Queries** - Ask questions like "What's causing high CPU usage?"  
✅ **Multi-Source Data Collection** - Metrics, logs, traces from any source  
✅ **AI-Powered Analysis** - GPT-4 powered insights and recommendations  
✅ **Real-time Monitoring** - Live dashboards and intelligent alerting  
✅ **Easy Deployment** - One-command setup with Docker Compose  
✅ **Scalable Architecture** - From laptops to enterprise deployments  

## 🚀 Quick Start (2 minutes)

### Option 1: Automated Setup (Recommended)

```bash
# 1. Clone the repository
git clone <repository-url>
cd observability-ai

# 2. Make the start script executable
chmod +x start.sh

# 3. Start the system (with automatic configuration)
./start.sh --demo

# 4. Open your browser to http://localhost:3000
```

### Option 2: Manual Setup

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY

# 2. Start services
make build && make up

# 3. Wait for services to be ready (2-3 minutes)
make health
```

### Option 3: Minimal Hardware Mode

For systems with limited resources (< 8GB RAM):

```bash
./start.sh --minimal
```

## 🎯 What You Get

After setup, you'll have access to:

| Service | URL | Description |
|---------|-----|-------------|
| 🤖 **AI Chat Interface** | http://localhost:3000 | Main interface - chat with your infrastructure |
| 📊 **Grafana Dashboards** | http://localhost:3001 | Visual monitoring (admin/admin) |
| 📈 **Prometheus** | http://localhost:9090 | Metrics collection and queries |
| 🔍 **Jaeger Tracing** | http://localhost:16686 | Distributed tracing visualization |
| 🔌 **Chat API** | http://localhost:8000 | REST/WebSocket API for integrations |

## 💬 Try These Example Queries

Once your system is running, try asking:

- *"Show me system performance overview"*
- *"What are the current issues?"*
- *"Analyze recent errors"*
- *"Show me slow requests"*
- *"What's the CPU and memory usage trend?"*
- *"Are there any anomalies in the last hour?"*

## 📋 Requirements

### Minimum Hardware
- **CPU**: 4 cores
- **RAM**: 8 GB (4 GB in minimal mode)
- **Disk**: 20 GB free space
- **Network**: Internet access for AI features

### Software Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- OpenAI API key (for AI features)

> **💡 Tip**: The system works on laptops! Use `./start.sh --minimal` for reduced resource usage.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   Collection    │    │     Storage     │
│                 │    │                 │    │                 │
│  • Applications │───▶│  • OpenTelemetry│───▶│  • Prometheus   │
│  • Infrastructure │   │  • Prometheus   │    │  • Jaeger       │
│  • Databases    │    │  • Fluentd      │    │  • Elasticsearch│
│  • APIs         │    │  • Custom       │    │  • Vector DB    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌─────────────────┐             │
│   AI Interface  │    │   AI Processing │◀────────────┘
│                 │    │                 │
│  • Chat UI      │◀───│  • Data Analysis│
│  • Dashboards   │    │  • Embeddings   │
│  • Alerts       │    │  • LLM Integration│
└─────────────────┘    └─────────────────┘
```

## 🔧 Configuration

### Essential Configuration (.env file)
```bash
# Required: OpenAI API key for AI features
OPENAI_API_KEY=sk-your-key-here

# Optional: Adjust for your environment
LOG_LEVEL=INFO
AI_MODEL=gpt-4
ENVIRONMENT=development
```

### Advanced Configuration
- **Data Sources**: Connect your Prometheus, Elasticsearch, or custom sources
- **AI Models**: Use OpenAI, Anthropic, or local LLMs
- **Resource Limits**: Optimize for your hardware
- **Authentication**: Add security layers (coming soon)

## 📖 Documentation

- **[🚀 Complete Setup Guide](SETUP.md)** - Detailed installation and configuration
- **[🔧 Configuration Reference](config/)** - All configuration options
- **[🐛 Troubleshooting](SETUP.md#troubleshooting)** - Common issues and solutions
- **[📊 Performance Tuning](SETUP.md#performance-optimization-for-low-resource-systems)** - Optimize for your hardware

## 🛠️ Development

```bash
# Development mode with hot reload
make dev

# Run tests
make test

# View logs
make logs

# Check service health
make health

# Clean up and restart
make clean && make build && make up
```

## 🚀 Deployment Options

### Local Development
```bash
docker-compose up -d
```

### Minimal Resource Mode
```bash
docker-compose -f docker-compose.yml -f docker-compose.minimal.yml up -d
```

### Production (Coming Soon)
- Kubernetes manifests
- Helm charts
- Cloud provider templates

## 🤝 Contributing

We welcome contributions! Areas where help is needed:

- Additional AI models integration
- More data source connectors
- UI/UX improvements
- Documentation and examples
- Performance optimizations

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Need Help?

1. **Quick Issues**: Check the [troubleshooting guide](SETUP.md#troubleshooting)
2. **Setup Problems**: Read the [complete setup guide](SETUP.md)
3. **Feature Requests**: Open an issue with the "enhancement" label
4. **Bugs**: Open an issue with detailed reproduction steps

## 🎉 What's Next?

After getting the system running:

1. **Explore the Chat Interface** - Try different types of questions
2. **Connect Your Data** - Add your applications and infrastructure
3. **Customize Dashboards** - Create views for your specific needs
4. **Set Up Alerts** - Get notified about important issues
5. **Scale Up** - Deploy to production environments

---

**Ready to get started?** Run `./start.sh --demo` and start chatting with your infrastructure! 🚀