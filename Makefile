.PHONY: help build up down restart logs clean dev test health status

# Default target
help:
	@echo "AI-Powered Observability System"
	@echo "================================"
	@echo ""
	@echo "Available commands:"
	@echo "  make build     - Build all Docker images"
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make restart   - Restart all services"
	@echo "  make logs      - View logs from all services"
	@echo "  make clean     - Clean up containers and volumes"
	@echo "  make dev       - Start in development mode"
	@echo "  make test      - Run tests"
	@echo "  make health    - Check health of all services"
	@echo "  make status    - Show status of all services"
	@echo ""
	@echo "Quick start:"
	@echo "  1. Set your OpenAI API key: export OPENAI_API_KEY=your_key_here"
	@echo "  2. Run: make up"
	@echo "  3. Open http://localhost:3000 for the chat interface"

# Build all Docker images
build:
	@echo "Building all Docker images..."
	docker-compose build --no-cache

# Start all services
up:
	@echo "Starting AI-Powered Observability System..."
	docker-compose up -d
	@echo ""
	@echo "Services are starting up. This may take a few minutes..."
	@echo ""
	@echo "Access points:"
	@echo "  Chat Interface:  http://localhost:3000"
	@echo "  Grafana:         http://localhost:3001 (admin/admin)"
	@echo "  Prometheus:      http://localhost:9090"
	@echo "  Jaeger:          http://localhost:16686"
	@echo "  Chat API:        http://localhost:8000"
	@echo ""
	@echo "Run 'make health' to check service health"

# Stop all services
down:
	@echo "Stopping all services..."
	docker-compose down

# Restart all services
restart: down up

# View logs from all services
logs:
	docker-compose logs -f

# View logs from specific service
logs-%:
	docker-compose logs -f $*

# Clean up containers, networks, and volumes
clean:
	@echo "Cleaning up containers, networks, and volumes..."
	docker-compose down -v
	docker system prune -f
	docker volume prune -f

# Start in development mode (with file watching)
dev:
	@echo "Starting in development mode..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Run tests
test:
	@echo "Running tests..."
	docker-compose exec ai-processor python -m pytest
	docker-compose exec chat-api python -m pytest

# Check health of all services
health:
	@echo "Checking service health..."
	@echo ""
	@echo "Chat API Health:"
	@curl -s http://localhost:8000/health | jq . || echo "Chat API not responding"
	@echo ""
	@echo "Prometheus Health:"
	@curl -s http://localhost:9090/-/healthy || echo "Prometheus not responding"
	@echo ""
	@echo "Elasticsearch Health:"
	@curl -s http://localhost:9200/_cluster/health | jq . || echo "Elasticsearch not responding"
	@echo ""
	@echo "Jaeger Health:"
	@curl -s http://localhost:16686/ > /dev/null && echo "Jaeger: OK" || echo "Jaeger not responding"

# Show status of all services
status:
	@echo "Service Status:"
	@echo "==============="
	docker-compose ps

# Initialize the system (first time setup)
init:
	@echo "Initializing AI-Powered Observability System..."
	@if [ -z "$$OPENAI_API_KEY" ]; then \
		echo "Warning: OPENAI_API_KEY not set. The AI features will not work."; \
		echo "Set it with: export OPENAI_API_KEY=your_key_here"; \
		echo ""; \
	fi
	cp .env.example .env
	@echo "Environment file created. Please edit .env with your configuration."
	@echo "Then run: make build && make up"

# Quick demo setup
demo:
	@echo "Setting up demo environment..."
	@if [ -z "$$OPENAI_API_KEY" ]; then \
		echo "Warning: OPENAI_API_KEY not set. AI features will be limited."; \
	fi
	make build
	make up
	@echo ""
	@echo "Demo environment is starting up..."
	@echo "Please wait 2-3 minutes for all services to be ready."
	@echo ""
	@echo "Then visit http://localhost:3000 to try the AI chat interface!"

# Backup data
backup:
	@echo "Creating backup..."
	mkdir -p backup
	docker run --rm -v observability_prometheus_data:/data -v $(PWD)/backup:/backup alpine tar czf /backup/prometheus-$(shell date +%Y%m%d-%H%M%S).tar.gz -C /data .
	docker run --rm -v observability_grafana_data:/data -v $(PWD)/backup:/backup alpine tar czf /backup/grafana-$(shell date +%Y%m%d-%H%M%S).tar.gz -C /data .
	docker run --rm -v observability_elasticsearch_data:/data -v $(PWD)/backup:/backup alpine tar czf /backup/elasticsearch-$(shell date +%Y%m%d-%H%M%S).tar.gz -C /data .
	@echo "Backup completed in ./backup/"

# Restore data
restore:
	@echo "Available backups:"
	@ls -la backup/ | grep tar.gz || echo "No backups found"
	@echo "To restore, run: make restore-file BACKUP_FILE=filename.tar.gz"

# Install dependencies (for local development)
install:
	@echo "Installing development dependencies..."
	# AI Processor dependencies
	cd services/ai-processor && pip install -r requirements.txt
	# Chat API dependencies  
	cd services/chat-api && pip install -r requirements.txt
	# Frontend dependencies
	cd services/chat-frontend && npm install

# Update all services
update:
	@echo "Updating all services..."
	git pull
	make build
	make restart

# Show system resource usage
resources:
	@echo "System Resource Usage:"
	@echo "====================="
	docker stats --no-stream