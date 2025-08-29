#!/bin/bash

# Alopecosa Fabrilis Web Crawler - Cloudflare Deployment Script
# This script automates the deployment process to Cloudflare Workers

set -e  # Exit on any error

echo "🕷️  Deploying Alopecosa Fabrilis Web Crawler to Cloudflare..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if wrangler is installed
check_wrangler() {
    if ! command -v wrangler &> /dev/null; then
        print_error "Wrangler CLI is not installed. Please install it first:"
        echo "npm install -g wrangler"
        exit 1
    fi
    print_success "Wrangler CLI found"
}

# Check if user is logged in to Cloudflare
check_login() {
    if ! wrangler whoami &> /dev/null; then
        print_warning "You are not logged in to Cloudflare. Please login first:"
        echo "wrangler login"
        exit 1
    fi
    print_success "Logged in to Cloudflare"
}

# Install dependencies
install_deps() {
    print_status "Installing Python dependencies..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Dependencies installed"
    else
        print_warning "No requirements.txt found, skipping dependency installation"
    fi
}

# Deploy to Cloudflare
deploy() {
    local environment=$1
    
    if [ "$environment" = "production" ]; then
        print_status "Deploying to PRODUCTION environment..."
        wrangler deploy --env production
    elif [ "$environment" = "staging" ]; then
        print_status "Deploying to STAGING environment..."
        wrangler deploy --env staging
    else
        print_status "Deploying to default environment..."
        wrangler deploy
    fi
    
    print_success "Deployment completed!"
}

# Main deployment logic
main() {
    local environment=${1:-default}
    
    print_status "Starting deployment process..."
    
    # Pre-deployment checks
    check_wrangler
    check_login
    install_deps
    
    # Deploy
    deploy "$environment"
    
    print_success "🎉 Alopecosa Fabrilis Web Crawler deployed successfully!"
    
    if [ "$environment" = "production" ]; then
        echo ""
        echo "🌐 Your crawler is now live at:"
        echo "   https://alopecosa-crawler-prod.your-subdomain.workers.dev"
    elif [ "$environment" = "staging" ]; then
        echo ""
        echo "🌐 Your crawler is now live at:"
        echo "   https://alopecosa-crawler-staging.your-subdomain.workers.dev"
    else
        echo ""
        echo "🌐 Your crawler is now live at:"
        echo "   https://alopecosa-crawler.your-subdomain.workers.dev"
    fi
    
    echo ""
    echo "📚 Next steps:"
    echo "   1. Test your deployment by visiting the URL above"
    echo "   2. Configure custom domains in your Cloudflare dashboard"
    echo "   3. Set up environment variables if needed"
    echo "   4. Monitor performance in Cloudflare Analytics"
}

# Parse command line arguments
case "${1:-}" in
    "production"|"prod")
        main "production"
        ;;
    "staging"|"stage")
        main "staging"
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [environment]"
        echo ""
        echo "Environments:"
        echo "  default   - Deploy to default environment"
        echo "  staging   - Deploy to staging environment"
        echo "  production - Deploy to production environment"
        echo ""
        echo "Examples:"
        echo "  $0              # Deploy to default"
        echo "  $0 staging      # Deploy to staging"
        echo "  $0 production   # Deploy to production"
        ;;
    *)
        main "default"
        ;;
esac
