#!/usr/bin/env python3
"""
Comprehensive test script for the multi-agent system
Tests actual functionality with real OpenAI API integration
"""

import asyncio
import os
import sys
import json
import httpx
from typing import Dict, Any, List
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Import our components
try:
    from app.core.ai_service import MultiProviderAIService, ai_service
    from app.agents.ideation import Ideation
    from app.core.config import settings
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)

class MultiAgentSystemTester:
    """Comprehensive tester for the multi-agent system"""
    
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.results = {}
        
    async def test_environment_setup(self) -> Dict[str, Any]:
        """Test if environment is properly configured"""
        print("🔍 Testing environment setup...")
        
        tests = {
            "openai_api_key": bool(os.getenv("OPENAI_API_KEY")),
            "settings_loaded": hasattr(settings, 'OPENAI_API_KEY'),
            "ai_service_initialized": ai_service is not None,
            "providers_available": len(ai_service.providers) > 0 if ai_service else False
        }
        
        for test_name, result in tests.items():
            status = "✅" if result else "❌"
            print(f"  {status} {test_name}: {result}")
        
        return tests
    
    async def test_ai_service_direct(self) -> Dict[str, Any]:
        """Test AI service directly (not through API)"""
        print("\n🤖 Testing AI service directly...")
        
        try:
            # Test basic response generation
            response = await ai_service.generate_response(
                prompt="Hello! Please respond with 'AI Service Working' to confirm you're functional.",
                max_tokens=50,
                temperature=0.3
            )
            
            print(f"  ✅ AI Service Response: {response.get('response', 'No response')[:100]}...")
            print(f"  ✅ Provider Used: {response.get('provider', 'Unknown')}")
            print(f"  ✅ Model Used: {response.get('model', 'Unknown')}")
            
            return {
                "status": "success",
                "response": response,
                "working": True
            }
            
        except Exception as e:
            print(f"  ❌ AI Service Error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "working": False
            }
    
    async def test_ideation_agent_direct(self) -> Dict[str, Any]:
        """Test ideation agent directly"""
        print("\n💡 Testing Ideation Agent directly...")
        
        try:
            ideation_agent = Ideation()
            
            # Test project scope generation
            project_scope = await ideation_agent.generate_project_scope(
                description="Build a simple task management app with user authentication",
                template_key="web_app"
            )
            
            print(f"  ✅ Project Scope Generated:")
            print(f"    - Overview: {project_scope.get('project_overview', 'N/A')[:100]}...")
            print(f"    - Features: {len(project_scope.get('key_features', []))} features")
            
            # Test technical specs generation
            tech_specs = await ideation_agent.generate_technical_specs(project_scope)
            
            print(f"  ✅ Technical Specs Generated:")
            print(f"    - Architecture: {tech_specs.get('system_architecture', {}).get('frontend', 'N/A')}")
            print(f"    - Models: {len(tech_specs.get('data_models', []))} data models")
            
            # Test user stories generation
            user_stories = await ideation_agent.generate_user_stories(project_scope)
            
            print(f"  ✅ User Stories Generated: {len(user_stories)} stories")
            if user_stories:
                print(f"    - First Story: {user_stories[0].get('i_want_to', 'N/A')[:50]}...")
            
            return {
                "status": "success",
                "project_scope": project_scope,
                "tech_specs": tech_specs,
                "user_stories": user_stories,
                "working": True
            }
            
        except Exception as e:
            print(f"  ❌ Ideation Agent Error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "working": False
            }
    
    async def test_api_endpoints(self) -> Dict[str, Any]:
        """Test API endpoints"""
        print("\n🌐 Testing API endpoints...")
        
        endpoints_to_test = [
            ("GET", "/api/agents/status", None),
            ("GET", "/api/agents/health", None),
            ("POST", "/api/agents/ideate", {
                "description": "Build a simple task management app with user authentication",
                "template_key": "web_app"
            })
        ]
        
        results = {}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for method, endpoint, payload in endpoints_to_test:
                try:
                    url = f"{self.base_url}{endpoint}"
                    
                    if method == "GET":
                        response = await client.get(url)
                    elif method == "POST":
                        response = await client.post(url, json=payload)
                    
                    status = "✅" if response.status_code == 200 else "❌"
                    print(f"  {status} {method} {endpoint}: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if endpoint == "/api/agents/ideate" and "project_scope" in data:
                                print(f"    - Project scope generated successfully")
                                print(f"    - Technical specs: {'✅' if 'technical_specs' in data else '❌'}")
                        except:
                            pass
                    
                    results[endpoint] = {
                        "status_code": response.status_code,
                        "success": response.status_code == 200,
                        "response_size": len(response.content) if response.content else 0
                    }
                    
                except Exception as e:
                    print(f"  ❌ {method} {endpoint}: Error - {str(e)}")
                    results[endpoint] = {
                        "status_code": 0,
                        "success": False,
                        "error": str(e)
                    }
        
        return results
    
    async def test_full_workflow(self) -> Dict[str, Any]:
        """Test complete end-to-end workflow"""
        print("\n🔄 Testing full multi-agent workflow...")
        
        try:
            # Test the complete ideation workflow
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/agents/ideate",
                    json={
                        "description": "Create a modern e-commerce platform with shopping cart, payment processing, and order management",
                        "template_key": "web_app"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    print(f"  ✅ Full workflow completed successfully")
                    print(f"  ✅ Project Scope: {bool(data.get('project_scope'))}")
                    print(f"  ✅ Technical Specs: {bool(data.get('technical_specs'))}")
                    print(f"  ✅ User Stories: {len(data.get('user_stories', []))} stories")
                    
                    # Show some details
                    if 'project_scope' in data:
                        scope = data['project_scope']
                        print(f"    - Features: {len(scope.get('key_features', []))}")
                        print(f"    - Timeline: {scope.get('timeline_estimates', {}).get('development_phase', 'N/A')}")
                    
                    return {
                        "status": "success",
                        "data": data,
                        "working": True
                    }
                else:
                    print(f"  ❌ Workflow failed with status: {response.status_code}")
                    print(f"    Response: {response.text[:200]}...")
                    
                    return {
                        "status": "error",
                        "status_code": response.status_code,
                        "response": response.text,
                        "working": False
                    }
                    
        except Exception as e:
            print(f"  ❌ Full workflow error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "working": False
            }
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return comprehensive results"""
        print("🚀 Starting comprehensive multi-agent system test...\n")
        
        # Run all tests
        env_results = await self.test_environment_setup()
        ai_results = await self.test_ai_service_direct()
        ideation_results = await self.test_ideation_agent_direct()
        api_results = await self.test_api_endpoints()
        workflow_results = await self.test_full_workflow()
        
        # Compile final results
        overall_results = {
            "timestamp": datetime.now().isoformat(),
            "environment_setup": env_results,
            "ai_service_direct": ai_results,
            "ideation_agent_direct": ideation_results,
            "api_endpoints": api_results,
            "full_workflow": workflow_results,
            "summary": {
                "environment_ok": all(env_results.values()),
                "ai_service_working": ai_results.get("working", False),
                "ideation_agent_working": ideation_results.get("working", False),
                "api_endpoints_working": any(result.get("success", False) for result in api_results.values()),
                "full_workflow_working": workflow_results.get("working", False)
            }
        }
        
        # Print summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        summary = overall_results["summary"]
        for test_name, result in summary.items():
            status = "✅" if result else "❌"
            print(f"{status} {test_name.replace('_', ' ').title()}: {result}")
        
        overall_success = all(summary.values())
        print(f"\n🎯 Overall System Status: {'✅ WORKING' if overall_success else '❌ NEEDS FIXES'}")
        
        return overall_results

async def main():
    """Main test function"""
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable is not set!")
        print("Please set your OpenAI API key in a .env file or environment variable")
        print("Example: export OPENAI_API_KEY='your-openai-api-key-here'")
        return
    
    tester = MultiAgentSystemTester()
    results = await tester.run_all_tests()
    
    # Save results to file
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📝 Full test results saved to: test_results.json")

if __name__ == "__main__":
    asyncio.run(main())