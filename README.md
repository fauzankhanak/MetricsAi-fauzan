# AI-Powered Observability System

A comprehensive observability platform that collects metrics, logs, and traces from various sources and provides AI-powered insights through a conversational interface.

## Architecture Overview

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

## Features

- **Multi-Source Data Collection**: Metrics, logs, traces from various sources
- **AI-Powered Analysis**: Natural language querying and insights
- **Intelligent Recommendations**: Performance optimization suggestions
- **Real-time Monitoring**: Live dashboards and alerting
- **Scalable Architecture**: Supports small to enterprise deployments

## Quick Start

1. **Prerequisites**:
   ```bash
   # Ensure Docker and Docker Compose are installed
   docker --version
   docker-compose --version
   ```

2. **Deploy the System**:
   ```bash
   # Start all services
   docker-compose up -d
   
   # Check status
   docker-compose ps
   ```

3. **Access Interfaces**:
   - Chat Interface: http://localhost:3000
   - Grafana Dashboards: http://localhost:3001
   - Prometheus: http://localhost:9090
   - Jaeger UI: http://localhost:16686

## Components

### Data Collection
- **OpenTelemetry Collector**: Traces and metrics collection
- **Prometheus**: Metrics scraping and storage
- **Fluentd**: Log aggregation and processing
- **Custom Exporters**: Application-specific data collection

### Storage
- **Prometheus**: Time-series metrics storage
- **Jaeger**: Distributed tracing storage
- **Elasticsearch**: Log storage and search
- **Qdrant**: Vector database for AI embeddings

### AI Processing
- **Data Pipeline**: Processes observability data into AI-friendly formats
- **Embedding Service**: Creates vector embeddings of logs, metrics, traces
- **LLM Integration**: OpenAI/Local LLM for analysis and recommendations

### User Interface
- **Chat Interface**: Natural language querying
- **Dashboards**: Visual monitoring and analytics
- **API**: RESTful and GraphQL APIs for integration

## Configuration

See `config/` directory for detailed configuration options:
- `prometheus.yml`: Metrics collection configuration
- `otelcol.yml`: OpenTelemetry collector configuration
- `fluent.conf`: Log processing configuration
- `ai-config.yml`: AI service configuration

## Development

```bash
# Start development environment
make dev

# Run tests
make test

# Build all images
make build
```

## Deployment

### Local Development
```bash
docker-compose up -d
```

### Production (Kubernetes)
```bash
kubectl apply -f k8s/
```

## Documentation

- [Data Collection Setup](docs/data-collection.md)
- [AI Configuration](docs/ai-setup.md)
- [API Reference](docs/api.md)
- [Troubleshooting](docs/troubleshooting.md)

## License

MIT License