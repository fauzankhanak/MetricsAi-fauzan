#!/bin/bash

# 🔑 OpenAI API Key Quick Setup Script
# Helps you configure OpenAI API key for the AI observability system

set -e

echo "🔑 OpenAI API Key Setup for AI Observability System"
echo "=================================================="
echo

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️ $1${NC}"
}

# Check if .env file exists
setup_env_file() {
    print_step "Setting up environment file..."
    
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_success "Created .env file from template"
        else
            print_error ".env.example file not found. Please ensure you're in the project root directory."
            exit 1
        fi
    else
        print_success ".env file already exists"
    fi
}

# Prompt user for OpenAI API key
get_api_key() {
    print_step "OpenAI API Key Configuration"
    echo
    print_info "You need an OpenAI API key to use the AI features."
    print_info "📖 For detailed instructions, see: docs/OPENAI_API_SETUP.md"
    echo
    
    # Check if key already exists in .env
    if grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
        current_key=$(grep "OPENAI_API_KEY=" .env | cut -d'=' -f2)
        if [[ $current_key != *"your-actual-openai-api-key-here"* ]] && [[ $current_key == sk-* ]]; then
            print_success "OpenAI API key already configured"
            echo -e "Current key: ${current_key:0:20}..."
            echo
            read -p "Do you want to update it? (y/N): " update_key
            if [[ $update_key != [Yy]* ]]; then
                return 0
            fi
        fi
    fi
    
    echo -e "${BLUE}🔗 To get your OpenAI API key:${NC}"
    echo "1. Go to: https://platform.openai.com/api-keys"
    echo "2. Sign up or log in to your OpenAI account"
    echo "3. Click 'Create new secret key'"
    echo "4. Copy the key (starts with sk-proj- or sk-)"
    echo
    
    read -p "Do you have an OpenAI API key? (y/N): " has_key
    
    if [[ $has_key == [Yy]* ]]; then
        echo
        read -p "Please paste your OpenAI API key: " api_key
        
        # Validate API key format
        if [[ $api_key =~ ^sk-[a-zA-Z0-9-_]+$ ]]; then
            # Update .env file
            if grep -q "OPENAI_API_KEY=" .env; then
                sed -i.bak "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$api_key/" .env
            else
                echo "OPENAI_API_KEY=$api_key" >> .env
            fi
            print_success "API key configured successfully"
        else
            print_error "Invalid API key format. OpenAI keys should start with 'sk-'"
            print_info "Please check your key and try again."
            exit 1
        fi
    else
        echo
        print_warning "You need an OpenAI API key to use AI features."
        print_info "Opening setup guide..."
        echo
        echo -e "${BLUE}Quick setup steps:${NC}"
        echo "1. Visit: https://platform.openai.com/api-keys"
        echo "2. Create account and add billing info (required)"
        echo "3. Create new secret key"
        echo "4. Run this script again with your key"
        echo
        print_info "💰 Cost estimate: ~\$2-10/month for typical usage"
        print_info "📖 Full guide: docs/OPENAI_API_SETUP.md"
        
        exit 0
    fi
}

# Test API key
test_api_key() {
    print_step "Testing OpenAI API key..."
    
    # Get API key from .env
    api_key=$(grep "OPENAI_API_KEY=" .env | cut -d'=' -f2)
    
    if [ -z "$api_key" ] || [[ $api_key == *"your-actual-openai-api-key-here"* ]]; then
        print_error "API key not configured properly"
        return 1
    fi
    
    # Test API key
    response=$(curl -s -w "%{http_code}" -o /tmp/openai_test.json \
        -H "Authorization: Bearer $api_key" \
        -H "Content-Type: application/json" \
        https://api.openai.com/v1/models)
    
    http_code=$(echo "$response" | tail -c 4)
    
    if [ "$http_code" = "200" ]; then
        print_success "API key is valid and working!"
        
        # Show available models
        if command -v jq >/dev/null 2>&1; then
            echo
            print_info "Available models:"
            jq -r '.data[] | select(.id | contains("gpt")) | "  - " + .id' /tmp/openai_test.json 2>/dev/null | head -5
        fi
    else
        print_error "API key validation failed (HTTP $http_code)"
        
        case $http_code in
            "401")
                print_info "Invalid API key. Please check your key."
                ;;
            "429")
                print_info "Rate limit exceeded or quota reached."
                print_info "Check your billing: https://platform.openai.com/account/billing"
                ;;
            "403")
                print_info "Access denied. Check your API key permissions."
                ;;
            *)
                print_info "Unexpected error. Check your internet connection."
                ;;
        esac
        
        return 1
    fi
    
    # Cleanup
    rm -f /tmp/openai_test.json
}

# Configure model settings
configure_model() {
    print_step "Configuring AI model settings..."
    
    echo
    echo -e "${BLUE}Choose your AI model:${NC}"
    echo "1. gpt-3.5-turbo (Cheapest, ~\$2-5/month)"
    echo "2. gpt-4o-mini (Best value, ~\$5-10/month)" 
    echo "3. gpt-4o (Highest quality, ~\$15-30/month)"
    echo
    
    read -p "Select model (1-3, default: 1): " model_choice
    
    case $model_choice in
        1|"")
            model="gpt-3.5-turbo"
            max_tokens="1024"
            ;;
        2)
            model="gpt-4o-mini"
            max_tokens="1024"
            ;;
        3)
            model="gpt-4o"
            max_tokens="2048"
            ;;
        *)
            print_warning "Invalid choice, using gpt-3.5-turbo"
            model="gpt-3.5-turbo"
            max_tokens="1024"
            ;;
    esac
    
    # Update .env file
    if grep -q "OPENAI_MODEL=" .env; then
        sed -i.bak "s/OPENAI_MODEL=.*/OPENAI_MODEL=$model/" .env
    else
        echo "OPENAI_MODEL=$model" >> .env
    fi
    
    if grep -q "OPENAI_MAX_TOKENS=" .env; then
        sed -i.bak "s/OPENAI_MAX_TOKENS=.*/OPENAI_MAX_TOKENS=$max_tokens/" .env
    else
        echo "OPENAI_MAX_TOKENS=$max_tokens" >> .env
    fi
    
    print_success "Model configured: $model (max tokens: $max_tokens)"
}

# Restart services to apply new configuration
restart_services() {
    print_step "Applying configuration..."
    
    if command -v docker-compose >/dev/null 2>&1; then
        if docker-compose ps >/dev/null 2>&1; then
            print_info "Restarting AI services to apply new configuration..."
            docker-compose restart ai-processor chat-api 2>/dev/null || {
                print_info "Services not running yet. Configuration will be applied on next startup."
            }
        else
            print_info "Services not running. Configuration ready for next startup."
        fi
    else
        print_info "Docker Compose not found. Manual restart may be required."
    fi
}

# Show completion summary
show_completion() {
    echo
    echo "🎉 OpenAI API Setup Complete!"
    echo "============================="
    echo
    print_success "✅ OpenAI API key configured"
    print_success "✅ AI model settings optimized"
    print_success "✅ Environment variables updated"
    echo
    print_info "Next steps:"
    echo "1. Start the system: ./start.sh --demo"
    echo "2. Open chat interface: http://localhost:3000"
    echo "3. Test with: 'Hello, test my AI connection'"
    echo
    print_info "💰 Monitor your usage: https://platform.openai.com/usage"
    print_info "📖 Full documentation: docs/OPENAI_API_SETUP.md"
    echo
}

# Main execution
main() {
    # Check if we're in the right directory
    if [ ! -f "docker-compose.yml" ]; then
        print_error "Please run this script from the project root directory"
        exit 1
    fi
    
    setup_env_file
    get_api_key
    
    if [ $? -eq 0 ]; then
        test_api_key
        if [ $? -eq 0 ]; then
            configure_model
            restart_services
            show_completion
        else
            print_error "API key test failed. Please check your key and try again."
            print_info "Run: $0 to retry"
            exit 1
        fi
    fi
}

# Handle script arguments
case "${1:-}" in
    --help|-h)
        echo "Usage: $0 [--help]"
        echo
        echo "This script helps you set up OpenAI API key for the AI observability system."
        echo
        echo "Options:"
        echo "  --help    Show this help message"
        echo
        echo "For detailed setup instructions, see: docs/OPENAI_API_SETUP.md"
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac