#!/usr/bin/env python3
"""
Test script for the Live Workflow Demo functionality.
This script tests the real OpenAI API integration and workflow execution.
"""

import asyncio
import httpx
import json
import time
import os
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")

def print_step(text: str) -> None:
    """Print a formatted step."""
    print(f"\n🔸 {text}")

def print_success(text: str) -> None:
    """Print a success message."""
    print(f"✅ {text}")

def print_error(text: str) -> None:
    """Print an error message."""
    print(f"❌ {text}")

def print_info(text: str) -> None:
    """Print an info message."""
    print(f"ℹ️  {text}")

async def test_backend_connection() -> bool:
    """Test if the backend is running and accessible."""
    print_step("Testing backend connection...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/")
            if response.status_code == 200:
                print_success("Backend is running and accessible")
                return True
            else:
                print_error(f"Backend returned status code: {response.status_code}")
                return False
    except Exception as e:
        print_error(f"Failed to connect to backend: {str(e)}")
        return False

async def test_workflow_execution() -> bool:
    """Test the complete workflow execution with real API calls."""
    print_step("Testing workflow execution...")
    
    # Prepare test data
    test_request = {
        "project_description": "Build a simple Python web API with FastAPI that manages a todo list",
        "programming_language": "Python",
        "workflow_type": "full_development",
        "code_sample": """
def get_todos():
    # Simple function that could be optimized
    todos = []
    for i in range(100):
        if i % 2 == 0:
            todos.append(f"Todo {i}")
    return todos
"""
    }
    
    try:
        async with httpx.AsyncClient() as client:
            # Start workflow
            print_info("Starting workflow execution...")
            response = await client.post(
                f"{API_BASE_URL}/workflow/execute",
                json=test_request,
                timeout=10.0
            )
            
            if response.status_code != 200:
                print_error(f"Failed to start workflow: {response.status_code} - {response.text}")
                return False
            
            result = response.json()
            workflow_id = result.get("workflow_id")
            
            if not workflow_id:
                print_error("No workflow_id returned from start request")
                return False
            
            print_success(f"Workflow started with ID: {workflow_id}")
            
            # Poll for status updates
            print_info("Polling for workflow status updates...")
            max_attempts = 60  # Maximum 60 seconds
            attempt = 0
            
            while attempt < max_attempts:
                status_response = await client.get(
                    f"{API_BASE_URL}/workflow/status/{workflow_id}",
                    timeout=10.0
                )
                
                if status_response.status_code != 200:
                    print_error(f"Failed to get status: {status_response.status_code}")
                    return False
                
                status_data = status_response.json()
                workflow_status = status_data.get("status")
                current_step = status_data.get("current_step", 0)
                total_steps = status_data.get("total_steps", 5)
                
                print(f"📊 Step {current_step}/{total_steps} - Status: {workflow_status}")
                
                # Show individual step progress
                steps = status_data.get("steps", [])
                for step in steps:
                    step_status = step.get("status", "pending")
                    agent_name = step.get("agent_name", "Unknown")
                    
                    if step_status == "completed":
                        print(f"   ✅ {agent_name}: Completed")
                    elif step_status == "running":
                        print(f"   🔄 {agent_name}: Running...")
                    elif step_status == "failed":
                        error = step.get("error", "Unknown error")
                        print(f"   ❌ {agent_name}: Failed - {error}")
                    else:
                        print(f"   ⏳ {agent_name}: Pending")
                
                if workflow_status in ["completed", "failed"]:
                    break
                
                await asyncio.sleep(2)
                attempt += 1
            
            if workflow_status == "completed":
                print_success("Workflow completed successfully!")
                
                # Display results summary
                results = status_data.get("results", {})
                print_info(f"Results generated for {len(results)} agents:")
                
                for agent_key, result in results.items():
                    agent = result.get("agent", agent_key)
                    print(f"   🤖 {agent}")
                    
                    # Show specific metrics for each agent
                    if agent == "CodeOptimizer":
                        score = result.get("optimization_score", "N/A")
                        improvement = result.get("estimated_improvement", "N/A")
                        print(f"      📈 Optimization Score: {score}/100")
                        print(f"      ⚡ Estimated Improvement: {improvement}")
                    
                    elif agent == "SecurityAnalyzer":
                        score = result.get("security_score", "N/A")
                        vulnerabilities = result.get("vulnerabilities_found", "N/A")
                        print(f"      🔒 Security Score: {score}/100")
                        print(f"      🚨 Vulnerabilities Found: {vulnerabilities}")
                    
                    elif agent == "TestGenerator":
                        test_cases = result.get("test_cases_generated", "N/A")
                        automation = result.get("automation_score", "N/A")
                        print(f"      🧪 Test Cases Generated: {test_cases}")
                        print(f"      🤖 Automation Score: {automation}%")
                    
                    elif agent == "DocGenerator":
                        doc_score = result.get("documentation_score", "N/A")
                        completeness = result.get("completeness", "N/A")
                        print(f"      📚 Documentation Score: {doc_score}/100")
                        print(f"      📋 Completeness: {completeness}")
                
                return True
            
            else:
                print_error(f"Workflow failed or timed out. Final status: {workflow_status}")
                return False
    
    except Exception as e:
        print_error(f"Error during workflow execution: {str(e)}")
        return False

async def test_openai_integration() -> bool:
    """Test if OpenAI API integration is working."""
    print_step("Testing OpenAI API integration...")
    
    if not OPENAI_API_KEY:
        print_error("OPENAI_API_KEY environment variable not set")
        return False
    
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user",
                        "content": "Say 'Hello from Monk-AI!' if you can read this message."
                    }
                ],
                "max_tokens": 50,
                "temperature": 0.1
            }
            
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result["choices"][0]["message"]["content"]
                print_success(f"OpenAI API integration working. Response: {message}")
                return True
            else:
                print_error(f"OpenAI API error: {response.status_code} - {response.text}")
                return False
                
    except Exception as e:
        print_error(f"Error testing OpenAI integration: {str(e)}")
        return False

async def main():
    """Main test function."""
    print_header("🤖 Monk-AI Live Workflow Demo Test Suite")
    
    print_info("This test suite verifies the complete functionality of the Live Workflow Demo")
    print_info("including backend connectivity, OpenAI API integration, and workflow execution.")
    
    # Test results
    tests = {
        "Backend Connection": False,
        "OpenAI Integration": False,
        "Workflow Execution": False
    }
    
    # Run tests
    tests["Backend Connection"] = await test_backend_connection()
    
    if tests["Backend Connection"]:
        tests["OpenAI Integration"] = await test_openai_integration()
        
        if tests["OpenAI Integration"]:
            tests["Workflow Execution"] = await test_workflow_execution()
    
    # Summary
    print_header("📋 Test Results Summary")
    
    all_passed = True
    for test_name, passed in tests.items():
        if passed:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
            all_passed = False
    
    if all_passed:
        print_header("🎉 ALL TESTS PASSED!")
        print_info("The Live Workflow Demo is ready for use!")
        print_info("You can now access the frontend at http://localhost:3000")
        print_info("Navigate to the 'Live Demo' tab to experience the full workflow.")
    else:
        print_header("❌ SOME TESTS FAILED")
        print_info("Please check the error messages above and fix the issues.")
        print_info("Make sure:")
        print_info("  1. Backend is running on http://localhost:8000")
        print_info("  2. OPENAI_API_KEY environment variable is set")
        print_info("  3. Internet connection is available for OpenAI API calls")

if __name__ == "__main__":
    asyncio.run(main()) 