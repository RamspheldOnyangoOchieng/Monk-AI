#!/bin/bash

# Production deployment script for Monk AI

set -e  # Exit on error

# Colors for better output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create required directories
mkdir -p data nginx/ssl nginx/cache

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file doesn't exist.${NC}"
    echo -e "${YELLOW}Creating a production .env file...${NC}"
    
    if [ -f .env.production ]; then
        cp .env.production .env
        echo -e "${GREEN}Production .env file created.${NC}"
    elif [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${YELLOW}Using example .env file. Please update with production values.${NC}"
        sleep 2  # Give time to read the warning
    else
        echo -e "${RED}No .env templates found. Please create a .env file manually.${NC}"
        exit 1
    fi
fi

# Process command line arguments
REBUILD=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -r|--rebuild) REBUILD=true ;;
        -h|--help)
            echo "Usage: $0 [-r|--rebuild]"
            echo "  -r, --rebuild   Force rebuilding of images"
            echo "  -h, --help      Show this help message"
            exit 0
            ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Check for SSL certificates
if [ ! -f nginx/ssl/fullchain.pem ] || [ ! -f nginx/ssl/privkey.pem ]; then
    echo -e "${YELLOW}Warning: SSL certificates not found in nginx/ssl/${NC}"
    echo -e "${YELLOW}For production, please add proper SSL certificates${NC}"
    echo -e "${YELLOW}For testing, creating self-signed certificates...${NC}"
    
    # Generate self-signed certificates for testing
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout nginx/ssl/privkey.pem -out nginx/ssl/fullchain.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    
    echo -e "${GREEN}Self-signed certificates created for testing.${NC}"
    echo -e "${RED}DO NOT USE THESE IN ACTUAL PRODUCTION!${NC}"
fi

# Prepare environment
echo -e "${GREEN}Setting up production environment...${NC}"

# Build or pull the latest images
if [ "$REBUILD" = true ]; then
    echo -e "${YELLOW}Rebuilding containers from scratch...${NC}"
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml build --no-cache
else
    echo -e "${YELLOW}Using cached images when available...${NC}"
fi

# Start production environment
echo -e "${GREEN}Starting production environment with Docker Compose...${NC}"
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Display status
echo -e "${GREEN}Production environment started in detached mode.${NC}"
echo -e "${GREEN}Commands:${NC}"
echo -e "  ${YELLOW}docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps${NC}    - List containers"
echo -e "  ${YELLOW}docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f${NC} - View logs"
echo -e "  ${YELLOW}docker-compose -f docker-compose.yml -f docker-compose.prod.yml down${NC}  - Stop environment" 