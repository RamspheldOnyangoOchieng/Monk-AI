from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime

from app.api.routes import users, projects, snippets, reviews, auth, agents, workflow
from app.agents.pr_reviewer import PRReviewer

api_router = APIRouter()

# Include all routers with their prefixes
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(snippets.router, prefix="/snippets", tags=["snippets"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(workflow.router, prefix="/workflow", tags=["workflow"])

# Add missing endpoints for frontend compatibility
@api_router.post("/generate-project-scope")
async def generate_project_scope(request: dict):
    """Generate project scope - redirect to ideation agent"""
    try:
        # Use the working ideation agent
        from app.agents.ideation import Ideation
        ideation = Ideation()
        
        description = request.get("description", "")
        template_key = request.get("template_key", "web_app")
        
        project_scope = await ideation.generate_project_scope(
            description=description,
            template_key=template_key
        )
        
        return {
            "status": "success",
            "project_scope": project_scope,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@api_router.get("/demo/scenarios")
async def get_demo_scenarios():
    """Get demo scenarios for the frontend"""
    return {
        "scenarios": [
            {
                "id": "task-management",
                "name": "Task Management App",
                "description": "Build a complete task management application with user authentication, CRUD operations, and real-time updates",
                "duration": "3 minutes",
                "icon": "task"
            },
            {
                "id": "ecommerce",
                "name": "E-commerce Platform", 
                "description": "Create a modern e-commerce platform with shopping cart, payment processing, and inventory management",
                "duration": "4 minutes",
                "icon": "shop"
            },
            {
                "id": "chat-app",
                "name": "Real-time Chat Application",
                "description": "Develop a real-time chat application with user authentication and message history",
                "duration": "3.5 minutes",
                "icon": "chat"
            },
            {
                "id": "api-service",
                "name": "REST API Service",
                "description": "Build a robust REST API service with authentication, validation, and documentation",
                "duration": "2.5 minutes",
                "icon": "api"
            }
        ]
    }

@api_router.get("/demo/live-metrics")
async def get_live_metrics():
    """Get live metrics for the demo dashboard"""
    return {
        "metrics": {
            "active_agents": 7,
            "projects_generated": 142,
            "code_lines_generated": 15847,
            "user_stories_created": 486,
            "tests_generated": 293,
            "success_rate": 97.8,
            "avg_generation_time": 2.3
        },
        "recent_activity": [
            {
                "timestamp": datetime.now().isoformat(),
                "action": "Project Generated",
                "details": "TaskMaster Pro - Task Management App"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "action": "User Stories Created",
                "details": "15 stories for E-commerce Platform"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "action": "Code Generated",
                "details": "FastAPI endpoints with authentication"
            }
        ]
    }

@api_router.post("/api/automated-pipeline")
async def start_automated_pipeline(request: dict):
    """Endpoint to start the automated pipeline with user input."""
    try:
        import uuid
        
        # Extract user input
        user_idea = request.get("user_idea", "")
        target_framework = request.get("target_framework", "flask")
        deployment_type = request.get("deployment_type", "local")
        
        # Forward to workflow router with the actual user input
        pipeline_id = str(uuid.uuid4())
        
        # Store the request data temporarily (in production, use proper storage)
        from app.main import app
        if not hasattr(app.state, 'pipeline_requests'):
            app.state.pipeline_requests = {}
        app.state.pipeline_requests[pipeline_id] = {
            "user_idea": user_idea,
            "target_framework": target_framework,
            "deployment_type": deployment_type
        }
        
        return {
            "pipeline_id": pipeline_id,
            "stream_url": f"/api/workflow/automated-stream/{pipeline_id}",
            "status": "started",
            "message": "Automated pipeline started - from idea to working app!"
        }
    except Exception as e:
        return {"error": str(e)}, 500 