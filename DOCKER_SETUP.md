# Docker Setup for TraeDevMate

This document provides instructions on how to run TraeDevMate using Docker.

## Prerequisites

- Docker installed on your machine
- Docker Compose installed on your machine

## Project Structure
```
traedevmate/
├── app/                # Backend FastAPI application
│   ├── agents/         # AI agent implementations
│   └── main.py         # Main FastAPI application entry point
├── frontend/           # React frontend application
│   ├── public/         # Static assets
│   ├── src/            # React source code
│   │   ├── pages/      # React page components
│   │   └── App.tsx     # Main React application component
│   ├── package.json    # Frontend dependencies
│   └── tsconfig.json   # TypeScript configuration
├── docker-compose.yml          # Docker Compose configuration for development
├── docker-compose.prod.yml     # Docker Compose overrides for production
├── Dockerfile.backend          # Dockerfile for the backend service
├── Dockerfile.frontend         # Dockerfile for the frontend service
├── nginx/                      # Nginx configuration for production
│   ├── nginx.conf              # Nginx configuration
│   └── ssl/                    # SSL certificates (for production)
└── scripts/                    # Helper scripts
    ├── dev.sh                  # Development startup script
    └── prod.sh                 # Production deployment script
```

## Getting Started

1. Create a `.env` file with your API keys:
```
# API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
NOVITA_API_KEY=your_novita_key

# Database Configuration
DATABASE_URL=sqlite:///./data/app.db

# FastAPI Configuration
DEBUG=true
ENVIRONMENT=development

# Security
JWT_SECRET=your_jwt_secret_for_development
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

2. Start the development environment:
```bash
# Using the helper script
./scripts/dev.sh

# Or directly with Docker Compose
docker-compose up --build
```

3. Access the services:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API documentation: http://localhost:8000/docs

## Development Workflow

The development setup includes:
- Hot-reloading for the backend code through volume mounts
- Volume mounts for frontend code to facilitate development
- Automatic database creation through SQLite

## Production Deployment

For production deployment:

```bash
# Using the helper script (includes SSL certificate generation)
./scripts/prod.sh

# Or manually
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

The production setup includes:
- Nginx reverse proxy with SSL support
- Optimized container configurations
- Resource limits for each service

## Troubleshooting

### Common Issues

1. **Missing Frontend Files**:
   If you encounter errors about missing files during the frontend build:
   ```
   Ensure all required files exist in the frontend directory:
   - frontend/public/index.html
   - frontend/src/index.tsx
   - frontend/tsconfig.json
   ```

2. **Backend Connectivity Issues**:
   If the frontend can't connect to the backend:
   ```bash
   # Check backend logs
   docker-compose logs backend
   
   # Verify the backend health endpoint is working
   curl http://localhost:8000/health
   ```

3. **Permission Issues**:
   ```bash
   # Fix data directory permissions
   mkdir -p data
   chmod 777 data
   ``` 