#!/bin/bash

# 🔧 Quick Chat Fix Script
# Automatically diagnoses and fixes common chat blocking issues

set -e

echo "🔧 Chat Interface Quick Fix Tool"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ️${NC} $1"
}

# Check if Docker is running
check_docker() {
    echo "🐳 Checking Docker..."
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_status "Docker is running"
}

# Check if docker-compose.yml exists
check_compose_file() {
    echo "📄 Checking Docker Compose file..."
    if [ ! -f "docker-compose.yml" ]; then
        print_error "docker-compose.yml not found. Please run from the project root directory."
        exit 1
    fi
    print_status "Docker Compose file found"
}

# Check service status
check_services() {
    echo "🔍 Checking service status..."
    
    # Get service status
    status=$(docker-compose ps --format "table {{.Name}}\t{{.State}}" 2>/dev/null || echo "No services")
    
    if echo "$status" | grep -q "Up"; then
        print_status "Some services are running"
    else
        print_warning "No services are currently running"
        return 1
    fi
    
    # Check specific chat services
    for service in chat-frontend chat-api ai-processor; do
        if docker-compose ps $service 2>/dev/null | grep -q "Up"; then
            print_status "$service is running"
        else
            print_warning "$service is not running"
        fi
    done
}

# Test API connectivity
test_api() {
    echo "🌐 Testing API connectivity..."
    
    # Wait a moment for services to be ready
    sleep 5
    
    # Test Chat API
    if curl -f -s http://localhost:8000/health > /dev/null 2>&1; then
        print_status "Chat API is responding"
    else
        print_warning "Chat API is not responding"
        return 1
    fi
    
    # Test AI Processor  
    if curl -f -s http://localhost:5000/health > /dev/null 2>&1; then
        print_status "AI Processor is responding"
    else
        print_warning "AI Processor is not responding"
        return 1
    fi
    
    # Test Frontend
    if curl -f -s http://localhost:3000 > /dev/null 2>&1; then
        print_status "Frontend is accessible"
    else
        print_warning "Frontend is not accessible"
        return 1
    fi
}

# Check environment configuration
check_environment() {
    echo "🔧 Checking environment configuration..."
    
    if [ -f ".env" ]; then
        print_status ".env file exists"
        
        # Check for OpenAI API key
        if grep -q "OPENAI_API_KEY=" .env && ! grep -q "OPENAI_API_KEY=$" .env; then
            print_status "OpenAI API key is configured"
        else
            print_warning "OpenAI API key is missing or empty"
            print_info "Please set OPENAI_API_KEY in your .env file"
            return 1
        fi
    else
        print_warning ".env file not found"
        print_info "Creating .env file from template..."
        
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_status "Created .env file from template"
            print_warning "Please edit .env file and set your OPENAI_API_KEY"
            return 1
        else
            print_error ".env.example not found. Please create .env file manually."
            return 1
        fi
    fi
}

# Fix function - restart services
fix_restart_services() {
    echo "🔄 Restarting chat services..."
    docker-compose restart chat-api ai-processor chat-frontend
    print_status "Services restarted"
}

# Fix function - rebuild services
fix_rebuild_services() {
    echo "🔨 Rebuilding and restarting services..."
    docker-compose down
    docker-compose build chat-api ai-processor chat-frontend
    docker-compose up -d
    print_status "Services rebuilt and restarted"
}

# Fix function - complete reset
fix_complete_reset() {
    echo "💥 Performing complete reset..."
    docker-compose down -v
    docker-compose build --no-cache
    docker-compose up -d
    print_status "Complete reset performed"
}

# Fix function - check ports
fix_port_conflicts() {
    echo "🔌 Checking for port conflicts..."
    
    ports=(3000 8000 5000 9090 9200)
    conflicts=false
    
    for port in "${ports[@]}"; do
        if lsof -i :$port > /dev/null 2>&1; then
            pid=$(lsof -t -i :$port)
            process=$(ps -p $pid -o comm= 2>/dev/null || echo "unknown")
            if [[ "$process" != *"docker"* ]]; then
                print_warning "Port $port is in use by process $process (PID: $pid)"
                conflicts=true
            fi
        fi
    done
    
    if [ "$conflicts" = true ]; then
        print_info "Some ports are in use by non-Docker processes"
        print_info "You may need to stop these processes or change ports in docker-compose.yml"
        return 1
    else
        print_status "No port conflicts detected"
    fi
}

# Main diagnosis and fix routine
main() {
    echo "Starting chat diagnosis..."
    echo
    
    # Basic checks
    check_docker
    check_compose_file
    
    # Environment check
    if ! check_environment; then
        echo
        print_info "Please fix environment configuration and run the script again"
        exit 1
    fi
    
    # Check for port conflicts
    fix_port_conflicts
    
    # Check services
    if ! check_services; then
        echo
        print_info "Starting services..."
        docker-compose up -d
        sleep 10
    fi
    
    # Test connectivity
    if ! test_api; then
        echo
        print_info "API tests failed. Attempting fixes..."
        
        # Try restart first
        fix_restart_services
        sleep 10
        
        if ! test_api; then
            print_info "Restart didn't help. Trying rebuild..."
            fix_rebuild_services
            sleep 15
            
            if ! test_api; then
                print_info "Rebuild didn't help. Trying complete reset..."
                fix_complete_reset
                sleep 20
                
                if ! test_api; then
                    print_error "All automated fixes failed. Please check the logs:"
                    echo "  docker-compose logs chat-api"
                    echo "  docker-compose logs ai-processor"
                    echo "  docker-compose logs chat-frontend"
                    exit 1
                fi
            fi
        fi
    fi
    
    # Final test
    echo
    echo "🎉 Final verification..."
    
    # Test end-to-end chat functionality
    print_info "Testing chat functionality..."
    response=$(curl -s -X POST http://localhost:8000/api/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "test", "conversation_id": "fix-test"}' 2>/dev/null || echo "failed")
    
    if echo "$response" | grep -q "response\|message\|content"; then
        print_status "Chat functionality is working!"
    else
        print_warning "Chat API responded but functionality may be limited"
        print_info "Response: $response"
    fi
    
    echo
    echo "🚀 Chat System Status:"
    print_status "Chat Interface: http://localhost:3000"
    print_status "Chat API: http://localhost:8000"
    print_status "AI Processor: http://localhost:5000"
    
    echo
    print_info "If you're still experiencing issues:"
    print_info "1. Check browser console for JavaScript errors (F12)"
    print_info "2. Try incognito/private browsing mode"
    print_info "3. Clear browser cache and cookies"
    print_info "4. Check the troubleshooting guide: docs/CHAT_TROUBLESHOOTING.md"
    
    echo
    print_status "Chat fix completed! Try accessing http://localhost:3000"
}

# Run the main function
main "$@"