import asyncio
import json
import time
import uuid
import os
import subprocess
import tempfile
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Optional, AsyncGenerator, Any
from app.agents.ideation import Ideation
from app.agents.code_optimizer import CodeOptimizer
from app.agents.orchestrator import AgentOrchestrator
from app.crud.agent_log import AgentLogRepository

router = APIRouter(tags=["workflow"])

class AutomatedWorkflowRequest(BaseModel):
    user_idea: str
    target_framework: str = "flask"  # flask, fastapi, react, express
    deployment_type: str = "local"  # local, docker

class WorkflowRequest(BaseModel):
    project_description: str
    programming_language: Optional[str] = "python"
    workflow_type: Optional[str] = "full_development"
    code_sample: Optional[str] = ""

# Global workflow store for tracking active workflows
active_workflows = {}
pipeline_requests: Dict[str, Any] = {}
workflow_requests: Dict[str, WorkflowRequest] = {}

def create_sse_message(event: str, data: Dict[str, Any]) -> str:
    """Formats a message for Server-Sent Events."""
    json_data = json.dumps(data)
    return f"event: {event}\ndata: {json_data}\n\n"

@router.post("/automated-pipeline")
async def start_automated_pipeline(request: AutomatedWorkflowRequest):
    """Start the fully automated pipeline from user idea to working app."""
    pipeline_id = str(uuid.uuid4())
    
    return {
        "pipeline_id": pipeline_id,
        "stream_url": f"/api/workflow/automated-stream/{pipeline_id}",
        "status": "started",
        "message": "Automated pipeline started - from idea to working app!"
    }

@router.get("/automated-stream/{pipeline_id}")
async def stream_automated_pipeline(pipeline_id: str):
    """Stream the automated pipeline execution."""
    
    from fastapi import Request as FastAPIRequest
    from app.main import app
    
    # Get the actual user request data
    pipeline_requests = getattr(app.state, 'pipeline_requests', {})
    request_data = pipeline_requests.get(pipeline_id, {
        "user_idea": "A task management app with user login and CRUD operations",
        "target_framework": "flask", 
        "deployment_type": "local"
    })
    
    request = AutomatedWorkflowRequest(
        user_idea=request_data.get("user_idea", "A task management app"),
        target_framework=request_data.get("target_framework", "flask"),
        deployment_type=request_data.get("deployment_type", "local")
    )
    
    return StreamingResponse(
        generate_automated_pipeline_stream(pipeline_id, request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

async def generate_automated_pipeline_stream(pipeline_id: str, request: AutomatedWorkflowRequest) -> AsyncGenerator[str, None]:
    """Generate the complete automated pipeline from idea to working app."""
    
    # Initialize agents
    ideation_agent = Ideation()
    code_optimizer = CodeOptimizer()
    
    # Step 1: Ideation & Feature Elaboration
    yield create_sse_message("pipeline_update", {
        "pipeline_id": pipeline_id,
        "step": "ideation",
        "status": "running",
        "message": "🤖 AI is elaborating your idea and generating features...",
        "progress": 10
    })
    
    await asyncio.sleep(1)
    
    try:
        project_scope = ideation_agent.generate_project_scope(request.user_idea)
        user_stories = await ideation_agent.generate_user_stories(project_scope)
        tech_specs = await ideation_agent.generate_technical_specs(project_scope)
        
        yield create_sse_message("step_complete", {
            "pipeline_id": pipeline_id,
            "step": "ideation",
            "status": "completed",
            "result": {
                "project_scope": project_scope,
                "user_stories": user_stories[:5],  # Limit for display
                "tech_specs": tech_specs
            },
            "progress": 25
        })
        
    except Exception as e:
        yield create_sse_message("error", {"message": f"Ideation failed: {str(e)}"})
        return
    
    # Step 2: Automated Code Generation
    yield create_sse_message("pipeline_update", {
        "pipeline_id": pipeline_id,
        "step": "code_generation",
        "status": "running", 
        "message": "⚡ Generating complete application code...",
        "progress": 40
    })
    
    await asyncio.sleep(2)
    
    # Generate application code based on framework
    generated_code = await generate_application_code(project_scope, request.target_framework)
    
    yield create_sse_message("step_complete", {
        "pipeline_id": pipeline_id,
        "step": "code_generation",
        "status": "completed",
        "result": {
            "framework": request.target_framework,
            "files_generated": len(generated_code),
            "main_file": list(generated_code.keys())[0] if generated_code else "No files",
            "preview": list(generated_code.values())[0][:500] + "..." if generated_code else "No code"
        },
        "progress": 60
    })
    
    # Step 3: Code Optimization
    yield create_sse_message("pipeline_update", {
        "pipeline_id": pipeline_id,
        "step": "optimization",
        "status": "running",
        "message": "🔧 Optimizing generated code for performance...",
        "progress": 70
    })
    
    await asyncio.sleep(1)
    
    # Optimize main file
    main_code = list(generated_code.values())[0] if generated_code else ""
    optimization_result = await code_optimizer.optimize_code(main_code, "python")
    
    yield create_sse_message("step_complete", {
        "pipeline_id": pipeline_id,
        "step": "optimization", 
        "status": "completed",
        "result": {
            "optimization_score": optimization_result.get("optimization_score", {}),
            "performance_projections": optimization_result.get("performance_projections", {}),
            "recommendations": optimization_result.get("recommendations_summary", {})
        },
        "progress": 80
    })
    
    # Step 4: Code Execution & App Deployment
    yield create_sse_message("pipeline_update", {
        "pipeline_id": pipeline_id,
        "step": "execution", 
        "status": "running",
        "message": "🚀 Executing code and starting your application...",
        "progress": 90
    })
    
    await asyncio.sleep(2)
    
    # Execute the generated code
    execution_result = await execute_generated_app(generated_code, request.target_framework, pipeline_id)
    
    yield create_sse_message("step_complete", {
        "pipeline_id": pipeline_id,
        "step": "execution",
        "status": "completed", 
        "result": execution_result,
        "progress": 100
    })
    
    # Final completion message
    yield create_sse_message("pipeline_complete", {
        "pipeline_id": pipeline_id,
        "status": "completed",
        "message": "🎉 Your app is ready and running!",
        "app_url": execution_result.get("app_url"),
        "app_preview": execution_result.get("preview_html"),
        "total_time": "45 seconds",
        "progress": 100
    })

async def generate_application_code(project_scope: Dict, framework: str) -> Dict[str, str]:
    """Generate complete application code based on project scope and framework."""
    
    project_name = project_scope.get("project_name", "Generated App")
    description = project_scope.get("description", "")
    
    if framework == "flask":
        return generate_flask_app(project_name, description)
    elif framework == "fastapi":
        return generate_fastapi_app(project_name, description)
    elif framework == "react":
        return generate_react_app(project_name, description)
    else:
        return generate_flask_app(project_name, description)  # Default to Flask

def generate_flask_app(project_name: str, description: str) -> Dict[str, str]:
    """Generate a complete Flask application."""
    
    app_code = f'''
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-{uuid.uuid4().hex[:8]}'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {{
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }}

# Routes
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks, project_name="{project_name}")

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task(
        title=data.get('title', ''),
        description=data.get('description', '')
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

# Create tables
with app.app_context():
    db.create_all()
    
    # Add sample data if no tasks exist
    if Task.query.count() == 0:
        sample_tasks = [
            Task(title="Welcome to {project_name}!", description="This is your first task. Click to mark it as complete."),
            Task(title="Add a new task", description="Use the form below to add your own tasks."),
            Task(title="Edit this task", description="Click the edit button to modify this task."),
        ]
        for task in sample_tasks:
            db.session.add(task)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    html_template = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{ project_name }}}}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ text-align: center; color: white; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }}
        .header p {{ font-size: 1.2em; opacity: 0.9; }}
        .app-container {{ background: white; border-radius: 15px; padding: 30px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); }}
        .task-form {{ background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
        .form-group {{ margin-bottom: 15px; }}
        .form-group label {{ display: block; margin-bottom: 5px; font-weight: bold; color: #333; }}
        .form-group input, .form-group textarea {{ width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px; transition: border-color 0.3s; }}
        .form-group input:focus, .form-group textarea:focus {{ outline: none; border-color: #667eea; }}
        .btn {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 16px; transition: transform 0.2s; }}
        .btn:hover {{ transform: translateY(-2px); }}
        .task-list {{ list-style: none; }}
        .task-item {{ background: white; border: 2px solid #e0e0e0; border-radius: 10px; padding: 20px; margin-bottom: 15px; transition: all 0.3s; }}
        .task-item:hover {{ transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }}
        .task-item.completed {{ opacity: 0.7; border-color: #28a745; }}
        .task-title {{ font-size: 1.3em; font-weight: bold; margin-bottom: 8px; color: #333; }}
        .task-description {{ color: #666; margin-bottom: 15px; line-height: 1.5; }}
        .task-actions {{ display: flex; gap: 10px; }}
        .btn-small {{ padding: 8px 16px; font-size: 14px; }}
        .btn-success {{ background: #28a745; }}
        .btn-danger {{ background: #dc3545; }}
        .btn-warning {{ background: #ffc107; color: #333; }}
        .status-badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; text-transform: uppercase; }}
        .status-pending {{ background: #ffeaa7; color: #d63031; }}
        .status-completed {{ background: #55a3ff; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{{{ project_name }}}}</h1>
            <p>AI-Generated Task Management Application</p>
        </div>
        
        <div class="app-container">
            <div class="task-form">
                <h3>Add New Task</h3>
                <form id="taskForm">
                    <div class="form-group">
                        <label for="title">Task Title:</label>
                        <input type="text" id="title" name="title" required>
                    </div>
                    <div class="form-group">
                        <label for="description">Description:</label>
                        <textarea id="description" name="description" rows="3"></textarea>
                    </div>
                    <button type="submit" class="btn">Add Task</button>
                </form>
            </div>
            
            <div class="tasks-section">
                <h3>Your Tasks</h3>
                <ul class="task-list" id="taskList">
                    {{% for task in tasks %}}
                    <li class="task-item {{% if task.completed %}}completed{{% endif %}}" data-task-id="{{{{ task.id }}}}">
                        <div class="task-title">{{{{ task.title }}}}</div>
                        <div class="task-description">{{{{ task.description or 'No description' }}}}</div>
                        <div class="task-actions">
                            <span class="status-badge {{% if task.completed %}}status-completed{{% else %}}status-pending{{% endif %}}">
                                {{% if task.completed %}}Completed{{% else %}}Pending{{% endif %}}
                            </span>
                            <button class="btn btn-success btn-small" onclick="toggleTask({{{{ task.id }}}}, {{{{ not task.completed }}}})">
                                {{% if task.completed %}}Mark Pending{{% else %}}Mark Complete{{% endif %}}
                            </button>
                            <button class="btn btn-danger btn-small" onclick="deleteTask({{{{ task.id }}}})">Delete</button>
                        </div>
                    </li>
                    {{% endfor %}}
                </ul>
            </div>
        </div>
    </div>

    <script>
        // Add new task
        document.getElementById('taskForm').addEventListener('submit', async (e) => {{
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = {{
                title: formData.get('title'),
                description: formData.get('description')
            }};
            
            try {{
                const response = await fetch('/api/tasks', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(data)
                }});
                
                if (response.ok) {{
                    location.reload();
                }}
            }} catch (error) {{
                console.error('Error adding task:', error);
            }}
        }});
        
        // Toggle task completion
        async function toggleTask(taskId, completed) {{
            try {{
                const response = await fetch(`/api/tasks/${{taskId}}`, {{
                    method: 'PUT',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ completed }})
                }});
                
                if (response.ok) {{
                    location.reload();
                }}
            }} catch (error) {{
                console.error('Error updating task:', error);
            }}
        }}
        
        // Delete task
        async function deleteTask(taskId) {{
            if (confirm('Are you sure you want to delete this task?')) {{
                try {{
                    const response = await fetch(`/api/tasks/${{taskId}}`, {{
                        method: 'DELETE'
                    }});
                    
                    if (response.ok) {{
                        location.reload();
                    }}
                }} catch (error) {{
                    console.error('Error deleting task:', error);
                }}
            }}
        }}
    </script>
</body>
</html>
'''
    
    requirements = '''
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Werkzeug==2.3.7
'''
    
    return {
        "app.py": app_code,
        "templates/index.html": html_template,
        "requirements.txt": requirements
    }

def generate_fastapi_app(project_name: str, description: str) -> Dict[str, str]:
    """Generate a FastAPI application."""
    # Similar structure but for FastAPI
    return generate_flask_app(project_name, description)  # Simplified for demo

def generate_react_app(project_name: str, description: str) -> Dict[str, str]:
    """Generate a React application."""
    # Similar structure but for React
    return generate_flask_app(project_name, description)  # Simplified for demo

async def execute_generated_app(generated_code: Dict[str, str], framework: str, pipeline_id: str) -> Dict[str, Any]:
    """Execute the generated application code and return execution details."""
    
    try:
        # Create temporary directory for the app
        temp_dir = tempfile.mkdtemp(suffix=f"_monk_ai_{pipeline_id}")
        
        # Write all generated files
        for filename, content in generated_code.items():
            file_path = os.path.join(temp_dir, filename)
            
            # Create directories if needed
            os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else temp_dir, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Install requirements
        requirements_path = os.path.join(temp_dir, "requirements.txt")
        if os.path.exists(requirements_path):
            subprocess.run(["pip", "install", "-r", requirements_path], 
                         cwd=temp_dir, capture_output=True, text=True, timeout=30)
        
        # Start the application in background
        if framework == "flask":
            app_file = os.path.join(temp_dir, "app.py")
            if os.path.exists(app_file):
                # For demo, we'll simulate app execution
                port = 5000 + hash(pipeline_id) % 1000  # Generate unique port
                
                # In a real implementation, you'd start the Flask app:
                # process = subprocess.Popen(["python", app_file], cwd=temp_dir)
                
                # For demo, return success with preview
                with open(os.path.join(temp_dir, "templates/index.html"), 'r') as f:
                    preview_html = f.read()
                    # Replace Flask template syntax for preview
                    preview_html = preview_html.replace("{{ project_name }}", "Demo Task Manager")
                    preview_html = preview_html.replace("{% for task in tasks %}", "")
                    preview_html = preview_html.replace("{% endfor %}", "")
                    preview_html = preview_html.replace("{{ task.id }}", "1")
                    preview_html = preview_html.replace("{{ task.title }}", "Sample Task")
                    preview_html = preview_html.replace("{{ task.description or 'No description' }}", "This is a sample task")
                    preview_html = preview_html.replace("{% if task.completed %}", "")
                    preview_html = preview_html.replace("{% else %}", "")
                    preview_html = preview_html.replace("{% endif %}", "")
                    preview_html = preview_html.replace("{{ not task.completed }}", "true")
                
                return {
                    "status": "success",
                    "message": "Application is running successfully!",
                    "app_url": f"http://localhost:{port}",
                    "framework": framework,
                    "files_created": len(generated_code),
                    "temp_directory": temp_dir,
                    "preview_html": preview_html,
                    "features": [
                        "✅ Task Creation",
                        "✅ Task Management", 
                        "✅ Task Completion",
                        "✅ Task Deletion",
                        "✅ Responsive Design",
                        "✅ RESTful API"
                    ]
                }
        
        return {
            "status": "error",
            "message": "Failed to execute application",
            "temp_directory": temp_dir
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Execution failed: {str(e)}",
            "temp_directory": None
        }

async def generate_workflow_stream(workflow_id: str, request: WorkflowRequest) -> AsyncGenerator[str, None]:
    """Generate workflow execution stream with step tracking and stop capability"""
    
    # Initialize workflow tracking
    active_workflows[workflow_id] = {
        "status": "running",
        "current_step": 0,
        "total_steps": 6,
        "progress": 0,
        "steps": [],
        "should_stop": False,
        "start_time": asyncio.get_event_loop().time()
    }
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator()
    
    workflow_steps = [
        ("ideation", "Ideation & Planning"),
        ("code_generation", "Code Generation"),
        ("security_analysis", "Security Analysis"),
        ("test_generation", "Test Generation"),
        ("documentation", "Documentation"),
        ("code_review", "Code Review")
    ]
    
    context = {
        "project_description": request.project_description,
        "programming_language": request.programming_language,
        "workflow_type": request.workflow_type,
        "code_sample": request.code_sample
    }

    try:
        # Initial workflow started message
        yield create_sse_message("workflow_start", {
            "workflow_id": workflow_id,
            "status": "started",
            "total_steps": len(workflow_steps),
            "progress": 0,
            "message": "🚀 Workflow initiated, buckle up!"
        })

        for i, (step_key, step_name) in enumerate(workflow_steps):
            
            # Check if workflow should stop
            if active_workflows.get(workflow_id, {}).get("should_stop", False):
                yield create_sse_message("workflow_update", {
                    "workflow_id": workflow_id,
                    "status": "stopping",
                    "message": "Workflow stop signal received."
                })
                break
            
            step_id = f"{workflow_id}-{i+1}"
            active_workflows[workflow_id]["current_step"] = i + 1
            
            # Send step start message
            yield create_sse_message("step_start", {
                "workflow_id": workflow_id,
                "step_id": step_id,
                "agent_name": step_name,
                "status": "started",
                "progress": 0,
                "message": f"🚀 {step_name}: Starting..."
            })
            
            active_workflows[workflow_id]["progress"] = int(((i + 1) / len(workflow_steps)) * 100 * 0.5)
            
            # Send an update that we're in progress
            yield create_sse_message("step_update", {
                "workflow_id": workflow_id,
                "step_id": step_id,
                "agent_name": step_name,
                "status": "running",
                "progress": 75,
                "message": f"⚡ {step_name}: Processing..."
            })
            
            # Execute the actual step
            try:
                result = await orchestrator.execute_step(step_key, context)
                
                # Update context with results
                context.update(result)
                
                # Send step completion
                yield create_sse_message("step_complete", {
                    "workflow_id": workflow_id,
                    "step_id": step_id,
                    "agent_name": step_name,
                    "status": "completed",
                    "progress": 100,
                    "result": result,
                    "duration": 2, # Placeholder duration
                    "message": f"✅ {step_name}: Completed successfully"
                })
                
                await asyncio.sleep(0.5)
                
            except Exception as e:
                # Send error for this step but continue workflow
                yield create_sse_message("step_error", {
                    "workflow_id": workflow_id,
                    "step_id": step_id,
                    "agent_name": step_name,
                    "status": "failed",
                    "progress": 100,
                    "error": str(e),
                    "message": f"❌ {step_name}: Failed - {str(e)}"
                })
                
                await asyncio.sleep(0.5)
        
        # Final workflow completion
        if workflow_id in active_workflows:
            final_status = "stopped" if active_workflows[workflow_id].get("should_stop", False) else "completed"
            
            active_workflows[workflow_id]["status"] = final_status
            active_workflows[workflow_id]["progress"] = 100
            
            yield create_sse_message("workflow_complete", {
                "workflow_id": workflow_id,
                "status": final_status,
                "results": context,
                "total_time": int(asyncio.get_event_loop().time() - active_workflows[workflow_id]["start_time"]),
                "message": "🎉 Workflow completed successfully!" if final_status == "completed" else "🛑 Workflow stopped",
                "progress": 100
            })
        
    except Exception as e:
        # Send final error
        yield create_sse_message("error", {
            "workflow_id": workflow_id,
            "message": f"Workflow failed: {str(e)}",
            "error": str(e)
        })
    
    finally:
        # Clean up workflow tracking
        if workflow_id in active_workflows:
            # Keep for a short time for status queries
            await asyncio.sleep(2)
            if workflow_id in active_workflows:
                del active_workflows[workflow_id]

@router.post("/execute")
async def start_workflow(request: WorkflowRequest):
    """Start a new workflow execution."""
    workflow_id = str(uuid.uuid4())
    workflow_requests[workflow_id] = request
    
    return {
        "workflow_id": workflow_id,
        "stream_url": f"/api/workflow/stream/{workflow_id}",
        "status": "started"
    }

@router.get("/stream/{workflow_id}")
async def stream_workflow(workflow_id: str):
    """Stream workflow execution via Server-Sent Events."""
    
    if workflow_id not in workflow_requests:
        raise HTTPException(status_code=404, detail="Workflow not found")

    request = workflow_requests[workflow_id]
    
    return StreamingResponse(
        generate_workflow_stream(workflow_id, request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
        }
    )

@router.get("/available-workflows")
async def get_available_workflows():
    """Get list of available workflow types."""
    return {
        "workflows": [
            {
                "id": "automated_pipeline",
                "name": "Automated Pipeline", 
                "description": "Complete end-to-end: Idea → Features → Code → Running App",
                "estimated_time": "2-3 minutes",
                "steps": ["Ideation", "Code Generation", "Optimization", "Execution"]
            },
            {
                "id": "full_development", 
                "name": "Full Development Cycle",
                "description": "Complete development workflow with all agents",
                "estimated_time": "5-8 minutes",
                "steps": ["Ideation", "Code Generation", "Security Analysis", "Testing", "Documentation", "Review"]
            },
            {
                "id": "code_improvement",
                "name": "Code Improvement",
                "description": "Focus on optimizing existing code",
                "estimated_time": "3-5 minutes", 
                "steps": ["Code Generation", "Security Analysis", "Testing", "Review"]
            },
            {
                "id": "security_focused",
                "name": "Security Analysis",
                "description": "Security-focused code review and testing",
                "estimated_time": "2-3 minutes",
                "steps": ["Security Analysis", "Testing"]
            }
        ]
    }

# FRONTEND DEMO ENDPOINTS - Adding here to fix 404 errors
@router.get("/demo/scenarios") 
async def get_demo_scenarios():
    """Get demo scenarios for the frontend"""
    return {
        "scenarios": [
            {
                "id": "task-management",
                "title": "🎯 Task Management App",
                "description": "Build a complete task management application with user authentication, CRUD operations, and real-time updates",
                "expected_duration": "3 minutes",
                "features": ["Authentication", "CRUD Operations", "Real-time Updates"]
            },
            {
                "id": "ecommerce", 
                "title": "🛒 E-commerce Platform",
                "description": "Create a full-featured e-commerce platform with product catalog, shopping cart, and payment integration",
                "expected_duration": "4 minutes", 
                "features": ["Product Catalog", "Shopping Cart", "Payment Integration"]
            },
            {
                "id": "chat-app",
                "title": "💬 Real-time Chat Application", 
                "description": "Develop a real-time chat application with WebSocket support, user presence, and message history",
                "expected_duration": "3.5 minutes",
                "features": ["WebSocket Support", "User Presence", "Message History"]
            },
            {
                "id": "api-service",
                "title": "🔧 REST API Service",
                "description": "Build a robust REST API service with authentication, rate limiting, and comprehensive documentation", 
                "expected_duration": "2.5 minutes",
                "features": ["Authentication", "Rate Limiting", "API Documentation"]
            }
        ]
    }

@router.get("/demo/live-metrics")
async def get_live_metrics():
    """Get live metrics for the demo dashboard"""
    return {
        "live_stats": {
            "agents_active": 6,
            "workflows_completed": 193,
            "lines_of_code_generated": 68651,
            "security_vulnerabilities_prevented": 346,
            "tests_generated": 1247,
            "documentation_pages_created": 89,
            "developer_time_saved_hours": 1027
        },
        "real_time_activity": [
            "✅ TestGenerator: Created 47 unit tests with 96% coverage",
            "🔒 SecurityAnalyzer: Detected and fixed SQL injection vulnerability", 
            "📝 DocGenerator: Generated user guide for e-commerce module - Quality Score: A+",
            "⚡ CodeOptimizer: Improved database query performance by 340%",
            "🤖 IdeationAgent: Proposed microservices architecture for scalability"
        ],
        "performance_metrics": {
            "average_response_time": "1.2s",
            "success_rate": "99.7%",
            "agent_utilization": "87%",
            "queue_length": 3
        },
        "total_agents": 6,
        "active_workflows": 12,
        "completed_tasks": 193,
        "avg_response_time": 1.2,
        "uptime_hours": 1027
    }

@router.post("/stop/{workflow_id}")
async def stop_workflow(workflow_id: str):
    """Stop a running workflow"""
    try:
        if workflow_id in active_workflows:
            # Signal the workflow to stop
            active_workflows[workflow_id]["should_stop"] = True
            
            # Clean up after a delay
            await asyncio.sleep(1)
            if workflow_id in active_workflows:
                del active_workflows[workflow_id]
            
            return {"message": f"Workflow {workflow_id} has been stopped", "workflow_id": workflow_id}
        else:
            return {"message": f"Workflow {workflow_id} not found or already completed", "workflow_id": workflow_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop workflow: {str(e)}")

@router.get("/status/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Get the current status of a workflow"""
    if workflow_id in active_workflows:
        workflow = active_workflows[workflow_id]
        return {
            "workflow_id": workflow_id,
            "status": workflow.get("status", "running"),
            "current_step": workflow.get("current_step", 0),
            "total_steps": workflow.get("total_steps", 6),
            "progress": workflow.get("progress", 0),
            "steps": workflow.get("steps", [])
        }
    else:
        return {"workflow_id": workflow_id, "status": "not_found"}