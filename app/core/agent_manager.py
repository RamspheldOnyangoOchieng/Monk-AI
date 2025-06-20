import asyncio
import logging
import uuid
import time
import json
from typing import Dict, List, Optional, Any, Callable, Set, Tuple
from enum import Enum
from datetime import datetime, timedelta
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError
import redis.asyncio as redis

from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

class TaskStatus(str, Enum):
    """Task status enum for type safety and validation."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELED = "canceled"

class TaskPriority(int, Enum):
    """Task priority levels."""
    LOW = 1
    MEDIUM = 5
    HIGH = 10
    CRITICAL = 20

class Task:
    """Represents a task to be executed by an agent."""
    
    def __init__(
        self, 
        task_type: str, 
        priority: TaskPriority = TaskPriority.MEDIUM,
        data: Optional[Dict[str, Any]] = None,
        callback: Optional[Callable] = None,
        task_id: Optional[str] = None,
        timeout_seconds: Optional[int] = None
    ):
        self.id = task_id or str(uuid.uuid4())
        self.task_type = task_type
        self.priority = priority
        self.data = data or {}
        self.callback = callback
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.result: Optional[Any] = None
        self.status = TaskStatus.PENDING
        self.error: Optional[str] = None
        self.agent_id: Optional[str] = None
        self.runtime_seconds: Optional[float] = None
        self.timeout_seconds = timeout_seconds or settings.AGENT_TIMEOUT_SECONDS
        self.retry_count = 0
        self.max_retries = 3

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for serialization."""
        return {
            "id": self.id,
            "task_type": self.task_type,
            "priority": int(self.priority),
            "data": self.data,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "status": self.status,
            "error": self.error,
            "agent_id": self.agent_id,
            "runtime_seconds": self.runtime_seconds,
            "timeout_seconds": self.timeout_seconds,
            "retry_count": self.retry_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create a Task instance from a dictionary."""
        task = cls(
            task_type=data["task_type"],
            priority=TaskPriority(data["priority"]),
            data=data.get("data", {}),
            task_id=data["id"],
            timeout_seconds=data.get("timeout_seconds")
        )
        
        # Restore task state
        task.status = TaskStatus(data["status"])
        if data.get("created_at"):
            task.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("started_at"):
            task.started_at = datetime.fromisoformat(data["started_at"])
        if data.get("completed_at"):
            task.completed_at = datetime.fromisoformat(data["completed_at"])
        task.error = data.get("error")
        task.agent_id = data.get("agent_id")
        task.runtime_seconds = data.get("runtime_seconds")
        task.retry_count = data.get("retry_count", 0)
        
        return task

class AgentType(str, Enum):
    """Types of agents available in the system."""
    GENERAL = "general"
    RESEARCHER = "researcher"
    WRITER = "writer"
    CODER = "coder"
    ANALYST = "analyst"


class Agent:
    """Represents an AI agent that can execute tasks."""
    
    def __init__(self, agent_id: str, agent_type: AgentType):
        self.id = agent_id
        self.agent_type = agent_type
        self.current_task: Optional[Task] = None
        self.last_active = datetime.now()
        self.status = "idle"  # idle, busy
        self.completed_task_count = 0
        self.failed_task_count = 0
        self.total_runtime_seconds = 0.0
        self.health_status = "healthy"  # healthy, degraded, unhealthy
        self.specialties: Set[str] = set()  # Task types this agent is specialized in
        
    async def execute_task(self, task: Task) -> Any:
        """Execute the given task and return the result."""
        self.current_task = task
        self.status = "busy"
        self.last_active = datetime.now()
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()
        task.agent_id = self.id
        start_time = time.time()
        
        try:
            logger.info(f"Agent {self.id} executing task {task.id} of type {task.task_type}")
            
            # Here you would implement the actual task execution logic
            # This would likely involve calling the appropriate AI model/service
            # For demonstration purposes, we'll simulate work with a delay
            
            # Different agent types might handle tasks differently
            if self.agent_type == AgentType.RESEARCHER:
                # Simulating research work
                await asyncio.sleep(2)
                result = {"research_findings": f"Research findings for {task.task_type}"}
            elif self.agent_type == AgentType.WRITER:
                # Simulating writing work
                await asyncio.sleep(3)
                result = {"written_content": f"Written content for {task.task_type}"}
            else:
                # Default handling for other agent types
                await asyncio.sleep(1)
                result = {"message": f"Task {task.task_type} completed successfully"}
            
            # Task execution successful
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            task.result = result
            self.completed_task_count += 1
            
            # Call the callback if provided
            if task.callback:
                try:
                    task.callback(task)
                except Exception as callback_error:
                    logger.error(f"Error in task callback: {str(callback_error)}")
                
            return result
            
        except Exception as e:
            # Task execution failed
            logger.error(f"Task execution failed: {str(e)}")
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()
            self.failed_task_count += 1
            return None
        finally:
            task.runtime_seconds = time.time() - start_time
            self.total_runtime_seconds += task.runtime_seconds
            self.current_task = None
            self.status = "idle"
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert agent to dictionary for serialization."""
        return {
            "id": self.id,
            "agent_type": self.agent_type,
            "status": self.status,
            "last_active": self.last_active.isoformat(),
            "completed_task_count": self.completed_task_count,
            "failed_task_count": self.failed_task_count,
            "total_runtime_seconds": self.total_runtime_seconds,
            "health_status": self.health_status,
            "specialties": list(self.specialties),
            "current_task_id": self.current_task.id if self.current_task else None
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Agent':
        """Create an Agent instance from a dictionary."""
        agent = cls(
            agent_id=data["id"], 
            agent_type=AgentType(data["agent_type"])
        )
        agent.status = data["status"]
        agent.last_active = datetime.fromisoformat(data["last_active"])
        agent.completed_task_count = data["completed_task_count"]
        agent.failed_task_count = data["failed_task_count"]
        agent.total_runtime_seconds = data["total_runtime_seconds"]
        agent.health_status = data["health_status"]
        agent.specialties = set(data["specialties"])
        return agent


class AgentManager:
    """
    Manages a pool of agents and distributes tasks to them.
    Implements task scheduling, prioritization, and agent allocation.
    """
    
    def __init__(self, use_persistence: bool = True):
        self.agents: Dict[str, Agent] = {}
        self.task_queue: List[Task] = []
        self.running_tasks: Dict[str, Task] = {}
        self.completed_tasks: Dict[str, Task] = {}
        self.max_agents = settings.MAX_CONCURRENT_AGENTS
        self.task_timeout = settings.AGENT_TIMEOUT_SECONDS
        self.use_persistence = use_persistence
        self.metrics: Dict[str, Any] = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "avg_completion_time": 0.0,
            "queue_length_history": [],
        }
        
        # Initialize Redis for task persistence if enabled
        if self.use_persistence:
            self.redis = redis.from_url(settings.REDIS_URL)
        
    async def register_agent(self, agent_type: AgentType, specialties: List[str] = None) -> Agent:
        """Register a new agent in the pool."""
        agent_id = f"{agent_type}-{str(uuid.uuid4())[:8]}"
        agent = Agent(agent_id, agent_type)
        
        # Set specialties if provided
        if specialties:
            agent.specialties = set(specialties)
            
        self.agents[agent_id] = agent
        logger.info(f"Registered new agent: {agent_id} of type {agent_type}")
        
        # Save agent to persistent storage if enabled
        if self.use_persistence:
            await self._save_agent(agent)
            
        return agent
        
    async def add_task(self, task: Task) -> str:
        """Add a task to the queue for execution."""
        self.task_queue.append(task)
        # Sort by priority (higher numbers first)
        self.task_queue.sort(key=lambda x: x.priority, reverse=True)
        logger.info(f"Added task {task.id} to queue with priority {task.priority}")
        
        # Save task to persistent storage if enabled
        if self.use_persistence:
            await self._save_task(task)
            
        # Update metrics
        self.metrics["queue_length_history"].append({
            "timestamp": datetime.now().isoformat(),
            "length": len(self.task_queue)
        })
        if len(self.metrics["queue_length_history"]) > 100:
            # Keep only the last 100 entries to prevent unbounded growth
            self.metrics["queue_length_history"] = self.metrics["queue_length_history"][-100:]
            
        return task.id
    
    def get_available_agent(self, task_type: str) -> Optional[Agent]:
        """
        Find an available agent that can handle the given task type.
        Uses a scoring system to find the best agent based on:
        1. Specialist for the task type
        2. Idle status
        3. Fewest completed tasks (for load balancing)
        """
        best_agent = None
        best_score = -1
        
        for agent in self.agents.values():
            if agent.status != "idle":
                continue
                
            # Base score - all idle agents start at 0
            score = 0
            
            # Add points for specialists
            if task_type in agent.specialties:
                score += 10
                
            # Add points for health status
            if agent.health_status == "healthy":
                score += 5
            elif agent.health_status == "degraded":
                score += 2
                
            # Distribute load - prefer agents with fewer completed tasks
            inverse_load = max(0, 100 - agent.completed_task_count)
            score += inverse_load / 100
            
            if score > best_score:
                best_score = score
                best_agent = agent
                
        return best_agent
    
    async def process_queue(self):
        """Process the task queue, assigning tasks to available agents."""
        while True:
            if not self.task_queue:
                # No tasks to process, wait a bit
                await asyncio.sleep(1)
                continue
                
            task = self.task_queue[0]
            
            # Find an available agent
            agent = self.get_available_agent(task.task_type)
            if not agent:
                # No available agents, wait and try again
                await asyncio.sleep(1)
                continue
            
            # Remove task from queue and add to running tasks
            self.task_queue.pop(0)
            self.running_tasks[task.id] = task
            
            # Save state changes if persistence enabled
            if self.use_persistence:
                await self._update_task_status(task.id, TaskStatus.RUNNING)
            
            # Execute task asynchronously
            asyncio.create_task(self._execute_task(agent, task))
    
    async def _execute_task(self, agent: Agent, task: Task):
        """Execute a task with the given agent and handle completion."""
        try:
            # Add retry logic with exponential backoff
            @retry(stop=stop_after_attempt(task.max_retries), wait=wait_exponential(multiplier=1, min=1, max=10))
            async def _execute_with_retry():
                return await agent.execute_task(task)
                
            result = await _execute_with_retry()
            
            # Update metrics
            if task.status == TaskStatus.COMPLETED:
                self.metrics["tasks_completed"] += 1
                
                # Update average completion time
                if task.runtime_seconds:
                    total_time = self.metrics["avg_completion_time"] * (self.metrics["tasks_completed"] - 1)
                    self.metrics["avg_completion_time"] = (total_time + task.runtime_seconds) / self.metrics["tasks_completed"]
            else:
                self.metrics["tasks_failed"] += 1
            
            # Move task from running to completed
            if task.id in self.running_tasks:
                del self.running_tasks[task.id]
                self.completed_tasks[task.id] = task
                
                # Update persistence
                if self.use_persistence:
                    await self._save_task(task)
                
            return result
            
        except RetryError:
            # All retries failed
            logger.error(f"All retries failed for task {task.id}")
            task.status = TaskStatus.FAILED
            task.error = "Maximum retry attempts reached"
            task.completed_at = datetime.now()
            self.metrics["tasks_failed"] += 1
            
            if task.id in self.running_tasks:
                del self.running_tasks[task.id]
                self.completed_tasks[task.id] = task
                
                # Update persistence
                if self.use_persistence:
                    await self._save_task(task)
                    
        except Exception as e:
            logger.error(f"Error executing task {task.id}: {str(e)}")
            task.status = TaskStatus.FAILED
            task.error = str(e)
            self.metrics["tasks_failed"] += 1
            
            if task.id in self.running_tasks:
                del self.running_tasks[task.id]
                self.completed_tasks[task.id] = task
                
                # Update persistence
                if self.use_persistence:
                    await self._save_task(task)
    
    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get the current status of a task."""
        # First check memory
        if task_id in self.running_tasks:
            return self.running_tasks[task_id].to_dict()
        elif task_id in self.completed_tasks:
            return self.completed_tasks[task_id].to_dict()
            
        # If persistence is enabled, try to get from Redis
        if self.use_persistence:
            try:
                task_json = await self.redis.get(f"task:{task_id}")
                if task_json:
                    task_data = json.loads(task_json)
                    return task_data
            except Exception as e:
                logger.error(f"Error retrieving task from Redis: {str(e)}")
                
        return None
    
    async def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a task if it's pending or running.
        Returns True if successfully canceled, False otherwise.
        """
        # Try to cancel from queue first
        for i, task in enumerate(self.task_queue):
            if task.id == task_id:
                canceled_task = self.task_queue.pop(i)
                canceled_task.status = TaskStatus.CANCELED
                self.completed_tasks[task_id] = canceled_task
                
                # Update persistence
                if self.use_persistence:
                    await self._save_task(canceled_task)
                    
                logger.info(f"Canceled queued task {task_id}")
                return True
                
        # Try to cancel running task
        if task_id in self.running_tasks:
            task = self.running_tasks[task_id]
            # We can't truly interrupt a running task, just mark it as canceled
            task.status = TaskStatus.CANCELED
            logger.info(f"Marked running task {task_id} as canceled")
            
            # Update persistence
            if self.use_persistence:
                await self._save_task(task)
                
            return True
            
        return False
    
    async def monitor_tasks(self):
        """Monitor running tasks for timeouts and collect metrics."""
        while True:
            current_time = datetime.now()
            
            # Check for timed-out tasks
            for task_id, task in list(self.running_tasks.items()):
                if task.started_at:
                    elapsed_seconds = (current_time - task.started_at).total_seconds()
                    if elapsed_seconds > task.timeout_seconds:
                        logger.warning(f"Task {task_id} timed out after {elapsed_seconds} seconds")
                        task.status = TaskStatus.TIMEOUT
                        task.error = "Task execution timed out"
                        task.completed_at = current_time
                        task.runtime_seconds = elapsed_seconds
                        
                        # Move from running to completed
                        del self.running_tasks[task_id]
                        self.completed_tasks[task_id] = task
                        
                        # Update persistence
                        if self.use_persistence:
                            await self._save_task(task)
                            
                        # Update metrics
                        self.metrics["tasks_failed"] += 1
            
            # Check agent health
            for agent in self.agents.values():
                # Mark agent as unhealthy if no activity for too long
                if (current_time - agent.last_active).total_seconds() > 300:  # 5 minutes
                    if agent.status == "idle":
                        if agent.health_status != "unhealthy":
                            agent.health_status = "unhealthy"
                            logger.warning(f"Agent {agent.id} marked as unhealthy due to inactivity")
                
                # Calculate agent success rate
                total_tasks = agent.completed_task_count + agent.failed_task_count
                if total_tasks > 0:
                    success_rate = agent.completed_task_count / total_tasks
                    if success_rate < 0.5 and agent.health_status != "unhealthy":
                        agent.health_status = "degraded"
                        logger.warning(f"Agent {agent.id} marked as degraded due to low success rate ({success_rate:.2f})")
                
                # Update agent persistence
                if self.use_persistence:
                    await self._save_agent(agent)
            
            await asyncio.sleep(10)  # Check every 10 seconds
    
    async def _save_task(self, task: Task):
        """Save task to Redis for persistence."""
        if not self.use_persistence:
            return
            
        try:
            task_data = task.to_dict()
            await self.redis.set(
                f"task:{task.id}", 
                json.dumps(task_data),
                ex=86400*7  # Store for 7 days
            )
            
            # Also update task lists for easier retrieval
            if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.TIMEOUT, TaskStatus.CANCELED]:
                await self.redis.zadd(
                    "completed_tasks", 
                    {task.id: task.completed_at.timestamp() if task.completed_at else 0}
                )
            elif task.status == TaskStatus.RUNNING:
                await self.redis.zadd(
                    "running_tasks",
                    {task.id: task.started_at.timestamp() if task.started_at else 0}
                )
            elif task.status == TaskStatus.PENDING:
                await self.redis.zadd(
                    "pending_tasks", 
                    {task.id: task.created_at.timestamp()}
                )
                
        except Exception as e:
            logger.error(f"Error saving task to Redis: {str(e)}")
    
    async def _save_agent(self, agent: Agent):
        """Save agent to Redis for persistence."""
        if not self.use_persistence:
            return
            
        try:
            agent_data = agent.to_dict()
            await self.redis.set(
                f"agent:{agent.id}", 
                json.dumps(agent_data),
                ex=86400  # Store for 1 day
            )
        except Exception as e:
            logger.error(f"Error saving agent to Redis: {str(e)}")
    
    async def _update_task_status(self, task_id: str, status: TaskStatus):
        """Update just the status field of a task in Redis."""
        if not self.use_persistence:
            return
            
        try:
            task_json = await self.redis.get(f"task:{task_id}")
            if task_json:
                task_data = json.loads(task_json)
                task_data["status"] = status
                await self.redis.set(
                    f"task:{task_id}", 
                    json.dumps(task_data),
                    ex=86400*7  # Store for 7 days
                )
        except Exception as e:
            logger.error(f"Error updating task status in Redis: {str(e)}")
    
    async def _restore_state_from_persistence(self):
        """Restore agent manager state from Redis on startup."""
        if not self.use_persistence:
            return
            
        try:
            # Restore running tasks
            running_task_ids = await self.redis.zrange("running_tasks", 0, -1)
            for task_id in running_task_ids:
                task_json = await self.redis.get(f"task:{task_id.decode('utf-8')}")
                if task_json:
                    task_data = json.loads(task_json)
                    task = Task.from_dict(task_data)
                    # Tasks that were running before should be requened
                    task.status = TaskStatus.PENDING
                    await self.add_task(task)
                    
            # Restore pending tasks
            pending_task_ids = await self.redis.zrange("pending_tasks", 0, -1)
            for task_id in pending_task_ids:
                task_json = await self.redis.get(f"task:{task_id.decode('utf-8')}")
                if task_json:
                    task_data = json.loads(task_json)
                    task = Task.from_dict(task_data)
                    await self.add_task(task)
                    
            # Restore agents (optional)
            agent_keys = await self.redis.keys("agent:*")
            for key in agent_keys:
                agent_id = key.decode("utf-8").split(":", 1)[1]
                agent_json = await self.redis.get(f"agent:{agent_id}")
                if agent_json:
                    agent_data = json.loads(agent_json)
                    agent = Agent.from_dict(agent_data)
                    self.agents[agent_id] = agent
                    
            logger.info(f"Restored {len(self.task_queue)} pending tasks and {len(self.agents)} agents from persistent storage")
            
        except Exception as e:
            logger.error(f"Error restoring state from Redis: {str(e)}")
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get system metrics and statistics."""
        metrics = {
            **self.metrics,  # Include base metrics
            "queue_length": len(self.task_queue),
            "running_tasks": len(self.running_tasks),
            "completed_tasks": len(self.completed_tasks),
            "active_agents": sum(1 for a in self.agents.values() if a.status == "busy"),
            "total_agents": len(self.agents),
            "healthy_agents": sum(1 for a in self.agents.values() if a.health_status == "healthy"),
            "agent_types": {}
        }
        
        # Count agents by type
        for agent in self.agents.values():
            if agent.agent_type not in metrics["agent_types"]:
                metrics["agent_types"][agent.agent_type] = 0
            metrics["agent_types"][agent.agent_type] += 1
            
        return metrics
    
    async def start(self):
        """Start the agent manager."""
        logger.info(f"Starting agent manager with max {self.max_agents} agents")
        
        # Restore state from Redis if persistence is enabled
        if self.use_persistence:
            await self._restore_state_from_persistence()
        
        # Create initial pool of agents if none were restored
        if not self.agents:
            # Create a mix of different agent types
            for _ in range(max(1, self.max_agents // 5)):
                await self.register_agent(AgentType.GENERAL)
                
            for _ in range(max(1, self.max_agents // 5)):
                await self.register_agent(AgentType.RESEARCHER, ["research", "data_collection"])
                
            for _ in range(max(1, self.max_agents // 5)):
                await self.register_agent(AgentType.WRITER, ["content_creation", "summarization"])
                
            for _ in range(max(1, self.max_agents // 5)):
                await self.register_agent(AgentType.CODER, ["code_generation", "debugging"])
                
            for _ in range(max(1, self.max_agents // 5)):
                await self.register_agent(AgentType.ANALYST, ["data_analysis", "insight_generation"])
            
        # Start task processing and monitoring
        await asyncio.gather(
            self.process_queue(),
            self.monitor_tasks()
        )


# Create a global instance of the agent manager
agent_manager = AgentManager() 