# 🐳 Docker Setup for Alopecosa Fabrilis Web Crawler

This guide explains how to run the Alopecosa Fabrilis Web Crawler using Docker for easy deployment and consistent environments.

## 🚀 Quick Start

### Prerequisites
- Docker installed and running
- Docker Compose installed
- At least 2GB of available RAM

### 1. Clone and Navigate
```bash
git clone <your-repo-url>
cd -Alopecosa-Fabrilis-Web-Crawler
```

### 2. Run with Simple Script
```bash
# Development mode (with logs)
./docker-run.sh dev

# Production mode (with nginx)
./docker-run.sh prod

# Stop containers
./docker-run.sh stop
```

## 📋 Docker Files Overview

### `Dockerfile`
- **Base Image**: Python 3.11-slim for smaller size
- **Security**: Non-root user for container security
- **Dependencies**: Installs system and Python packages
- **Health Check**: Monitors application health
- **Port**: Exposes port 5000

### `docker-compose.yml`
- **Services**: Main crawler + optional nginx proxy
- **Environment**: Configurable via .env file
- **Volumes**: Persistent data storage
- **Resources**: Memory and CPU limits
- **Networking**: Internal communication

### `nginx.conf`
- **Reverse Proxy**: Routes traffic to crawler
- **Security Headers**: XSS protection, frame options
- **Rate Limiting**: Prevents abuse
- **WebSocket Support**: For real-time features

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```bash
# Flask Configuration
FLASK_SECRET_KEY=your-secure-random-key
FLASK_ENV=production

# OpenAI API Configuration (optional)
OPENAI_API_KEY=your-openai-api-key
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
```

### Auto-Generate .env File
The `docker-run.sh` script can create a `.env` file automatically:

```bash
./docker-run.sh dev  # Creates .env if it doesn't exist
```

## 🎯 Running Modes

### Development Mode
```bash
./docker-run.sh dev
```
- **Features**: Live logs, hot reloading
- **Port**: http://localhost:5000
- **Use Case**: Development and testing

### Production Mode
```bash
./docker-run.sh prod
```
- **Features**: Nginx reverse proxy, security headers
- **Port**: http://localhost (nginx) or http://localhost:5000 (direct)
- **Use Case**: Production deployment

## 📊 Container Management

### View Status
```bash
./docker-run.sh status
```

### View Logs
```bash
./docker-run.sh logs
```

### Stop Containers
```bash
./docker-run.sh stop
```

### Clean Up Everything
```bash
./docker-run.sh cleanup
```

## 🔒 Security Features

### Container Security
- **Non-root User**: Runs as `crawler` user
- **Resource Limits**: Prevents resource exhaustion
- **Health Checks**: Monitors application status
- **Security Headers**: XSS protection, frame options

### Network Security
- **Internal Communication**: Services communicate internally
- **Port Exposure**: Only necessary ports exposed
- **Rate Limiting**: Prevents abuse via nginx

### Data Security
- **Volume Mounts**: Persistent data storage
- **Environment Variables**: Secure configuration
- **No Hardcoded Secrets**: All secrets via environment

## 📁 Volume Structure

```
Project Root/
├── data/              # Database and persistent data
├── crawl_results/      # Crawling results
├── logs/              # Application logs
└── templates/         # Web interface templates (read-only)
```

## 🛠️ Manual Docker Commands

### Build Image
```bash
docker build -t alopecosa-crawler .
```

### Run Container
```bash
docker run -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/crawl_results:/app/crawl_results \
  -e OPENAI_API_KEY=your-key \
  alopecosa-crawler
```

### Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using port 5000
lsof -i :5000

# Stop containers
./docker-run.sh stop
```

#### 2. Permission Denied
```bash
# Make script executable
chmod +x docker-run.sh
```

#### 3. Docker Not Running
```bash
# Start Docker Desktop or Docker daemon
# On macOS: Open Docker Desktop
# On Linux: sudo systemctl start docker
```

#### 4. Out of Memory
```bash
# Check available memory
docker system df

# Clean up unused resources
docker system prune
```

#### 5. Build Failures
```bash
# Clean build cache
docker builder prune

# Rebuild without cache
docker-compose build --no-cache
```

### Debug Mode
```bash
# Run with debug output
docker-compose up --build --verbose

# Access container shell
docker-compose exec alopecosa-crawler bash
```

## 📈 Performance Optimization

### Resource Limits
The containers have default resource limits:
- **Memory**: 2GB limit, 512MB reservation
- **CPU**: 1.0 cores limit, 0.5 cores reservation

### Customize Limits
Edit `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      memory: 4G    # Increase memory limit
      cpus: '2.0'   # Increase CPU limit
    reservations:
      memory: 1G    # Increase memory reservation
      cpus: '1.0'   # Increase CPU reservation
```

### Scaling
For high-traffic scenarios:

```bash
# Scale the crawler service
docker-compose up --scale alopecosa-crawler=3
```

## 🌐 Production Deployment

### 1. Environment Setup
```bash
# Create production .env
cp .env.example .env.prod
# Edit .env.prod with production values
```

### 2. SSL/TLS Setup
Add SSL certificates to nginx:

```nginx
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    # ... rest of config
}
```

### 3. Reverse Proxy
Use nginx or Traefik for production:

```bash
# With Traefik
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 4. Monitoring
Add monitoring with Prometheus/Grafana:

```yaml
# Add to docker-compose.yml
monitoring:
  image: prom/prometheus
  ports:
    - "9090:9090"
  volumes:
    - ./monitoring:/etc/prometheus
```

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
name: Deploy to Production
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        run: |
          docker-compose pull
          docker-compose up -d
```

## 📚 Additional Resources

### Docker Documentation
- [Docker Official Docs](https://docs.docker.com/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)

### Related Files
- `Dockerfile` - Container definition
- `docker-compose.yml` - Multi-service orchestration
- `nginx.conf` - Reverse proxy configuration
- `docker-run.sh` - Easy management script
- `.dockerignore` - Build context exclusions

### Support
- Check logs: `./docker-run.sh logs`
- View status: `./docker-run.sh status`
- Get help: `./docker-run.sh help`

---

**🎉 You're ready to deploy your spider-inspired web crawler with Docker!**

The Docker setup provides a production-ready environment with security, monitoring, and easy management. Start with development mode to test, then move to production when ready.

