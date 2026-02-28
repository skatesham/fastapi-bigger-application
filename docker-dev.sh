#!/bin/bash

# FastAPI Car Shop ERP - Docker Development Script
# This script automates the Docker setup and development workflow

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

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Function to start services
start_services() {
    print_status "Starting FastAPI Car Shop ERP with Docker..."
    
    # Build and start services
    if docker compose version &> /dev/null; then
        docker compose up --build -d
    else
        docker-compose up --build -d
    fi
    
    print_success "Services are starting up..."
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 10
    
    # Check service status
    check_services
}

# Function to check service status
check_services() {
    print_status "Checking service status..."
    
    # Check API health
    if curl -f http://localhost:8000/health &> /dev/null; then
        print_success "✅ FastAPI API is healthy (http://localhost:8000)"
    else
        print_warning "⚠️  FastAPI API is not ready yet"
    fi
    
    # Check database
    if docker compose exec -T db pg_isready -U skatesham &> /dev/null; then
        print_success "✅ PostgreSQL database is ready"
    else
        print_warning "⚠️  PostgreSQL database is not ready yet"
    fi
    
    # Check Adminer
    if curl -f http://localhost:9000 &> /dev/null; then
        print_success "✅ Adminer is accessible (http://localhost:9000)"
    else
        print_warning "⚠️  Adminer is not ready yet"
    fi
}

# Function to show logs
show_logs() {
    print_status "Showing logs for all services..."
    if docker compose version &> /dev/null; then
        docker compose logs -f
    else
        docker-compose logs -f
    fi
}

# Function to stop services
stop_services() {
    print_status "Stopping all services..."
    if docker compose version &> /dev/null; then
        docker compose down
    else
        docker-compose down
    fi
    print_success "All services stopped"
}

# Function to reset everything
reset_services() {
    print_warning "This will remove all containers, networks, and volumes. Continue? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Removing all services and volumes..."
        if docker compose version &> /dev/null; then
            docker compose down -v
            docker compose system prune -f
        else
            docker-compose down -v
            docker system prune -f
        fi
        print_success "Environment reset complete"
    else
        print_status "Reset cancelled"
    fi
}

# Function to show service URLs
show_urls() {
    echo ""
    print_success "🚀 FastAPI Car Shop ERP is running!"
    echo ""
    echo -e "${BLUE}Available Services:${NC}"
    echo -e "  📡 ${GREEN}FastAPI API:${NC}        http://localhost:8000"
    echo -e "  📚 ${GREEN}API Documentation:${NC}   http://localhost:8000/docs"
    echo -e "  🗄️  ${GREEN}PostgreSQL:${NC}         localhost:5432 (skatesham:skatesham-github)"
    echo -e "  🔧 ${GREEN}Adminer (DB Admin):${NC}  http://localhost:9000"
    echo ""
    echo -e "${BLUE}Database Credentials:${NC}"
    echo -e "  📝 User: ${YELLOW}skatesham${NC}"
    echo -e "  🔒 Password: ${YELLOW}skatesham-github${NC}"
    echo -e "  🗃️  Database: ${YELLOW}skatesham${NC}"
    echo ""
}

# Main menu
show_menu() {
    echo ""
    echo -e "${BLUE}FastAPI Car Shop ERP - Docker Development${NC}"
    echo "=================================="
    echo "1) 🚀 Start services"
    echo "2) 📊 Check service status"
    echo "3) 📋 Show logs"
    echo "4) 🛑 Stop services"
    echo "5) 🔄 Reset environment"
    echo "6) 🔗 Show service URLs"
    echo "7) ❌ Exit"
    echo ""
}

# Main execution
main() {
    check_docker
    
    while true; do
        show_menu
        read -p "Choose an option [1-7]: " choice
        
        case $choice in
            1)
                start_services
                show_urls
                ;;
            2)
                check_services
                ;;
            3)
                show_logs
                ;;
            4)
                stop_services
                ;;
            5)
                reset_services
                ;;
            6)
                show_urls
                ;;
            7)
                print_status "Goodbye! 👋"
                exit 0
                ;;
            *)
                print_error "Invalid option. Please choose 1-7."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Run main function
main
