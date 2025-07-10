#!/bin/bash

# Verification script for AI-Powered Observability System
# Checks if all required files are present and provides setup summary

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║          AI-Powered Observability System Verification        ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
}

check_file() {
    if [[ -f "$1" ]]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1 (missing)"
        return 1
    fi
}

check_dir() {
    if [[ -d "$1" ]]; then
        echo -e "${GREEN}✓${NC} $1/"
        return 0
    else
        echo -e "${RED}✗${NC} $1/ (missing)"
        return 1
    fi
}

print_header

echo "Checking core files..."
echo "====================="

# Core files
missing_files=0

check_file "README.md" || ((missing_files++))
check_file "SETUP.md" || ((missing_files++))
check_file "docker-compose.yml" || ((missing_files++))
check_file "docker-compose.minimal.yml" || ((missing_files++))
check_file ".env.example" || ((missing_files++))
check_file "Makefile" || ((missing_files++))
check_file "start.sh" || ((missing_files++))

echo ""
echo "Checking configuration files..."
echo "==============================="

# Configuration files
check_dir "config" || ((missing_files++))
check_file "config/prometheus.yml" || ((missing_files++))
check_file "config/otelcol.yml" || ((missing_files++))
check_file "config/fluent.conf" || ((missing_files++))
check_file "config/ai-config.yml" || ((missing_files++))

echo ""
echo "Checking service directories..."
echo "==============================="

# Service directories
check_dir "services" || ((missing_files++))
check_dir "services/ai-processor" || ((missing_files++))
check_dir "services/chat-api" || ((missing_files++))
check_dir "services/chat-frontend" || ((missing_files++))
check_dir "services/fluentd" || ((missing_files++))
check_dir "services/sample-app" || ((missing_files++))

echo ""
echo "Checking AI Processor service..."
echo "================================"

check_file "services/ai-processor/Dockerfile" || ((missing_files++))
check_file "services/ai-processor/requirements.txt" || ((missing_files++))
check_file "services/ai-processor/main.py" || ((missing_files++))
check_file "services/ai-processor/src/config.py" || ((missing_files++))

echo ""
echo "Checking Chat API service..."
echo "==========================="

check_file "services/chat-api/Dockerfile" || ((missing_files++))
check_file "services/chat-api/requirements.txt" || ((missing_files++))
check_file "services/chat-api/main.py" || ((missing_files++))

echo ""
echo "Checking Chat Frontend service..."
echo "================================"

check_file "services/chat-frontend/Dockerfile" || ((missing_files++))
check_file "services/chat-frontend/package.json" || ((missing_files++))
check_file "services/chat-frontend/nginx.conf" || ((missing_files++))
check_file "services/chat-frontend/src/App.js" || ((missing_files++))
check_file "services/chat-frontend/src/index.js" || ((missing_files++))
check_file "services/chat-frontend/src/components/ChatInterface.js" || ((missing_files++))
check_file "services/chat-frontend/src/components/Navigation.js" || ((missing_files++))
check_file "services/chat-frontend/src/components/Dashboard.js" || ((missing_files++))
check_file "services/chat-frontend/src/components/SystemStatus.js" || ((missing_files++))
check_file "services/chat-frontend/public/index.html" || ((missing_files++))

echo ""
echo "Checking Fluentd service..."
echo "=========================="

check_file "services/fluentd/Dockerfile" || ((missing_files++))
check_file "services/fluentd/elasticsearch_template.json" || ((missing_files++))

echo ""
echo "Checking Sample App service..."
echo "============================="

check_file "services/sample-app/Dockerfile" || ((missing_files++))
check_file "services/sample-app/requirements.txt" || ((missing_files++))
check_file "services/sample-app/app.py" || ((missing_files++))

echo ""
echo "Summary"
echo "======="

if [[ $missing_files -eq 0 ]]; then
    echo -e "${GREEN}✅ All files are present! System is ready to deploy.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Set your OpenAI API key: cp .env.example .env && edit .env"
    echo "2. Start the system: ./start.sh --demo"
    echo "3. Open http://localhost:3000 to access the chat interface"
    echo ""
    echo "For minimal resource usage: ./start.sh --minimal"
    echo "For detailed setup guide: See SETUP.md"
else
    echo -e "${RED}❌ Found $missing_files missing files.${NC}"
    echo ""
    echo "Please ensure all required files are present before deploying."
fi

echo ""
echo "System Requirements:"
echo "==================="
echo "• Docker 20.10+ and Docker Compose 2.0+"
echo "• Minimum 4 cores, 8GB RAM, 20GB disk"
echo "• OpenAI API key (for AI features)"
echo "• Internet connection"
echo ""
echo "For low-resource systems (4GB RAM), use: ./start.sh --minimal"
echo ""
echo "Documentation:"
echo "• README.md - Quick start and overview"
echo "• SETUP.md - Detailed installation guide"
echo "• start.sh --help - Script usage"
echo ""

if [[ -x "start.sh" ]]; then
    echo -e "${GREEN}✓${NC} start.sh is executable"
else
    echo -e "${YELLOW}⚠${NC} Making start.sh executable..."
    chmod +x start.sh
fi

echo ""
echo "🚀 Ready to deploy? Run: ./start.sh --demo"
echo ""