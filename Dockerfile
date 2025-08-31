# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=src/web_interface/web_interface.py \
    FLASK_ENV=production \
    WERKZEUG_RUN_MAIN=true

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create necessary directories
RUN mkdir -p data crawl_results

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash crawler && \
    chown -R crawler:crawler /app
USER crawler

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Default command to run the web interface
# Use Gunicorn for production, launch_web.py for development
CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:application"]

