#!/bin/bash

# Alopecosa Fabrilis Web Crawler - Docker Runner
# This script makes it easy to run the crawler in different modes

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}🕷️  Alopecosa Fabrilis Web Crawler${NC}"
    echo "=================================="
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to create .env file if it doesn't exist
create_env_file() {
    if [ ! -f .env ]; then
        print_status "Creating .env file with default values..."
        cat > .env << EOF
# Flask Configuration
FLASK_SECRET_KEY=$(openssl rand -hex 32)
FLASK_ENV=production

# OpenAI API Configuration (optional - leave empty to disable AI features)
OPENAI_API_KEY=

# AI Model Settings
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
OPENAI_MAX_TOKENS=400
OPENAI_TEMPERATURE=0.2

# AI Thresholds
AI_RELEVANCE_THRESHOLD=0.6
AI_QUALITY_THRESHOLD=0.7
AI_SIMILARITY_THRESHOLD=0.9

# Rate Limiting
OPENAI_RPM_LIMIT=60
OPENAI_CONCURRENT_LIMIT=5

# Crawler Settings
ALOPECOSA_USER_AGENT=Alopecosa-Fabrilis-Crawler/1.0
EOF
        print_status ".env file created. Please edit it to add your OpenAI API key if needed."
    fi
}

# Function to create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    mkdir -p data crawl_results logs
}

# Function to run in development mode
run_dev() {
    print_header
    print_status "Starting in development mode..."
    print_warning "This mode is for development only. Use --prod for production."
    
    check_docker
    create_env_file
    create_directories
    
    docker-compose up --build
}

# Function to run in production mode
run_prod() {
    print_header
    print_status "Starting in production mode with nginx reverse proxy..."
    
    check_docker
    create_env_file
    create_directories
    
    docker-compose --profile production up --build -d
    print_status "Production stack started!"
    print_status "Web interface: http://localhost"
    print_status "Direct access: http://localhost:5000"
}

# Function to stop containers
stop_containers() {
    print_status "Stopping containers..."
    docker-compose down
    print_status "Containers stopped."
}

# Function to view logs
view_logs() {
    print_status "Showing logs..."
    docker-compose logs -f
}

# Function to clean up
cleanup() {
    print_warning "This will remove all containers, images, and data. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Cleaning up..."
        docker-compose down -v --rmi all
        docker system prune -f
        print_status "Cleanup complete."
    else
        print_status "Cleanup cancelled."
    fi
}

# Function to show status
show_status() {
    print_status "Container status:"
    docker-compose ps
    echo
    print_status "Resource usage:"
    docker stats --no-stream
}

# Function to show help
show_help() {
    print_header
    echo "Usage: $0 [OPTION]"
    echo
    echo "Options:"
    echo "  dev, --dev          Run in development mode (with logs)"
    echo "  prod, --prod        Run in production mode (with nginx)"
    echo "  stop, --stop        Stop all containers"
    echo "  logs, --logs        View container logs"
    echo "  status, --status    Show container status and resource usage"
    echo "  cleanup, --cleanup  Remove all containers and images"
    echo "  help, --help        Show this help message"
    echo
    echo "Examples:"
    echo "  $0 dev              # Start development mode"
    echo "  $0 prod             # Start production mode"
    echo "  $0 logs             # View logs"
    echo "  $0 stop             # Stop containers"
    echo
    echo "Environment:"
    echo "  Create a .env file to configure the crawler"
    echo "  See .env.example for available options"
}

# Main script logic
case "${1:-help}" in
    dev|--dev)
        run_dev
        ;;
    prod|--prod)
        run_prod
        ;;
    stop|--stop)
        stop_containers
        ;;
    logs|--logs)
        view_logs
        ;;
    status|--status)
        show_status
        ;;
    cleanup|--cleanup)
        cleanup
        ;;
    help|--help|*)
        show_help
        ;;
esac

