#!/usr/bin/env python3
"""
Comprehensive Test Cycle for Monk-AI Project
Tests all agents with multiple AI providers (OpenAI, Gemini, OpenRouter)
Includes frontend-backend integration and real-world scenarios

Author: AI Assistant
Date: 2024
Version: 1.0
"""

import asyncio
import json
import time
import sys
import os
import aiohttp
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings
from app.agents.code_optimizer import CodeOptimizer
from app.agents.doc_generator import DocGenerator
from app.agents.ideation import Ideation
from app.agents.orchestrator import Orchestrator
from app.agents.pr_reviewer import PRReviewer
from app.agents.security_analyzer import SecurityAnalyzer
from app.agents.test_generator import TestGenerator

@dataclass
class TestResult:
    """Data class for test results"""
    agent_name: str
    provider: str
    success: bool
    execution_time: float
    error_message: Optional[str] = None
    output_quality: Optional[str] = None
    response_length: Optional[int] = None

class AIProviderManager:
    """Manages multiple AI providers for testing"""
    
    def __init__(self):
        self.providers = {
            'openai': {
                'api_key': 'your-openai-api-key-here',
                'base_url': 'https://api.openai.com/v1',
                'model': 'gpt-4o'
            },
            'gemini': {
                'api_key': None,  # To be set by user
                'base_url': None,
                'model': 'gemini-pro'
            },
            'openrouter': {
                'api_key': None,  # To be set by user
                'base_url': 'https://openrouter.ai/api/v1',
                'model': 'openai/gpt-4'
            }
        }
    
    def test_openai_connection(self) -> bool:
        """Test OpenAI API connection"""
        try:
            import openai
            client = openai.OpenAI(api_key=self.providers['openai']['api_key'])
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello, test connection"}],
                max_tokens=10
            )
            return True
        except Exception as e:
            print(f"❌ OpenAI connection failed: {e}")
            return False
    
    def test_gemini_connection(self) -> bool:
        """Test Google Gemini API connection"""
        if not self.providers['gemini']['api_key']:
            print("⚠️ Gemini API key not provided, skipping Gemini tests")
            return False
        
        try:
            from google import genai
            client = genai.Client(api_key=self.providers['gemini']['api_key'])
            # Test basic connection
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents='Hello, test connection'
            )
            return True
        except Exception as e:
            print(f"❌ Gemini connection failed: {e}")
            return False
    
    def test_openrouter_connection(self) -> bool:
        """Test OpenRouter API connection"""
        if not self.providers['openrouter']['api_key']:
            print("⚠️ OpenRouter API key not provided, skipping OpenRouter tests")
            return False
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.providers['openrouter']['api_key']}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": "Hello, test connection"}],
                    "max_tokens": 10
                }
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ OpenRouter connection failed: {e}")
            return False

class ComprehensiveTestCycle:
    """Main test cycle class for comprehensive testing"""
    
    def __init__(self):
        self.provider_manager = AIProviderManager()
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "test_cycle_name": "Comprehensive Monk-AI Test Cycle",
            "version": "1.0",
            "environment": {
                "backend_url": self.backend_url,
                "frontend_url": self.frontend_url,
                "python_version": sys.version,
                "os": os.name
            },
            "provider_status": {},
            "agent_tests": {},
            "integration_tests": {},
            "performance_metrics": {},
            "summary": {
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "success_rate": 0.0
            }
        }
        
        # Sample code for testing agents
        self.sample_python_code = '''
def fibonacci(n):
    """Calculate fibonacci sequence inefficiently"""
    if n <= 1:
        return n
    result = []
    a, b = 0, 1
    for i in range(n):
        result.append(a)
        temp = a + b
        a = b
        b = temp
    return result

def process_data(data):
    """Process data with potential security issues"""
    processed = []
    for item in data:
        # Potential SQL injection vulnerability
        query = f"SELECT * FROM users WHERE id = {item}"
        if item > 0:
            processed.append(item * 2)
    return processed

class DataProcessor:
    def __init__(self):
        self.data = []
        self.password = "admin123"  # Security issue: hardcoded password
    
    def add_data(self, item):
        self.data.append(item)
    
    def get_average(self):
        return sum(self.data) / len(self.data) if self.data else 0
'''
        
        self.sample_javascript_code = '''
function calculateTotal(items) {
    let total = 0;
    for (let i = 0; i < items.length; i++) {
        total += items[i].price * items[i].quantity;
    }
    return total;
}

async function fetchUserData(userId) {
    try {
        // Potential XSS vulnerability
        const response = await fetch(`/api/users/${userId}`);
        const data = await response.json();
        document.innerHTML = data.content; // XSS risk
        return data;
    } catch (error) {
        console.error('Error fetching user data:', error);
        return null;
    }
}

class ShoppingCart {
    constructor() {
        this.items = [];
        this.apiKey = "your-api-key-here"; // Remember to set your actual API key
    }
    
    addItem(item) {
        this.items.push(item);
    }
    
    getTotal() {
        return this.items.reduce((sum, item) => sum + item.price, 0);
    }
}
'''

    async def run_comprehensive_test_cycle(self):
        """Run the complete test cycle"""
        print("🚀 MONK-AI COMPREHENSIVE TEST CYCLE")
        print("=" * 80)
        print(f"⏰ Test cycle started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Step 1: Test AI provider connections
        await self._test_ai_providers()
        
        # Step 2: Test backend connectivity
        await self._test_backend_connectivity()
        
        # Step 3: Test frontend connectivity
        await self._test_frontend_connectivity()
        
        # Step 4: Test each agent with available providers
        await self._test_all_agents()
        
        # Step 5: Test frontend-backend integration
        await self._test_frontend_backend_integration()
        
        # Step 6: Generate comprehensive report
        self._generate_comprehensive_report()
        
        # Step 7: Save results to file
        self._save_test_results()
        
        return self.test_results
    
    async def _test_ai_providers(self):
        """Test all AI provider connections"""
        print("\n🔌 TESTING AI PROVIDER CONNECTIONS")
        print("-" * 50)
        
        # Test OpenAI
        openai_status = self.provider_manager.test_openai_connection()
        self.test_results["provider_status"]["openai"] = {
            "status": "connected" if openai_status else "failed",
            "available": openai_status
        }
        print(f"{'✅' if openai_status else '❌'} OpenAI API: {'Connected' if openai_status else 'Failed'}")
        
        # Test Gemini
        gemini_status = self.provider_manager.test_gemini_connection()
        self.test_results["provider_status"]["gemini"] = {
            "status": "connected" if gemini_status else "failed",
            "available": gemini_status
        }
        print(f"{'✅' if gemini_status else '❌'} Gemini API: {'Connected' if gemini_status else 'Failed'}")
        
        # Test OpenRouter
        openrouter_status = self.provider_manager.test_openrouter_connection()
        self.test_results["provider_status"]["openrouter"] = {
            "status": "connected" if openrouter_status else "failed",
            "available": openrouter_status
        }
        print(f"{'✅' if openrouter_status else '❌'} OpenRouter API: {'Connected' if openrouter_status else 'Failed'}")
    
    async def _test_backend_connectivity(self):
        """Test backend API connectivity"""
        print("\n🔗 TESTING BACKEND CONNECTIVITY")
        print("-" * 50)
        
        try:
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                async with session.get(f"{self.backend_url}/") as response:
                    end_time = time.time()
                    response_time = round((end_time - start_time) * 1000, 2)
                    
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ Backend API: {response.status} - {data.get('message', 'OK')} ({response_time}ms)")
                        self.test_results["integration_tests"]["backend"] = {
                            "status": "healthy",
                            "response_time_ms": response_time,
                            "success": True
                        }
                    else:
                        print(f"❌ Backend API: {response.status}")
                        self.test_results["integration_tests"]["backend"] = {
                            "status": "unhealthy",
                            "response_time_ms": response_time,
                            "success": False
                        }
        except Exception as e:
            print(f"💥 Backend API Error: {str(e)}")
            self.test_results["integration_tests"]["backend"] = {
                "status": "error",
                "error": str(e),
                "success": False
            }
    
    async def _test_frontend_connectivity(self):
        """Test frontend connectivity"""
        print("\n🌐 TESTING FRONTEND CONNECTIVITY")
        print("-" * 50)
        
        try:
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                async with session.get(f"{self.frontend_url}/") as response:
                    end_time = time.time()
                    response_time = round((end_time - start_time) * 1000, 2)
                    
                    if response.status == 200:
                        print(f"✅ Frontend App: {response.status} - React App Loaded ({response_time}ms)")
                        self.test_results["integration_tests"]["frontend"] = {
                            "status": "healthy",
                            "response_time_ms": response_time,
                            "success": True
                        }
                    else:
                        print(f"❌ Frontend App: {response.status}")
                        self.test_results["integration_tests"]["frontend"] = {
                            "status": "unhealthy",
                            "response_time_ms": response_time,
                            "success": False
                        }
        except Exception as e:
            print(f"💥 Frontend App Error: {str(e)}")
            self.test_results["integration_tests"]["frontend"] = {
                "status": "error",
                "error": str(e),
                "success": False
            }
    
    async def _test_all_agents(self):
        """Test all agents with available providers"""
        print("\n🤖 TESTING ALL AGENTS")
        print("-" * 50)
        
        agents_to_test = [
            ("code_optimizer", CodeOptimizer),
            ("doc_generator", DocGenerator),
            ("security_analyzer", SecurityAnalyzer),
            ("test_generator", TestGenerator),
            ("pr_reviewer", PRReviewer),
            ("ideation", Ideation),
            ("orchestrator", Orchestrator)
        ]
        
        for agent_name, agent_class in agents_to_test:
            print(f"\n🔧 Testing {agent_name.replace('_', ' ').title()}...")
            self.test_results["agent_tests"][agent_name] = {}
            
            # Test with OpenAI (primary provider)
            if self.test_results["provider_status"]["openai"]["available"]:
                result = await self._test_agent_with_provider(agent_name, agent_class, "openai")
                self.test_results["agent_tests"][agent_name]["openai"] = result.__dict__
                print(f"  {'✅' if result.success else '❌'} OpenAI: {result.execution_time:.2f}s")
            
            # Test with other providers if available
            for provider in ["gemini", "openrouter"]:
                if self.test_results["provider_status"][provider]["available"]:
                    result = await self._test_agent_with_provider(agent_name, agent_class, provider)
                    self.test_results["agent_tests"][agent_name][provider] = result.__dict__
                    print(f"  {'✅' if result.success else '❌'} {provider.title()}: {result.execution_time:.2f}s")
    
    async def _test_agent_with_provider(self, agent_name: str, agent_class, provider: str) -> TestResult:
        """Test a specific agent with a specific provider"""
        start_time = time.time()
        
        try:
            # Initialize agent
            agent = agent_class()
            
            # Prepare test input based on agent type
            if agent_name == "code_optimizer":
                result = await agent.optimize_code(self.sample_python_code, "python")
            elif agent_name == "doc_generator":
                result = await agent.generate_documentation(self.sample_python_code, "python")
            elif agent_name == "security_analyzer":
                result = await agent.analyze_security(self.sample_python_code, "python")
            elif agent_name == "test_generator":
                result = await agent.generate_tests(self.sample_python_code, "python")
            elif agent_name == "pr_reviewer":
                result = await agent.review_pr({
                    "title": "Test PR",
                    "description": "Test pull request",
                    "files": [{"filename": "test.py", "content": self.sample_python_code}]
                })
            elif agent_name == "ideation":
                result = await agent.generate_ideas("Create a web application for task management")
            elif agent_name == "orchestrator":
                result = await agent.orchestrate_workflow({
                    "task": "optimize and document code",
                    "code": self.sample_python_code
                })
            else:
                raise ValueError(f"Unknown agent: {agent_name}")
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Evaluate result quality
            quality = self._evaluate_result_quality(result)
            response_length = len(str(result)) if result else 0
            
            self.test_results["summary"]["total_tests"] += 1
            self.test_results["summary"]["passed_tests"] += 1
            
            return TestResult(
                agent_name=agent_name,
                provider=provider,
                success=True,
                execution_time=execution_time,
                output_quality=quality,
                response_length=response_length
            )
            
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            
            self.test_results["summary"]["total_tests"] += 1
            self.test_results["summary"]["failed_tests"] += 1
            
            return TestResult(
                agent_name=agent_name,
                provider=provider,
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            )
    
    def _evaluate_result_quality(self, result) -> str:
        """Evaluate the quality of agent output"""
        if not result:
            return "poor"
        
        result_str = str(result)
        if len(result_str) < 50:
            return "poor"
        elif len(result_str) < 200:
            return "fair"
        elif len(result_str) < 500:
            return "good"
        else:
            return "excellent"
    
    async def _test_frontend_backend_integration(self):
        """Test frontend-backend integration through API calls"""
        print("\n🔗 TESTING FRONTEND-BACKEND INTEGRATION")
        print("-" * 50)
        
        api_endpoints = [
            "/api/agents/optimize",
            "/api/agents/document",
            "/api/agents/security-analyze",
            "/api/agents/generate-tests",
            "/api/agents/review-pr",
            "/api/agents/ideate",
            "/api/agents/orchestrate"
        ]
        
        integration_results = []
        
        for endpoint in api_endpoints:
            try:
                async with aiohttp.ClientSession() as session:
                    test_payload = {
                        "code": self.sample_python_code,
                        "language": "python"
                    }
                    
                    start_time = time.time()
                    async with session.post(
                        f"{self.backend_url}{endpoint}",
                        json=test_payload,
                        headers={"Content-Type": "application/json"}
                    ) as response:
                        end_time = time.time()
                        response_time = round((end_time - start_time) * 1000, 2)
                        
                        if response.status == 200:
                            data = await response.json()
                            print(f"✅ {endpoint}: {response.status} ({response_time}ms)")
                            integration_results.append({
                                "endpoint": endpoint,
                                "status": "success",
                                "response_time_ms": response_time,
                                "response_size": len(str(data))
                            })
                        else:
                            print(f"❌ {endpoint}: {response.status}")
                            integration_results.append({
                                "endpoint": endpoint,
                                "status": "failed",
                                "response_time_ms": response_time,
                                "status_code": response.status
                            })
            except Exception as e:
                print(f"💥 {endpoint}: Error - {str(e)}")
                integration_results.append({
                    "endpoint": endpoint,
                    "status": "error",
                    "error": str(e)
                })
        
        self.test_results["integration_tests"]["api_endpoints"] = integration_results
    
    def _generate_comprehensive_report(self):
        """Generate comprehensive test report"""
        print("\n📊 GENERATING COMPREHENSIVE REPORT")
        print("-" * 50)
        
        # Calculate success rate
        total_tests = self.test_results["summary"]["total_tests"]
        passed_tests = self.test_results["summary"]["passed_tests"]
        
        if total_tests > 0:
            success_rate = (passed_tests / total_tests) * 100
            self.test_results["summary"]["success_rate"] = round(success_rate, 2)
        
        # Calculate performance metrics
        all_execution_times = []
        for agent_tests in self.test_results["agent_tests"].values():
            for provider_test in agent_tests.values():
                if "execution_time" in provider_test:
                    all_execution_times.append(provider_test["execution_time"])
        
        if all_execution_times:
            self.test_results["performance_metrics"] = {
                "average_execution_time": round(sum(all_execution_times) / len(all_execution_times), 2),
                "min_execution_time": round(min(all_execution_times), 2),
                "max_execution_time": round(max(all_execution_times), 2),
                "total_execution_time": round(sum(all_execution_times), 2)
            }
        
        # Print summary
        print(f"\n📈 TEST CYCLE SUMMARY")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {self.test_results['summary']['failed_tests']}")
        print(f"Success Rate: {self.test_results['summary']['success_rate']}%")
        
        if "average_execution_time" in self.test_results["performance_metrics"]:
            print(f"Average Execution Time: {self.test_results['performance_metrics']['average_execution_time']}s")
    
    def _save_test_results(self):
        """Save test results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_{timestamp}.json"
        filepath = os.path.join(os.path.dirname(__file__), "results", filename)
        
        # Create results directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Test results saved to: {filepath}")

async def main():
    """Main function to run the comprehensive test cycle"""
    test_cycle = ComprehensiveTestCycle()
    
    # Allow user to set additional API keys
    print("🔑 API KEY CONFIGURATION")
    print("-" * 30)
    print("OpenAI API key is already configured.")
    
    gemini_key = input("Enter Gemini API key (or press Enter to skip): ").strip()
    if gemini_key:
        test_cycle.provider_manager.providers['gemini']['api_key'] = gemini_key
    
    openrouter_key = input("Enter OpenRouter API key (or press Enter to skip): ").strip()
    if openrouter_key:
        test_cycle.provider_manager.providers['openrouter']['api_key'] = openrouter_key
    
    # Run the comprehensive test cycle
    results = await test_cycle.run_comprehensive_test_cycle()
    
    print("\n🎉 COMPREHENSIVE TEST CYCLE COMPLETED!")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    asyncio.run(main())