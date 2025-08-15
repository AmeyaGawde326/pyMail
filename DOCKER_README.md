# Docker Email Server

This document provides comprehensive instructions for running the Python Email Server using Docker.

## Prerequisites

- **Docker** installed and running
- **Docker Compose** (usually comes with Docker Desktop)
- **Environment file** (.env) with your configuration

## Quick Start

### 1. Create Environment File

First, create a `.env` file with your configuration:

```bash
# Copy the example file
cp env_example.txt .env

# Edit the .env file with your values
# MAIL_USERNAME=your-email@gmail.com
# MAIL_PASSWORD=your-app-password
# MAIL_DEFAULT_SENDER=your-email@gmail.com
# API_KEY=your-api-key-here
```

### 2. Run with Docker Compose (Recommended)

```bash
# Start the server
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the server
docker-compose down
```

### 3. Run with Docker Run

```bash
# Build the image
docker build -t python-email-server .

# Run the container
docker run -d \
  --name python-email-server \
  --env-file .env \
  -p 5000:5000 \
  --restart unless-stopped \
  python-email-server

# View logs
docker logs -f python-email-server

# Stop the container
docker stop python-email-server
docker rm python-email-server
```

## Using the Runner Scripts

### Linux/macOS (Bash)

Make the script executable and run:

```bash
# Make executable
chmod +x docker-run.sh

# Start with Docker Compose (recommended)
./docker-run.sh compose

# Start with Docker run
./docker-run.sh run

# Stop the server
./docker-run.sh stop

# View logs
./docker-run.sh logs

# Check status
./docker-run.sh status

# Show help
./docker-run.sh help
```

### Windows (Batch)

```cmd
# Start with Docker Compose (recommended)
docker-run.bat compose

# Start with Docker run
docker-run.bat run

# Stop the server
docker-run.bat stop

# View logs
docker-run.bat logs

# Check status
docker-run.bat status

# Show help
docker-run.bat help
```

## Docker Commands Reference

### Building the Image

```bash
# Build the image
docker build -t python-email-server .

# Build with no cache (force rebuild)
docker build --no-cache -t python-email-server .
```

### Running the Container

#### Docker Compose (Recommended)

```bash
# Start in background
docker-compose up -d

# Start and view logs
docker-compose up

# Stop and remove containers
docker-compose down

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Restart service
docker-compose restart
```

#### Docker Run

```bash
# Basic run
docker run -d \
  --name python-email-server \
  --env-file .env \
  -p 5000:5000 \
  python-email-server

# Run with restart policy
docker run -d \
  --name python-email-server \
  --env-file .env \
  -p 5000:5000 \
  --restart unless-stopped \
  python-email-server

# Run with custom environment variables
docker run -d \
  --name python-email-server \
  -e MAIL_USERNAME=your-email@gmail.com \
  -e MAIL_PASSWORD=your-app-password \
  -e MAIL_DEFAULT_SENDER=your-email@gmail.com \
  -e API_KEY=your-api-key \
  -p 5000:5000 \
  python-email-server
```

### Container Management

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop container
docker stop python-email-server

# Start container
docker start python-email-server

# Restart container
docker restart python-email-server

# Remove container
docker rm python-email-server

# Remove container and image
docker rm -f python-email-server
docker rmi python-email-server
```

### Logs and Debugging

```bash
# View logs
docker logs python-email-server

# Follow logs in real-time
docker logs -f python-email-server

# View last N lines
docker logs --tail 100 python-email-server

# View logs with timestamps
docker logs -t python-email-server
```

### Container Inspection

```bash
# Inspect container configuration
docker inspect python-email-server

# View container resource usage
docker stats python-email-server

# Execute command in running container
docker exec -it python-email-server /bin/bash

# View container processes
docker top python-email-server
```

## Environment Variables

The following environment variables can be set in your `.env` file or passed directly to Docker:

### Required Variables

```bash
# SMTP Configuration
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Security
API_KEY=your-api-key-here
```

### Optional Variables

```bash
# SMTP Configuration (defaults shown)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False

# Flask Configuration
FLASK_ENV=production
```

## Port Configuration

The default port is 5000. To change the port:

### Docker Compose

Edit `docker-compose.yml`:

```yaml
ports:
  - "8080:5000"  # Host port 8080, container port 5000
```

### Docker Run

```bash
docker run -d \
  --name python-email-server \
  --env-file .env \
  -p 8080:5000 \  # Host port 8080, container port 5000
  python-email-server
```

## Health Checks

The container includes a health check that monitors the `/health` endpoint:

```bash
# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Health}}"

# View health check logs
docker inspect python-email-server | grep -A 10 Health
```

## Troubleshooting

### Common Issues

#### Container Won't Start

```bash
# Check container logs
docker logs python-email-server

# Check if port is already in use
netstat -tulpn | grep :5000

# Check Docker daemon status
docker info
```

#### Environment Variables Not Working

```bash
# Verify .env file exists
ls -la .env

# Check environment variables in container
docker exec python-email-server env | grep MAIL

# Test with explicit environment variables
docker run -d \
  --name python-email-server-test \
  -e MAIL_USERNAME=test@gmail.com \
  -e MAIL_PASSWORD=test \
  -p 5001:5000 \
  python-email-server
```

#### Permission Issues

```bash
# Check file permissions
ls -la docker-run.sh

# Fix permissions (Linux/macOS)
chmod +x docker-run.sh

# Run as administrator (Windows)
# Right-click Command Prompt → Run as administrator
```

### Debug Mode

To run in debug mode for troubleshooting:

```bash
# Run with interactive terminal
docker run -it \
  --name python-email-server-debug \
  --env-file .env \
  -p 5000:5000 \
  python-email-server

# Or override the command
docker run -it \
  --name python-email-server-debug \
  --env-file .env \
  -p 5000:5000 \
  python-email-server /bin/bash
```

## Production Deployment

### Security Considerations

1. **Use strong API keys** - Generate secure random API keys
2. **Limit container access** - Don't run as root
3. **Network isolation** - Use custom Docker networks
4. **Resource limits** - Set memory and CPU limits

### Resource Limits

```bash
# Run with resource limits
docker run -d \
  --name python-email-server \
  --env-file .env \
  -p 5000:5000 \
  --memory=512m \
  --cpus=1.0 \
  --restart unless-stopped \
  python-email-server
```

### Docker Compose with Limits

```yaml
services:
  email-server:
    build: .
    container_name: python-email-server
    ports:
      - "5000:5000"
    env_file:
      - .env
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.5'
```

## Monitoring and Logging

### Log Aggregation

```bash
# Send logs to external system
docker run -d \
  --name python-email-server \
  --env-file .env \
  -p 5000:5000 \
  --log-driver=syslog \
  --log-opt syslog-address=udp://localhost:514 \
  python-email-server
```

### Performance Monitoring

```bash
# Monitor container performance
docker stats python-email-server

# Monitor specific metrics
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
```

## Backup and Recovery

### Backup Container Data

```bash
# Create backup of container
docker commit python-email-server python-email-server-backup

# Export container as tar
docker export python-email-server > email-server-backup.tar

# Save image
docker save python-email-server > email-server-image.tar
```

### Restore from Backup

```bash
# Load image from backup
docker load < email-server-image.tar

# Import container from backup
docker import email-server-backup.tar python-email-server-restored
```

## Support

If you encounter issues:

1. Check the container logs: `docker logs python-email-server`
2. Verify environment variables are set correctly
3. Ensure Docker is running and accessible
4. Check port conflicts and firewall settings
5. Review the main README.md for application-specific issues

## Quick Commands Summary

```bash
# Start server (Docker Compose)
docker-compose up -d

# Start server (Docker run)
docker run -d --name python-email-server --env-file .env -p 5000:5000 python-email-server

# View logs
docker-compose logs -f
# or
docker logs -f python-email-server

# Stop server
docker-compose down
# or
docker stop python-email-server

# Check status
docker-compose ps
# or
docker ps --filter name=python-email-server
```
