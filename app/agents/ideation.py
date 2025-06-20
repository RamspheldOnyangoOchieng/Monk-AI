import os
import os
import re
import json
from typing import Dict, List, Any, Optional
import logging
from sqlalchemy.orm import Session
from app.core.ai_service import AIService
from app.core.database import SessionLocal

logger = logging.getLogger(__name__)

class Ideation:
    """Agent for generating project ideas, specifications, user stories, and sprint plans."""
    
    def __init__(self, db_session: Session = None):
        """Initialize the Ideation agent."""
        self.db_session = db_session or SessionLocal()
        self.ai_service = AIService(session=self.db_session)
        
        # Define project scope templates
        self.scope_templates = {
            "web_app": "A web application with frontend and backend components",
            "mobile_app": "A mobile application for iOS and Android",
            "api": "A RESTful API service",
            "data_pipeline": "A data processing pipeline",
            "ml_model": "A machine learning model with training and inference",
            "desktop_app": "A desktop application for Windows/Mac/Linux"
        }
        
    async def generate_project_scope(self, description: str, template_key: Optional[str] = None, agent_id: int = 1, task_id: int = 1) -> Dict[str, Any]:
        """Generate a project scope based on description and optional template.
        
        Args:
            description: User's project description
            template_key: Optional key for predefined template
            agent_id: The ID of the agent
            task_id: The ID of the task
            
        Returns:
            Project scope details
        """
        template_context = self.scope_templates.get(template_key, "") if template_key else ""
        
        prompt = f"""
        Generate a comprehensive project scope based on the following description:
        {description}
        
        {f'Using this template as a starting point: {template_context}' if template_context else ''}
        
        The project scope should include:
        1. Project overview
        2. Goals and objectives
        3. Key features
        4. Technical requirements
        5. Constraints and limitations
        6. Timeline estimates
        7. Resources needed
        
        Format the response as a structured JSON object with these sections.
        """
        
        # Use AI service to generate project scope
        try:
            # NOTE: We need agent_id and task_id for logging, passing placeholders for now.
            ai_result = await self.ai_service.generate_text(
                prompt=prompt,
                agent_id=agent_id,
                task_id=task_id
            )
            
            response_content = ai_result["content"]
            
            # Try to parse JSON response
            try:
                project_data = json.loads(response_content)
            except json.JSONDecodeError:
                # If not valid JSON, wrap in a basic structure
                project_data = {
                    "project_name": f"Generated Project for {description[:50]}...",
                    "description": response_content,
                    "objectives": ["Generated from AI response"],
                    "target_audience": "To be defined",
                    "key_features": ["Generated from AI response"],
                    "success_metrics": ["To be defined"],
                    "resources_needed": ["To be defined"]
                }
            
            return project_data
            
        except Exception as e:
            logger.error(f"Error generating project scope: {e}", exc_info=True)
            # Fallback to mock data if AI service fails
            mock_data = self._get_mock_project_scope(description, template_key)
            mock_data["ai_status"] = {
                "provider": "fallback",
                "model": "mock",
                "status": "fallback_used",
                "error": str(e)
            }
            return mock_data
    
    async def generate_technical_specs(self, project_scope: Dict[str, Any], agent_id: int = 1, task_id: int = 1) -> Dict[str, Any]:
        """Generate technical specifications based on project scope.
        
        Args:
            project_scope: The project scope details
            agent_id: The ID of the agent
            task_id: The ID of the task
            
        Returns:
            Technical specifications
        """
        prompt = f"""
        Generate detailed technical specifications based on the following project scope:
        {json.dumps(project_scope, indent=2)}
        
        The technical specifications should include:
        1. System architecture
        2. Data models
        3. API endpoints
        4. Third-party integrations
        5. Security considerations
        6. Scalability plans
        7. Technology stack recommendations
        
        Format the response as a structured JSON object with these sections.
        """
        
        # Use AI service to generate technical specifications
        try:
            ai_result = await self.ai_service.generate_text(
                prompt=prompt,
                agent_id=agent_id,
                task_id=task_id
            )

            response_content = ai_result["content"]
            
            # Try to parse JSON response
            try:
                tech_specs = json.loads(response_content)
                return tech_specs
            except json.JSONDecodeError:
                # If not valid JSON, wrap in a basic structure
                return {
                    "system_architecture": response_content,
                    "data_models": "Generated from AI response",
                    "api_endpoints": "Generated from AI response",
                    "third_party_integrations": "Generated from AI response",
                    "security_considerations": "Generated from AI response",
                    "scalability_plans": "Generated from AI response",
                    "technology_stack": "Generated from AI response",
                }
        except Exception as e:
            logger.error(f"Error generating technical specs: {e}", exc_info=True)
            # Re-raise exception to be handled by orchestrator
            raise Exception(f"Error generating technical specs: {str(e)}")
    
    async def generate_user_stories(self, project_scope: Dict[str, Any], agent_id: int = 1, task_id: int = 1) -> List[Dict[str, Any]]:
        """Generate user stories based on project scope.
        
        Args:
            project_scope: The project scope details
            agent_id: The ID of the agent
            task_id: The ID of the task
            
        Returns:
            List of user stories
        """
        prompt = f"""
        Generate user stories based on the following project scope:
        {json.dumps(project_scope, indent=2)}
        
        Each user story should follow the format:
        - As a [type of user]
        - I want to [perform some action]
        - So that [I can achieve some goal/benefit]
        
        Also include:
        - Priority (High/Medium/Low)
        - Estimated effort (Story points: 1, 2, 3, 5, 8, 13)
        - Acceptance criteria
        
        Generate at least 10 user stories covering different aspects of the project.
        Format the response as a JSON array of user story objects.
        """
        
        # Use AI service to generate user stories
        try:
            ai_result = await self.ai_service.generate_text(
                prompt=prompt,
                agent_id=agent_id,
                task_id=task_id
            )

            response_content = ai_result["content"]
            
            # Try to parse JSON response
            try:
                return json.loads(response_content)
            except json.JSONDecodeError:
                # If not valid JSON, create a basic structure
                return [{
                    "id": 1,
                    "title": "Generated User Story",
                    "description": response_content,
                    "priority": "Medium",
                    "story_points": 3,
                    "acceptance_criteria": ["Generated from AI response"]
                }]
        except Exception as e:
            logger.error(f"Error generating user stories: {e}", exc_info=True)
            # Re-raise exception
            raise Exception(f"Error generating user stories: {str(e)}")
    
    async def generate_sprint_plan(self, user_stories: List[Dict[str, Any]], sprint_count: int = 3, agent_id: int = 1, task_id: int = 1) -> List[Dict[str, Any]]:
        """Generate sprint plan based on user stories.
        
        Args:
            user_stories: List of user stories
            sprint_count: Number of sprints to plan
            agent_id: The ID of the agent
            task_id: The ID of the task
            
        Returns:
            Sprint plan with stories assigned to sprints
        """
        prompt = f"""
        Generate a sprint plan for {sprint_count} sprints based on these user stories:
        {json.dumps(user_stories, indent=2)}
        
        The plan should include:
        - A list of sprints, each with a goal
        - User stories assigned to each sprint
        
        Format the response as a JSON array of sprint objects.
        """
        
        # Use AI service to generate sprint plan
        try:
            ai_result = await self.ai_service.generate_text(
                prompt=prompt,
                agent_id=agent_id,
                task_id=task_id,
            )

            response_content = ai_result["content"]

            # Try to parse JSON response
            try:
                return json.loads(response_content)
            except json.JSONDecodeError:
                # If not valid JSON, create a basic structure
                return [{
                    "sprint": 1,
                    "goal": "Initial setup and core features",
                    "user_stories": [user_stories[0] if user_stories else {"title": "Sample Story"}]
                }]
        except Exception as e:
            logger.error(f"Error generating sprint plan: {e}", exc_info=True)
            # Re-raise exception
            raise Exception(f"Error generating sprint plan: {str(e)}")
    
    def _get_mock_project_scope(self, description: str, template_key: Optional[str] = None) -> Dict[str, Any]:
        """Generate a mock project scope for development purposes."""
        template_type = template_key if template_key else "web_app"
        
        if "e-commerce" in description.lower() or "shop" in description.lower():
            return {
                "project_overview": "An e-commerce platform for selling products online",
                "goals_and_objectives": [
                    "Create a user-friendly shopping experience",
                    "Implement secure payment processing",
                    "Provide inventory management for sellers",
                    "Enable customer reviews and ratings"
                ],
                "key_features": [
                    "Product catalog with categories and search",
                    "Shopping cart and checkout process",
                    "User accounts and profiles",
                    "Order tracking and history",
                    "Admin dashboard for inventory management"
                ],
                "technical_requirements": [
                    "Responsive web design for mobile and desktop",
                    "Payment gateway integration",
                    "Database for products, users, and orders",
                    "Authentication and authorization system",
                    "API for mobile app integration"
                ],
                "constraints_and_limitations": [
                    "Budget constraints for third-party services",
                    "Timeline of 3 months for MVP",
                    "Compliance with payment card industry standards"
                ],
                "timeline_estimates": {
                    "planning_phase": "2 weeks",
                    "development_phase": "8 weeks",
                    "testing_phase": "2 weeks",
                    "deployment_phase": "1 week"
                },
                "resources_needed": [
                    "Frontend developer",
                    "Backend developer",
                    "UI/UX designer",
                    "QA tester",
                    "DevOps engineer (part-time)"
                ]
            }
        else:
            return {
                "project_overview": f"A {template_type} based on: {description}",
                "goals_and_objectives": [
                    "Create a scalable and maintainable solution",
                    "Deliver a user-friendly interface",
                    "Ensure security and performance",
                    "Meet all functional requirements"
                ],
                "key_features": [
                    "User authentication and authorization",
                    "Core functionality based on project description",
                    "Data management and persistence",
                    "Reporting and analytics",
                    "Admin controls and settings"
                ],
                "technical_requirements": [
                    "Modern frontend framework (React/Vue/Angular)",
                    "Robust backend API",
                    "Database design and implementation",
                    "Security measures (encryption, input validation)",
                    "Automated testing suite"
                ],
                "constraints_and_limitations": [
                    "Timeline constraints",
                    "Budget considerations",
                    "Technical debt management",
                    "Scalability requirements"
                ],
                "timeline_estimates": {
                    "planning_phase": "2-3 weeks",
                    "development_phase": "8-12 weeks",
                    "testing_phase": "2-4 weeks",
                    "deployment_phase": "1-2 weeks"
                },
                "resources_needed": [
                    "Frontend developer(s)",
                    "Backend developer(s)",
                    "UI/UX designer",
                    "QA engineer",
                    "Project manager",
                    "DevOps engineer (as needed)"
                ]
            }
    
    def _get_mock_technical_specs(self, project_scope: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock technical specifications for development purposes."""
        is_ecommerce = any("e-commerce" in str(value).lower() or "shop" in str(value).lower() 
                          for value in project_scope.values() if isinstance(value, (str, list)))
        
        if is_ecommerce:
            return {
                "system_architecture": {
                    "frontend": "React with Redux for state management",
                    "backend": "Node.js with Express",
                    "database": "MongoDB for products and PostgreSQL for transactions",
                    "caching": "Redis for session management and frequent queries",
                    "deployment": "Docker containers on AWS ECS"
                },
                "data_models": [
                    {
                        "name": "User",
                        "fields": [
                            {"name": "id", "type": "UUID", "description": "Unique identifier"},
                            {"name": "email", "type": "String", "description": "User email for login"},
                            {"name": "password", "type": "String", "description": "Hashed password"},
                            {"name": "name", "type": "String", "description": "User's full name"},
                            {"name": "address", "type": "Object", "description": "Shipping address"}
                        ]
                    },
                    {
                        "name": "Product",
                        "fields": [
                            {"name": "id", "type": "UUID", "description": "Unique identifier"},
                            {"name": "name", "type": "String", "description": "Product name"},
                            {"name": "description", "type": "String", "description": "Product description"},
                            {"name": "price", "type": "Decimal", "description": "Product price"},
                            {"name": "inventory", "type": "Integer", "description": "Available quantity"}
                        ]
                    },
                    {
                        "name": "Order",
                        "fields": [
                            {"name": "id", "type": "UUID", "description": "Unique identifier"},
                            {"name": "user_id", "type": "UUID", "description": "Reference to User"},
                            {"name": "items", "type": "Array", "description": "Array of order items"},
                            {"name": "total", "type": "Decimal", "description": "Order total"},
                            {"name": "status", "type": "String", "description": "Order status"}
                        ]
                    }
                ],
                "api_endpoints": [
                    {
                        "path": "/api/auth",
                        "methods": ["POST", "GET"],
                        "description": "Authentication endpoints"
                    },
                    {
                        "path": "/api/products",
                        "methods": ["GET", "POST", "PUT", "DELETE"],
                        "description": "Product management"
                    },
                    {
                        "path": "/api/cart",
                        "methods": ["GET", "POST", "PUT", "DELETE"],
                        "description": "Shopping cart operations"
                    },
                    {
                        "path": "/api/orders",
                        "methods": ["GET", "POST"],
                        "description": "Order processing"
                    },
                    {
                        "path": "/api/users",
                        "methods": ["GET", "PUT"],
                        "description": "User profile management"
                    }
                ],
                "third_party_integrations": [
                    {
                        "name": "Stripe",
                        "purpose": "Payment processing",
                        "implementation": "Server-side API integration"
                    },
                    {
                        "name": "AWS S3",
                        "purpose": "Product image storage",
                        "implementation": "Direct upload with signed URLs"
                    },
                    {
                        "name": "SendGrid",
                        "purpose": "Transactional emails",
                        "implementation": "API integration for order confirmations"
                    }
                ],
                "security_considerations": [
                    "JWT-based authentication with refresh tokens",
                    "HTTPS for all communications",
                    "Input validation and sanitization",
                    "Rate limiting for API endpoints",
                    "PCI compliance for payment processing"
                ],
                "scalability_plans": [
                    "Horizontal scaling of application servers",
                    "Database sharding for product catalog",
                    "CDN for static assets",
                    "Caching layer for product listings",
                    "Microservices architecture for future expansion"
                ],
                "technology_stack": {
                    "frontend": ["React", "Redux", "Material-UI", "Webpack"],
                    "backend": ["Node.js", "Express", "Mongoose", "Sequelize"],
                    "database": ["MongoDB", "PostgreSQL"],
                    "devops": ["Docker", "AWS", "GitHub Actions", "Terraform"]
                }
            }
        else:
            return {
                "system_architecture": {
                    "frontend": "React with TypeScript",
                    "backend": "Python FastAPI",
                    "database": "PostgreSQL with SQLAlchemy ORM",
                    "caching": "Redis for performance optimization",
                    "deployment": "Kubernetes cluster on cloud provider"
                },
                "data_models": [
                    {
                        "name": "User",
                        "fields": [
                            {"name": "id", "type": "UUID", "description": "Unique identifier"},
                            {"name": "email", "type": "String", "description": "User email"},
                            {"name": "name", "type": "String", "description": "User's name"},
                            {"name": "role", "type": "String", "description": "User role"}
                        ]
                    },
                    {
                        "name": "Project",
                        "fields": [
                            {"name": "id", "type": "UUID", "description": "Unique identifier"},
                            {"name": "name", "type": "String", "description": "Project name"},
                            {"name": "description", "type": "String", "description": "Project description"},
                            {"name": "owner_id", "type": "UUID", "description": "Reference to User"}
                        ]
                    },
                    {
                        "name": "Task",
                        "fields": [
                            {"name": "id", "type": "UUID", "description": "Unique identifier"},
                            {"name": "project_id", "type": "UUID", "description": "Reference to Project"},
                            {"name": "title", "type": "String", "description": "Task title"},
                            {"name": "description", "type": "String", "description": "Task description"},
                            {"name": "status", "type": "String", "description": "Task status"}
                        ]
                    }
                ],
                "api_endpoints": [
                    {
                        "path": "/api/auth",
                        "methods": ["POST", "GET"],
                        "description": "Authentication endpoints"
                    },
                    {
                        "path": "/api/users",
                        "methods": ["GET", "POST", "PUT", "DELETE"],
                        "description": "User management"
                    },
                    {
                        "path": "/api/projects",
                        "methods": ["GET", "POST", "PUT", "DELETE"],
                        "description": "Project operations"
                    },
                    {
                        "path": "/api/tasks",
                        "methods": ["GET", "POST", "PUT", "DELETE"],
                        "description": "Task management"
                    }
                ],
                "third_party_integrations": [
                    {
                        "name": "Auth0",
                        "purpose": "Authentication and authorization",
                        "implementation": "OAuth 2.0 integration"
                    },
                    {
                        "name": "AWS S3",
                        "purpose": "File storage",
                        "implementation": "SDK integration"
                    },
                    {
                        "name": "SendGrid",
                        "purpose": "Email notifications",
                        "implementation": "API integration"
                    }
                ],
                "security_considerations": [
                    "OAuth 2.0 with PKCE for authentication",
                    "HTTPS for all communications",
                    "Input validation and sanitization",
                    "Rate limiting for API endpoints",
                    "Regular security audits and penetration testing"
                ],
                "scalability_plans": [
                    "Horizontal scaling of application servers",
                    "Database read replicas for scaling reads",
                    "Caching strategies for frequently accessed data",
                    "Asynchronous processing for background tasks",
                    "Microservices architecture for independent scaling"
                ],
                "technology_stack": {
                    "frontend": ["React", "TypeScript", "Redux Toolkit", "Material-UI"],
                    "backend": ["Python", "FastAPI", "SQLAlchemy", "Pydantic"],
                    "database": ["PostgreSQL", "Redis"],
                    "devops": ["Docker", "Kubernetes", "GitHub Actions", "Terraform"]
                }
            }
    
    def _get_mock_user_stories(self, project_scope: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate mock user stories for development purposes."""
        is_ecommerce = any("e-commerce" in str(value).lower() or "shop" in str(value).lower() 
                          for value in project_scope.values() if isinstance(value, (str, list)))
        
        if is_ecommerce:
            return [
                {
                    "id": "US-001",
                    "as_a": "customer",
                    "i_want_to": "browse products by category",
                    "so_that": "I can find items I'm interested in purchasing",
                    "priority": "High",
                    "story_points": 5,
                    "acceptance_criteria": [
                        "Products are organized by categories",
                        "Categories are clearly labeled and navigable",
                        "Products display images, names, and prices",
                        "User can filter products within categories"
                    ]
                },
                {
                    "id": "US-002",
                    "as_a": "customer",
                    "i_want_to": "add items to my shopping cart",
                    "so_that": "I can purchase multiple items at once",
                    "priority": "High",
                    "story_points": 3,
                    "acceptance_criteria": [
                        "Add to cart button is visible on product pages",
                        "Cart updates immediately when items are added",
                        "User can view cart contents at any time",
                        "Cart persists across sessions"
                    ]
                },
                {
                    "id": "US-003",
                    "as_a": "customer",
                    "i_want_to": "create an account",
                    "so_that": "I can track my orders and save my information",
                    "priority": "High",
                    "story_points": 5,
                    "acceptance_criteria": [
                        "Registration form with validation",
                        "Email verification process",
                        "Password strength requirements",
                        "User can log in after registration"
                    ]
                },
                {
                    "id": "US-004",
                    "as_a": "customer",
                    "i_want_to": "checkout and pay for my items",
                    "so_that": "I can complete my purchase",
                    "priority": "High",
                    "story_points": 8,
                    "acceptance_criteria": [
                        "Secure payment processing",
                        "Address and shipping information collection",
                        "Order summary before payment",
                        "Order confirmation after payment"
                    ]
                },
                {
                    "id": "US-005",
                    "as_a": "customer",
                    "i_want_to": "view my order history",
                    "so_that": "I can track past purchases",
                    "priority": "Medium",
                    "story_points": 3,
                    "acceptance_criteria": [
                        "List of past orders with dates and status",
                        "Order details view with items and prices",
                        "Tracking information when available",
                        "Ability to reorder past purchases"
                    ]
                },
                {
                    "id": "US-006",
                    "as_a": "store owner",
                    "i_want_to": "add new products to the catalog",
                    "so_that": "I can expand my inventory",
                    "priority": "High",
                    "story_points": 5,
                    "acceptance_criteria": [
                        "Product creation form with validation",
                        "Image upload capability",
                        "Category assignment",
                        "Inventory and pricing fields"
                    ]
                },
                {
                    "id": "US-007",
                    "as_a": "store owner",
                    "i_want_to": "view sales reports",
                    "so_that": "I can track business performance",
                    "priority": "Medium",
                    "story_points": 8,
                    "acceptance_criteria": [
                        "Daily, weekly, monthly sales views",
                        "Product performance metrics",
                        "Revenue and profit calculations",
                        "Exportable reports"
                    ]
                },
                {
                    "id": "US-008",
                    "as_a": "customer",
                    "i_want_to": "search for products",
                    "so_that": "I can quickly find specific items",
                    "priority": "High",
                    "story_points": 5,
                    "acceptance_criteria": [
                        "Search bar is prominently displayed",
                        "Results update as user types",
                        "Relevant results based on keywords",
                        "No results message when appropriate"
                    ]
                },
                {
                    "id": "US-009",
                    "as_a": "customer",
                    "i_want_to": "leave reviews on products",
                    "so_that": "I can share my experience with others",
                    "priority": "Low",
                    "story_points": 5,
                    "acceptance_criteria": [
                        "Star rating system",
                        "Text review capability",
                        "Review moderation for administrators",
                        "Display of average ratings on product pages"
                    ]
                },
                {
                    "id": "US-010",
                    "as_a": "store owner",
                    "i_want_to": "manage inventory levels",
                    "so_that": "I can ensure product availability",
                    "priority": "Medium",
                    "story_points": 5,
                    "acceptance_criteria": [
                        "Inventory tracking for each product",
                        "Low stock alerts",
                        "Automatic out-of-stock handling",
                        "Bulk inventory update capability"
                    ]
                }
            ]
        else:
            return [
                {
                    "id": "US-001",
                    "as_a": "user",
                    "i_want_to": "create an account",
                    "so_that": "I can access the system",
                    "priority": "High",
                    "story_points": 3,
                    "acceptance_criteria": [
                        "Registration form with validation",
                        "Email verification process",
                        "Password strength requirements",
                        "User can log in after registration"
                    ]
                },
                {
                    "id": "US-002",
                    "as_a": "user",
                    "i_want_to": "log in to the system",
                    "so_that": "I can access my account",
                    "priority": "High",
                    "story_points": 2,
                    "acceptance_criteria": [
                        "Login form with validation",
                        "Password reset option",
                        "Remember me functionality",
                        "Secure authentication process"
                    ]
                },
                {
                    "id": "US-003",
                    "as_a": "user",
                    "i_want_to": "create a new project",
                    "so_that": "I can organize my work",
                    "priority": "High",
                    "story_points": 5,
                    "acceptance_criteria": [
                        "Project creation form",
                        "Project name and description fields",
                        "Project appears in user's project list",
                        "User becomes project owner"
                    ]
                },
                {
                    "id": "US-004",
                    "as_a": "project owner",
                    "i_want_to": "invite team members",
                    "so_that": "we can collaborate on the project",
                    "priority": "Medium",
                    "story_points": 5,
                    "acceptance_criteria": [
                        "Email invitation system",
                        "Role assignment for invitees",
                        "Acceptance flow for invitations",
                        "Team member list view"
                    ]
                },
                {
                    "id": "US-005",
                    "as_a": "team member",
                    "i_want_to": "create tasks",
                    "so_that": "work can be tracked and assigned",
                    "priority": "High",
                    "story_points": 5,
                    "acceptance_criteria": [
                        "Task creation form",
                        "Title, description, and priority fields",
                        "Ability to assign to team members",
                        "Due date selection"
                    ]
                },
                {
                    "id": "US-006",
                    "as_a": "team member",
                    "i_want_to": "view all tasks in a project",
                    "so_that": "I can see what needs to be done",
                    "priority": "Medium",
                    "story_points": 3,
                    "acceptance_criteria": [
                        "Task list view with filtering options",
                        "Sort by different criteria",
                        "Status indicators for tasks",
                        "Search functionality"
                    ]
                },
                {
                    "id": "US-007",
                    "as_a": "team member",
                    "i_want_to": "update task status",
                    "so_that": "progress can be tracked",
                    "priority": "High",
                    "story_points": 3,
                    "acceptance_criteria": [
                        "Status change options (To Do, In Progress, Done)",
                        "Status history tracking",
                        "Notifications for status changes",
                        "Visual indicators of status"
                    ]
                },
                {
                    "id": "US-008",
                    "as_a": "project owner",
                    "i_want_to": "generate project reports",
                    "so_that": "I can monitor progress and performance",
                    "priority": "Low",
                    "story_points": 8,
                    "acceptance_criteria": [
                        "Various report types (progress, time, etc.)",
                        "Filtering options for reports",
                        "Visual charts and graphs",
                        "Export to PDF/CSV"
                    ]
                },
                {
                    "id": "US-009",
                    "as_a": "team member",
                    "i_want_to": "comment on tasks",
                    "so_that": "I can provide updates and discuss issues",
                    "priority": "Medium",
                    "story_points": 3,
                    "acceptance_criteria": [
                        "Comment form on task details",
                        "Threaded conversations",
                        "Notification for mentioned users",
                        "Markdown support for formatting"
                    ]
                },
                {
                    "id": "US-010",
                    "as_a": "user",
                    "i_want_to": "set up my profile",
                    "so_that": "others can identify me and contact me",
                    "priority": "Low",
                    "story_points": 3,
                    "acceptance_criteria": [
                        "Profile picture upload",
                        "Contact information fields",
                        "Bio/description field",
                        "Skills/expertise listing"
                    ]
                }
            ]
    
    def _get_mock_sprint_plan(self, user_stories: List[Dict[str, Any]], sprint_count: int = 3) -> List[Dict[str, Any]]:
        """Generate a mock sprint plan for development purposes."""
        # Sort stories by priority and points
        high_priority = [story for story in user_stories if story["priority"] == "High"]
        medium_priority = [story for story in user_stories if story["priority"] == "Medium"]
        low_priority = [story for story in user_stories if story["priority"] == "Low"]
        
        # Create sprint plan
        sprints = []
        
        # Sprint 1: Focus on high priority items
        sprint1_stories = high_priority[:4]  # Take first 4 high priority stories
        sprint1_points = sum(story["story_points"] for story in sprint1_stories)
        sprints.append({
            "sprint_number": 1,
            "sprint_goal": "Establish core functionality",
            "user_stories": sprint1_stories,
            "total_story_points": sprint1_points,
            "key_deliverables": [
                "User authentication system",
                "Basic project/product setup",
                "Core user interactions"
            ]
        })
        
        # Sprint 2: Remaining high priority + some medium priority
        sprint2_stories = high_priority[4:] + medium_priority[:2]
        sprint2_points = sum(story["story_points"] for story in sprint2_stories)
        sprints.append({
            "sprint_number": 2,
            "sprint_goal": "Enhance user experience and functionality",
            "user_stories": sprint2_stories,
            "total_story_points": sprint2_points,
            "key_deliverables": [
                "Complete core user flows",
                "Implement secondary features",
                "Improve user interface"
            ]
        })
        
        # Sprint 3: Remaining medium priority + some low priority
        sprint3_stories = medium_priority[2:] + low_priority
        sprint3_points = sum(story["story_points"] for story in sprint3_stories)
        sprints.append({
            "sprint_number": 3,
            "sprint_goal": "Polish and finalize",
            "user_stories": sprint3_stories,
            "total_story_points": sprint3_points,
            "key_deliverables": [
                "Complete all remaining features",
                "Performance optimization",
                "Final testing and bug fixes"
            ]
        })
        
        return sprints[:sprint_count]  # Return only the requested number of sprints