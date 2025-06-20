#!/usr/bin/env python3
"""
Test script for the Multi-Agent Orchestrator
"""

import asyncio
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

async def test_orchestrator():
    """Test the orchestrator functionality"""
    print("🧪 Testing Multi-Agent Orchestrator...")
    
    try:
        from app.agents.orchestrator import AgentOrchestrator
        
        # Initialize orchestrator
        orchestrator = AgentOrchestrator()
        print("✅ Orchestrator initialized successfully")
        
        # Test available workflows
        workflows = orchestrator.get_available_workflows()
        print(f"✅ Available workflows: {len(workflows)}")
        for workflow_id, workflow_info in workflows.items():
            print(f"   - {workflow_info['name']}: {workflow_info['estimated_time']}")
        
        # Test workflow execution
        print("\n🚀 Testing workflow execution...")
        test_input = {
            "description": "A simple task management app with user authentication",
            "language": "python"
        }
        
        result = await orchestrator.execute_workflow("full_development", test_input)
        
        if result.success:
            print("✅ Workflow executed successfully!")
            print(f"   - Total time: {result.total_time:.2f}s")
            print(f"   - Steps completed: {result.summary['completed_steps']}/{result.summary['total_steps']}")
            print(f"   - Success rate: {result.summary['success_rate']:.1%}")
        else:
            print(f"❌ Workflow failed: {result.error_message}")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

async def test_individual_agents():
    """Test individual agents"""
    print("\n🤖 Testing individual agents...")
    
    try:
        from app.agents.ideation import Ideation
        from app.agents.code_optimizer import CodeOptimizer
        
        # Test Ideation Agent
        ideation = Ideation()
        project_scope = await ideation.generate_project_scope("A task management app")
        print("✅ Ideation Agent working")
        
        # Test Code Optimizer
        optimizer = CodeOptimizer()
        sample_code = "def hello(): print('Hello World')"
        result = await optimizer.optimize_code(sample_code, "python")
        print("✅ Code Optimizer working")
        
    except Exception as e:
        print(f"❌ Agent test failed: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Monk-AI Orchestrator Tests\n")
    
    # Run tests
    asyncio.run(test_orchestrator())
    asyncio.run(test_individual_agents())
    
    print("\n✅ All tests completed!") 