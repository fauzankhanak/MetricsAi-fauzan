#!/bin/bash

# AI-Powered Observability System - Quick Start Script
# This script helps you get the system up and running with minimal configuration

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MINIMAL_MODE=false
DEMO_MODE=false
SKIP_CHECKS=false

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Print banner
print_banner() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              AI-Powered Observability System                 ║"
    echo "║                    Quick Start Script                        ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
}

# Print help
print_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -m, --minimal     Start in minimal resource mode (for low-end hardware)"
    echo "  -d, --demo        Start with demo data and sample application"
    echo "  -s, --skip-checks Skip prerequisite checks"
    echo "  -h, --help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                # Normal startup"
    echo "  $0 --minimal      # Minimal resource mode"
    echo "  $0 --demo         # Demo mode with sample data"
    echo ""
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -m|--minimal)
                MINIMAL_MODE=true
                shift
                ;;
            -d|--demo)
                DEMO_MODE=true
                shift
                ;;
            -s|--skip-checks)
                SKIP_CHECKS=true
                shift
                ;;
            -h|--help)
                print_help
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                print_help
                exit 1
                ;;
        esac
    done
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    if [[ "$SKIP_CHECKS" == "true" ]]; then
        print_warning "Skipping prerequisite checks"
        return 0
    fi

    print_status "Checking prerequisites..."

    # Check Docker
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        echo "Installation guide: https://docs.docker.com/get-docker/"
        exit 1
    fi

    # Check Docker Compose
    if ! command_exists docker-compose && ! docker compose version >/dev/null 2>&1; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        echo "Installation guide: https://docs.docker.com/compose/install/"
        exit 1
    fi

    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi

    # Check available memory
    if command_exists free; then
        AVAILABLE_MEMORY=$(free -m | awk 'NR==2{printf "%.0f", $7}')
        if [[ $AVAILABLE_MEMORY -lt 4096 ]] && [[ "$MINIMAL_MODE" == "false" ]]; then
            print_warning "Available memory is ${AVAILABLE_MEMORY}MB. Consider using --minimal flag for better performance."
        fi
    fi

    # Check disk space
    if command_exists df; then
        AVAILABLE_DISK=$(df -BM . | awk 'NR==2{gsub(/M/,"",$4); print $4}')
        if [[ $AVAILABLE_DISK -lt 10240 ]]; then
            print_warning "Available disk space is ${AVAILABLE_DISK}MB. You may need more space for optimal performance."
        fi
    fi

    print_success "Prerequisites check completed"
}

# Setup environment file
setup_environment() {
    print_status "Setting up environment configuration..."

    if [[ ! -f .env ]]; then
        if [[ -f .env.example ]]; then
            cp .env.example .env
            print_success "Created .env file from template"
        else
            print_error ".env.example file not found"
            exit 1
        fi
    else
        print_status ".env file already exists"
    fi

    # Check for OpenAI API key
    if ! grep -q "^OPENAI_API_KEY=sk-" .env 2>/dev/null; then
        print_warning "OpenAI API key not configured in .env file"
        echo ""
        echo "To enable AI features, you need to set your OpenAI API key:"
        echo "1. Get an API key from: https://platform.openai.com/api-keys"
        echo "2. Edit .env file and set: OPENAI_API_KEY=your_key_here"
        echo ""
        read -p "Do you want to set it now? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            read -p "Enter your OpenAI API key: " OPENAI_KEY
            if [[ ! -z "$OPENAI_KEY" ]]; then
                sed -i.bak "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$OPENAI_KEY/" .env
                print_success "OpenAI API key configured"
            fi
        else
            print_warning "AI features will be limited without OpenAI API key"
        fi
    fi

    # Configure for minimal mode
    if [[ "$MINIMAL_MODE" == "true" ]]; then
        print_status "Configuring for minimal resource usage..."
        sed -i.bak 's/LOG_LEVEL=INFO/LOG_LEVEL=WARNING/' .env
        sed -i.bak 's/AI_PROCESSOR_MEMORY_LIMIT=2048m/AI_PROCESSOR_MEMORY_LIMIT=1024m/' .env
        sed -i.bak 's/ELASTICSEARCH_MEMORY_LIMIT=2048m/ELASTICSEARCH_MEMORY_LIMIT=512m/' .env
    fi
}

# Build and start services
start_services() {
    print_status "Building Docker images..."
    
    if [[ "$MINIMAL_MODE" == "true" ]]; then
        print_status "Starting services in minimal resource mode..."
        docker-compose -f docker-compose.yml -f docker-compose.minimal.yml build --parallel
        
        if [[ "$DEMO_MODE" == "true" ]]; then
            docker-compose -f docker-compose.yml -f docker-compose.minimal.yml --profile demo up -d
        else
            docker-compose -f docker-compose.yml -f docker-compose.minimal.yml up -d
        fi
    else
        docker-compose build --parallel
        
        if [[ "$DEMO_MODE" == "true" ]]; then
            docker-compose --profile demo up -d
        else
            docker-compose up -d
        fi
    fi

    print_success "Services started successfully"
}

# Wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for critical services
    local max_attempts=60
    local attempt=0
    
    while [[ $attempt -lt $max_attempts ]]; do
        if curl -sf http://localhost:8000/health >/dev/null 2>&1; then
            break
        fi
        
        ((attempt++))
        if [[ $((attempt % 10)) -eq 0 ]]; then
            print_status "Still waiting for services... (${attempt}/${max_attempts})"
        fi
        
        sleep 5
    done
    
    if [[ $attempt -eq $max_attempts ]]; then
        print_warning "Services might not be fully ready yet. You can check status with: docker-compose ps"
    else
        print_success "Services are ready!"
    fi
}

# Generate demo data
generate_demo_data() {
    if [[ "$DEMO_MODE" == "true" ]]; then
        print_status "Generating demo data..."
        
        # Wait a bit more for sample app to be ready
        sleep 10
        
        # Generate some demo activity
        for i in {1..5}; do
            curl -sf -X POST http://localhost:8080/simulate >/dev/null 2>&1 || true
            sleep 2
        done
        
        print_success "Demo data generated"
    fi
}

# Print access information
print_access_info() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🎉 System Ready! 🎉                      ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Access your observability system:"
    echo ""
    echo "🤖 Chat Interface (AI-powered):  http://localhost:3000"
    echo "📊 Grafana Dashboards:          http://localhost:3001 (admin/admin)"
    echo "📈 Prometheus Metrics:          http://localhost:9090"
    echo "🔍 Jaeger Tracing:              http://localhost:16686"
    echo "🔌 Chat API:                    http://localhost:8000"
    
    if [[ "$DEMO_MODE" == "true" ]]; then
        echo "🎮 Sample Application:          http://localhost:8080"
    fi
    
    echo ""
    echo "💡 Quick Tips:"
    echo "• Try asking: 'Show me system performance overview'"
    echo "• Use 'make logs' to view service logs"
    echo "• Use 'make health' to check service health"
    echo "• Use 'make status' to see running services"
    
    if [[ "$DEMO_MODE" == "true" ]]; then
        echo "• Visit http://localhost:8080/simulate to generate demo traffic"
    fi
    
    echo ""
    echo "📚 Documentation: See README.md and SETUP.md for more details"
    echo ""
}

# Check service status
check_status() {
    print_status "Checking service status..."
    
    if command_exists docker-compose; then
        docker-compose ps
    else
        docker compose ps
    fi
    
    echo ""
    print_status "Service health checks:"
    
    # Check each service
    local services=(
        "localhost:3000;Chat Frontend"
        "localhost:8000;Chat API"
        "localhost:9090;Prometheus"
        "localhost:9200;Elasticsearch"
        "localhost:16686;Jaeger"
    )
    
    if [[ "$DEMO_MODE" == "true" ]]; then
        services+=("localhost:8080;Sample App")
    fi
    
    for service in "${services[@]}"; do
        IFS=';' read -r url name <<< "$service"
        if curl -sf "http://$url" >/dev/null 2>&1; then
            print_success "$name is responding"
        else
            print_warning "$name is not responding"
        fi
    done
}

# Cleanup function
cleanup() {
    print_status "Cleaning up..."
    docker-compose down >/dev/null 2>&1 || true
}

# Main function
main() {
    # Set up signal handlers
    trap cleanup EXIT

    print_banner
    
    parse_args "$@"
    
    # Print configuration
    print_status "Configuration:"
    echo "  • Minimal mode: $MINIMAL_MODE"
    echo "  • Demo mode: $DEMO_MODE"
    echo "  • Skip checks: $SKIP_CHECKS"
    echo ""
    
    check_prerequisites
    setup_environment
    start_services
    wait_for_services
    generate_demo_data
    check_status
    print_access_info
    
    # Remove cleanup trap since we want services to keep running
    trap - EXIT
}

# Run main function with all arguments
main "$@"