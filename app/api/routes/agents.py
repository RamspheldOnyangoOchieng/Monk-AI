"""
API routes for AI agents - connecting to existing agent implementations
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
import time
from datetime import datetime

# Import the existing agents
from app.agents.code_optimizer import CodeOptimizer
from app.agents.doc_generator import DocGenerator
from app.agents.ideation import Ideation
from app.agents.orchestrator import AgentOrchestrator
from app.agents.pr_reviewer import PRReviewer
from app.agents.security_analyzer import SecurityAnalyzer
from app.agents.test_generator import TestGenerator

router = APIRouter()

# Initialize agents
code_optimizer = CodeOptimizer()
doc_generator = DocGenerator()
ideation_agent = Ideation()
orchestrator = AgentOrchestrator()
pr_reviewer = PRReviewer()
security_analyzer = SecurityAnalyzer()
test_generator = TestGenerator()

# Request/Response Models
class CodeOptimizationRequest(BaseModel):
    code: str
    language: str
    focus_areas: Optional[List[str]] = None

class DocumentationRequest(BaseModel):
    code: str
    language: str
    context: Optional[str] = None

class SecurityAnalysisRequest(BaseModel):
    code: str
    language: str
    focus_areas: Optional[List[str]] = None

class TestGenerationRequest(BaseModel):
    code: str
    language: str
    test_framework: str = "pytest"

class PRReviewRequest(BaseModel):
    pr_url: str
    repository: str
    branch: str = "main"

class IdeationRequest(BaseModel):
    description: str
    template_key: Optional[str] = None

class WorkflowRequest(BaseModel):
    workflow_type: str
    description: str
    language: str = "python"
    code: Optional[str] = None

# Agent Endpoints

@router.post("/optimize")
async def optimize_code(request: CodeOptimizationRequest):
    """Optimize code using the CodeOptimizer agent"""
    try:
        result = await code_optimizer.optimize_code(
            code=request.code,
            language=request.language,
            focus_areas=request.focus_areas
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code optimization failed: {str(e)}")

@router.post("/document")
async def generate_documentation(request: DocumentationRequest):
    """Generate documentation using the DocGenerator agent"""
    try:
        result = await doc_generator.generate_docs(
            code=request.code,
            language=request.language,
            context=request.context
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Documentation generation failed: {str(e)}")

@router.post("/security-analyze")
async def analyze_security(request: SecurityAnalysisRequest):
    """Analyze code security using the SecurityAnalyzer agent"""
    try:
        result = await security_analyzer.analyze_security(
            code=request.code,
            language=request.language,
            focus_areas=request.focus_areas
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Security analysis failed: {str(e)}")

@router.post("/generate-tests")
async def generate_tests(request: TestGenerationRequest):
    """Generate tests using the TestGenerator agent"""
    try:
        result = await test_generator.generate_tests(
            code=request.code,
            language=request.language,
            test_framework=request.test_framework
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test generation failed: {str(e)}")

@router.post("/review-pr")
async def review_pull_request(request: PRReviewRequest):
    """Review pull request using the PRReviewer agent"""
    try:
        result = await pr_reviewer.review_pr(
            pr_url=request.pr_url,
            repository=request.repository,
            branch=request.branch
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PR review failed: {str(e)}")

@router.post("/ideate")
async def generate_project_ideas(request: IdeationRequest):
    """Generate project ideas using the Ideation agent"""
    try:
        # Generate project scope first
        project_scope = ideation_agent.generate_project_scope(
            description=request.description,
            template_key=request.template_key
        )
        
        # Generate technical specs and user stories concurrently
        technical_specs_task = asyncio.create_task(
            asyncio.to_thread(ideation_agent.generate_technical_specs, project_scope)
        )
        user_stories_task = asyncio.create_task(
            asyncio.to_thread(ideation_agent.generate_user_stories, project_scope)
        )
        
        # Wait for both tasks to complete
        technical_specs, user_stories = await asyncio.gather(
            technical_specs_task, user_stories_task
        )
        
        return {
            "status": "success",
            "project_scope": project_scope,
            "technical_specs": technical_specs,
            "user_stories": user_stories
        }
    except Exception as e:
        print(f"Ideation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ideation failed: {str(e)}")

@router.post("/orchestrate")
async def orchestrate_workflow(request: WorkflowRequest):
    """Execute a complete workflow using the Orchestrator agent"""
    try:
        # Prepare initial input for the workflow
        initial_input = {
            "description": request.description,
            "language": request.language,
            "code": request.code
        }
        
        # Execute the workflow
        result = await orchestrator.execute_workflow(
            workflow_type=request.workflow_type,
            initial_input=initial_input
        )
        
        return result.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow orchestration failed: {str(e)}")

@router.get("/workflows")
async def get_available_workflows():
    """Get list of available workflow templates"""
    try:
        workflows = orchestrator.get_available_workflows()
        return {
            "status": "success",
            "workflows": workflows
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get workflows: {str(e)}")

@router.post("/full-workflow")
async def execute_full_development_workflow(request: WorkflowRequest):
    """Execute the complete development workflow"""
    try:
        result = await orchestrator.execute_full_workflow(
            description=request.description,
            language=request.language
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full workflow execution failed: {str(e)}")

# Agent Status and Health Endpoints

@router.get("/status")
async def get_agents_status():
    """Get status of all agents"""
    return {
        "status": "success",
        "agents": {
            "code_optimizer": "active",
            "doc_generator": "active", 
            "security_analyzer": "active",
            "test_generator": "active",
            "pr_reviewer": "active",
            "ideation": "active",
            "orchestrator": "active"
        },
        "timestamp": datetime.now().isoformat()
    }

@router.get("/health")
async def health_check():
    """Health check for all agents"""
    try:
        # Quick health check for each agent
        health_status = {
            "code_optimizer": "healthy",
            "doc_generator": "healthy",
            "security_analyzer": "healthy", 
            "test_generator": "healthy",
            "pr_reviewer": "healthy",
            "ideation": "healthy",
            "orchestrator": "healthy"
        }
        
        return {
            "status": "healthy",
            "agents": health_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")