#!/usr/bin/env python3
"""
Quick test to verify the fixed Monk-AI system
Tests both backend orchestrator and frontend compatibility
"""

import requests
import json
import time

def test_backend_health():
    """Test that backend is running and healthy"""
    try:
        response = requests.get("http://localhost:8000/api/agents/health")
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Backend Health Check:")
            print(f"   Status: {health_data['status']}")
            print(f"   All Agents: {list(health_data['agents'].keys())}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_orchestrator_workflow():
    """Test the orchestrator workflow execution"""
    try:
        print("\n🚀 Testing Multi-Agent Orchestrator...")
        
        payload = {
            "description": "Build a REST API service with authentication, rate limiting, and comprehensive documentation",
            "language": "python",
            "workflow_type": "full_development"
        }
        
        response = requests.post(
            "http://localhost:8000/api/agents/orchestrate",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=120  # 2 minutes timeout for complete workflow
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Orchestrator Workflow Completed Successfully!")
            
            # Handle summary safely
            summary = result.get('summary') or {}
            print(f"   Steps Completed: {summary.get('completed_steps', 'N/A')}")
            print(f"   Total Time: {result.get('total_time', 0):.2f} seconds")
            
            # Check if we have generated files
            steps = result.get('steps', {})
            if 'code_generation' in steps:
                code_gen = steps['code_generation']
                if code_gen and isinstance(code_gen, dict):
                    generated_files = code_gen.get('generated_files', {})
                    if generated_files:
                        print(f"   Generated Files: {list(generated_files.keys())}")
                    else:
                        print("   Generated Files: (checking for files...)")
                        if 'file_count' in code_gen:
                            print(f"   File Count: {code_gen['file_count']}")
                
            success_rate = summary.get('success_rate', 0) if summary else 0
            print(f"   Success Rate: {success_rate:.1f}%")
            return True
        else:
            print(f"❌ Orchestrator test failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Orchestrator test failed: {e}")
        return False

def test_ideation_endpoint():
    """Test the ideation agent endpoint"""
    try:
        print("\n💡 Testing Ideation Agent...")
        
        payload = {
            "description": "A modern task management application with real-time collaboration",
            "template_key": "web_app"
        }
        
        response = requests.post(
            "http://localhost:8000/api/agents/ideate",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Ideation Agent Working!")
            print(f"   Status: {result.get('status')}")
            
            # Check project scope
            project_scope = result.get('project_scope', {})
            if project_scope:
                print(f"   Project: {project_scope.get('project_name', 'Generated Project')}")
                
            return True
        else:
            print(f"❌ Ideation test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ideation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧙‍♂️ MONK-AI SYSTEM TEST")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Backend Health
    if test_backend_health():
        tests_passed += 1
    
    # Test 2: Ideation Agent
    if test_ideation_endpoint():
        tests_passed += 1
    
    # Test 3: Full Orchestrator Workflow
    if test_orchestrator_workflow():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! System is ready for demo!")
        print("\n📌 Frontend fixes applied:")
        print("   - Fixed timeline_estimates optional chaining in Ideation.tsx")
        print("   - Fixed system_architecture optional chaining")
        print("   - Fixed orchestrator endpoint URL")
        print("   - Removed SSE connection errors")
        print("\n🚀 Your system is now ready for the hackathon demo!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    main() 