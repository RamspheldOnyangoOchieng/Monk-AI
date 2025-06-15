#!/bin/bash

# Development startup script for Monk AI

set -e  # Exit on error

# Colors for better output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create data directory if it doesn't exist
mkdir -p data

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file doesn't exist.${NC}"
    echo -e "${YELLOW}Creating a default .env file...${NC}"
    cp -n .env.example .env || echo -e "${RED}No .env.example found. Please create a .env file manually.${NC}"
    
    if [ -f .env ]; then
        echo -e "${GREEN}Default .env file created. You may want to edit it with your specific settings.${NC}"
    else
        exit 1
    fi
fi

# Process command line arguments
DETACHED=false
REBUILD=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -d|--detach) DETACHED=true ;;
        -r|--rebuild) REBUILD=true ;;
        -h|--help)
            echo "Usage: $0 [-d|--detach] [-r|--rebuild]"
            echo "  -d, --detach    Run containers in detached mode"
            echo "  -r, --rebuild   Force rebuilding of images"
            echo "  -h, --help      Show this help message"
            exit 0
            ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Start development environment
echo -e "${GREEN}Starting development environment with Docker Compose...${NC}"

# Prepare docker compose command
DOCKER_COMPOSE_CMD="docker compose"

if [ "$REBUILD" = true ]; then
    DOCKER_COMPOSE_CMD="$DOCKER_COMPOSE_CMD build --no-cache"
    echo -e "${YELLOW}Rebuilding containers from scratch...${NC}"
fi

if [ "$DETACHED" = true ]; then
    echo -e "${YELLOW}Running in detached mode. Use 'docker compose logs -f' to view logs.${NC}"
    $DOCKER_COMPOSE_CMD up -d
else
    $DOCKER_COMPOSE_CMD up
fi

# This will only run if in detached mode or after stopping with Ctrl+C
echo -e "${GREEN}Development environment commands:${NC}"
echo -e "  ${YELLOW}docker compose ps${NC}      - List containers"
echo -e "  ${YELLOW}docker compose logs -f${NC} - View logs"
echo -e "  ${YELLOW}docker compose down${NC}    - Stop environment" 