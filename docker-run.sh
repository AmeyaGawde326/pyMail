#!/bin/bash

# Docker Email Server Runner Script
# This script provides various commands to run the containerized email server

set -e

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

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if .env file exists
check_env_file() {
    if [ ! -f .env ]; then
        print_error ".env file not found!"
        print_status "Please create a .env file with the following variables:"
        echo ""
        echo "MAIL_USERNAME=your-email@gmail.com"
        echo "MAIL_PASSWORD=your-app-password"
        echo "MAIL_DEFAULT_SENDER=your-email@gmail.com"
        echo "API_KEY=your-api-key-here"
        echo ""
        print_status "You can copy from env_example.txt and update the values"
        exit 1
    fi
    print_success ".env file found"
}

# Function to build the Docker image
build_image() {
    print_status "Building Docker image..."
    docker build -t python-email-server .
    print_success "Docker image built successfully"
}

# Function to run with Docker Compose (recommended)
run_with_compose() {
    print_status "Starting email server with Docker Compose..."
    docker-compose up -d
    print_success "Email server started with Docker Compose"
    print_status "Server is running on http://localhost:5000"
    print_status "Use 'docker-compose logs -f' to view logs"
    print_status "Use 'docker-compose down' to stop the server"
}

# Function to run with Docker run command
run_with_docker() {
    print_status "Starting email server with Docker run..."
    
    # Stop and remove existing container if it exists
    docker stop python-email-server 2>/dev/null || true
    docker rm python-email-server 2>/dev/null || true
    
    # Run the container
    docker run -d \
        --name python-email-server \
        --env-file .env \
        -p 5000:5000 \
        --restart unless-stopped \
        python-email-server
    
    print_success "Email server started with Docker run"
    print_status "Server is running on http://localhost:5000"
    print_status "Use 'docker logs -f python-email-server' to view logs"
    print_status "Use 'docker stop python-email-server' to stop the server"
}

# Function to stop the server
stop_server() {
    print_status "Stopping email server..."
    
    # Try Docker Compose first
    if docker-compose ps | grep -q "email-server"; then
        docker-compose down
        print_success "Email server stopped with Docker Compose"
    else
        # Try Docker run
        if docker ps | grep -q "python-email-server"; then
            docker stop python-email-server
            docker rm python-email-server
            print_success "Email server stopped with Docker run"
        else
            print_warning "No running email server found"
        fi
    fi
}

# Function to view logs
view_logs() {
    print_status "Viewing logs..."
    
    # Try Docker Compose first
    if docker-compose ps | grep -q "email-server"; then
        docker-compose logs -f
    else
        # Try Docker run
        if docker ps | grep -q "python-email-server"; then
            docker logs -f python-email-server
        else
            print_error "No running email server found"
        fi
    fi
}

# Function to show status
show_status() {
    print_status "Email server status:"
    
    # Try Docker Compose first
    if docker-compose ps | grep -q "email-server"; then
        docker-compose ps
        echo ""
        print_status "Docker Compose is managing the service"
    else
        # Try Docker run
        if docker ps | grep -q "python-email-server"; then
            docker ps --filter name=python-email-server
            echo ""
            print_status "Docker run is managing the service"
        else
            print_warning "No running email server found"
        fi
    fi
}

# Function to show help
show_help() {
    echo "Docker Email Server Runner Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build     Build the Docker image"
    echo "  compose   Start server with Docker Compose (recommended)"
    echo "  run       Start server with Docker run command"
    echo "  stop      Stop the running server"
    echo "  logs      View server logs"
    echo "  status    Show server status"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 compose    # Start with Docker Compose"
    echo "  $0 run        # Start with Docker run"
    echo "  $0 stop       # Stop the server"
    echo "  $0 logs       # View logs"
    echo ""
    echo "Note: Make sure you have a .env file with your configuration"
}

# Main script logic
main() {
    case "${1:-compose}" in
        "build")
            check_docker
            build_image
            ;;
        "compose")
            check_docker
            check_env_file
            build_image
            run_with_compose
            ;;
        "run")
            check_docker
            check_env_file
            build_image
            run_with_docker
            ;;
        "stop")
            check_docker
            stop_server
            ;;
        "logs")
            check_docker
            view_logs
            ;;
        "status")
            check_docker
            show_status
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
