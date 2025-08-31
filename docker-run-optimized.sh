#!/bin/bash

# Alopecosa Fabrilis Web Crawler - Optimized Docker Runner
# Performance-focused version with optimized settings

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
    echo -e "${BLUE}🕷️  Alopecosa Fabrilis Web Crawler (Optimized)${NC}"
    echo "================================================"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to check system resources
check_resources() {
    print_status "Checking system resources..."
    
    # Check available memory
    if command -v free > /dev/null 2>&1; then
        available_mem=$(free -m | awk 'NR==2{printf "%.0f", $7/1024}')
        print_status "Available memory: ${available_mem}GB"
        
        if [ "$available_mem" -lt 2 ]; then
            print_warning "Low memory detected. Consider closing other applications."
        fi
    fi
    
    # Check CPU cores
    cpu_cores=$(nproc)
    print_status "CPU cores: $cpu_cores"
    
    # Check disk space
    disk_space=$(df -h . | awk 'NR==2{print $4}')
    print_status "Available disk space: $disk_space"
}

# Function to create .env file if it doesn't exist
create_env_file() {
    if [ ! -f .env ]; then
        print_status "Creating .env file with optimized values..."
        cat > .env << EOF
# Flask Configuration
FLASK_SECRET_KEY=$(openssl rand -hex 32)
FLASK_ENV=production

# Performance Optimizations
PYTHONOPTIMIZE=1
PYTHONHASHSEED=random
PYTHONUNBUFFERED=1

# OpenAI API Configuration (optional)
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
        print_status ".env file created with optimized settings."
    fi
}

# Function to create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    mkdir -p data crawl_results logs
}

# Function to run in optimized development mode
run_dev_optimized() {
    print_header
    print_status "Starting in optimized development mode..."
    print_warning "This mode is for development only. Use --prod for production."
    
    check_docker
    check_resources
    create_env_file
    create_directories
    
    # Use development override with performance settings
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
}

# Function to run in optimized production mode
run_prod_optimized() {
    print_header
    print_status "Starting in optimized production mode..."
    
    check_docker
    check_resources
    create_env_file
    create_directories
    
    # Use optimized compose file
    docker-compose -f docker-compose.optimized.yml --profile production up --build -d
    print_status "Optimized production stack started!"
    print_status "Web interface: http://localhost"
    print_status "Direct access: http://localhost:5000"
    print_status "Performance monitoring: docker stats"
}

# Function to run performance benchmark
run_benchmark() {
    print_header
    print_status "Running performance benchmark..."
    
    # Start the optimized container
    docker-compose -f docker-compose.optimized.yml up --build -d
    
    # Wait for startup
    sleep 10
    
    # Run basic performance test
    print_status "Testing response times..."
    
    # Test health endpoint
    start_time=$(date +%s.%N)
    curl -s http://localhost:5000/api/health > /dev/null
    end_time=$(date +%s.%N)
    
    response_time=$(echo "$end_time - $start_time" | bc -l)
    print_status "Health endpoint response time: ${response_time}s"
    
    # Show resource usage
    print_status "Container resource usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
    
    # Stop containers
    docker-compose -f docker-compose.optimized.yml down
}

# Function to stop containers
stop_containers() {
    print_status "Stopping containers..."
    docker-compose down
    docker-compose -f docker-compose.optimized.yml down
    print_status "Containers stopped."
}

# Function to view logs
view_logs() {
    print_status "Showing logs..."
    docker-compose logs -f
}

# Function to show performance stats
show_stats() {
    print_status "Container performance statistics:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
}

# Function to clean up
cleanup() {
    print_warning "This will remove all containers, images, and data. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Cleaning up..."
        docker-compose down -v --rmi all
        docker-compose -f docker-compose.optimized.yml down -v --rmi all
        docker system prune -f
        print_status "Cleanup complete."
    else
        print_status "Cleanup cancelled."
    fi
}

# Function to show help
show_help() {
    print_header
    echo "Usage: $0 [OPTION]"
    echo
    echo "Optimized Options:"
    echo "  dev, --dev          Run in optimized development mode"
    echo "  prod, --prod        Run in optimized production mode"
    echo "  benchmark, --bench   Run performance benchmark"
    echo "  stop, --stop         Stop all containers"
    echo "  logs, --logs         View container logs"
    echo "  stats, --stats       Show performance statistics"
    echo "  cleanup, --cleanup   Remove all containers and images"
    echo "  help, --help         Show this help message"
    echo
    echo "Performance Features:"
    echo "  • Multi-stage Docker build"
    echo "  • Optimized resource allocation"
    echo "  • Shared memory usage"
    echo "  • Increased worker processes"
    echo "  • Better caching strategies"
    echo
    echo "Examples:"
    echo "  $0 dev               # Start optimized development mode"
    echo "  $0 prod              # Start optimized production mode"
    echo "  $0 benchmark          # Run performance test"
    echo "  $0 stats              # Show resource usage"
    echo
    echo "Environment:"
    echo "  Optimized .env file will be created automatically"
    echo "  Performance settings are pre-configured"
}

# Main script logic
case "${1:-help}" in
    dev|--dev)
        run_dev_optimized
        ;;
    prod|--prod)
        run_prod_optimized
        ;;
    benchmark|--bench)
        run_benchmark
        ;;
    stop|--stop)
        stop_containers
        ;;
    logs|--logs)
        view_logs
        ;;
    stats|--stats)
        show_stats
        ;;
    cleanup|--cleanup)
        cleanup
        ;;
    help|--help|*)
        show_help
        ;;
esac
