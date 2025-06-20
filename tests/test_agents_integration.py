"""
Comprehensive Integration Tests for Monk-AI Hackathon Demo
Tests all 7 agents with real functionality and API integration
"""

import asyncio
import json
import time
import sys
import os
from typing import Dict, List, Any
from datetime import datetime

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings
from app.core.ai_service import ai_service
from app.agents.code_optimizer import CodeOptimizer
from app.agents.doc_generator import DocGenerator
from app.agents.ideation import Ideation
from app.agents.orchestrator import Orchestrator
from app.agents.pr_reviewer import PRReviewer
from app.agents.security_analyzer import SecurityAnalyzer
from app.agents.test_generator import TestGenerator

class HackathonTestSuite:
    """
    Comprehensive test suite for Monk-AI hackathon demonstration
    """
    
    def __init__(self):
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "environment": "hackathon_demo",
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "agent_results": {},
            "performance_metrics": {},
            "api_health": {}
        }
        
        # Sample code for testing
        self.sample_python_code = '''
def fibonacci(n):
    if n <= 1:
        return n
    result = []
    a, b = 0, 1
    for i in range(n):
        result.append(a)
        a, b = b, a + b
    return result

def process_data(data):
    processed = []
    for item in data:
        if item > 0:
            processed.append(item * 2)
    return processed

class DataProcessor:
    def __init__(self):
        self.data = []
    
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
        const response = await fetch(`/api/users/${userId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching user data:', error);
        return null;
    }
}

class ShoppingCart {
    constructor() {
        this.items = [];
    }
    
    addItem(item) {
        this.items.push(item);
    }
    
    removeItem(itemId) {
        this.items = this.items.filter(item => item.id !== itemId);
    }
}
'''

    async def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run all agent tests and return comprehensive results"""
        print("🚀 Starting Monk-AI Hackathon Test Suite...")
        print("=" * 60)
        
        # Test AI Service Health
        await self._test_ai_service_health()
        
        # Test each agent
        agents_to_test = [
            ("CodeOptimizer", self._test_code_optimizer),
            ("DocGenerator", self._test_doc_generator),
            ("Ideation", self._test_ideation),
            ("Orchestrator", self._test_orchestrator),
            ("PRReviewer", self._test_pr_reviewer),
            ("SecurityAnalyzer", self._test_security_analyzer),
            ("TestGenerator", self._test_test_generator)
        ]
        
        for agent_name, test_func in agents_to_test:
            print(f"\n🔍 Testing {agent_name}...")
            try:
                start_time = time.time()
                result = await test_func()
                end_time = time.time()
                
                self.test_results["agent_results"][agent_name] = {
                    "status": "PASSED" if result["success"] else "FAILED",
                    "execution_time": round(end_time - start_time, 2),
                    "details": result,
                    "timestamp": datetime.now().isoformat()
                }
                
                if result["success"]:
                    self.test_results["passed_tests"] += 1
                    print(f"✅ {agent_name}: PASSED ({round(end_time - start_time, 2)}s)")
                else:
                    self.test_results["failed_tests"] += 1
                    print(f"❌ {agent_name}: FAILED - {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                self.test_results["failed_tests"] += 1
                self.test_results["agent_results"][agent_name] = {
                    "status": "ERROR",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                print(f"💥 {agent_name}: ERROR - {str(e)}")
            
            self.test_results["total_tests"] += 1
        
        # Generate final report
        await self._generate_final_report()
        return self.test_results

    async def _test_ai_service_health(self):
        """Test AI service health and provider availability"""
        print("🏥 Testing AI Service Health...")
        try:
            health_status = await ai_service.health_check()
            self.test_results["api_health"] = health_status
            
            available_providers = len([p for p, status in health_status.items() 
                                     if status.get("status") == "healthy"])
            print(f"✅ AI Service: {available_providers} providers available")
            
        except Exception as e:
            print(f"❌ AI Service Health Check Failed: {str(e)}")
            self.test_results["api_health"] = {"error": str(e)}

    async def _test_code_optimizer(self) -> Dict[str, Any]:
        """Test CodeOptimizer agent"""
        try:
            optimizer = CodeOptimizer()
            
            # Test Python code optimization
            result = await optimizer.optimize_code(
                code=self.sample_python_code,
                language="python",
                focus_areas=["performance", "memory_usage", "code_quality"]
            )
            
            # Validate result structure
            required_keys = ["status", "optimization_score", "performance_projections", "optimizations"]
            missing_keys = [key for key in required_keys if key not in result]
            
            if missing_keys:
                return {"success": False, "error": f"Missing keys: {missing_keys}"}
            
            # Check if optimizations were found
            optimizations_found = any(len(result["optimizations"].get(category, [])) > 0 
                                    for category in ["performance_optimizations", "memory_optimizations"])
            
            return {
                "success": True,
                "optimizations_found": optimizations_found,
                "optimization_score": result["optimization_score"]["overall_score"],
                "estimated_speedup": result["performance_projections"]["estimated_speedup"],
                "analysis_time": result.get("analysis_time_ms", 0)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _test_doc_generator(self) -> Dict[str, Any]:
        """Test DocGenerator agent"""
        try:
            doc_gen = DocGenerator()
            
            result = await doc_gen.generate_documentation(
                code=self.sample_python_code,
                language="python",
                doc_type="comprehensive"
            )
            
            # Validate result
            if result.get("status") != "success":
                return {"success": False, "error": "Documentation generation failed"}
            
            documentation = result.get("documentation", {})
            sections_generated = len([section for section in documentation.values() if section])
            
            return {
                "success": True,
                "sections_generated": sections_generated,
                "has_api_docs": bool(documentation.get("api_documentation")),
                "has_examples": bool(documentation.get("usage_examples")),
                "generation_time": result.get("generation_time_ms", 0)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _test_ideation(self) -> Dict[str, Any]:
        """Test Ideation agent"""
        try:
            ideation = Ideation()
            
            result = await ideation.generate_ideas(
                prompt="Create a modern web application for task management",
                category="web_development",
                creativity_level=0.8
            )
            
            if result.get("status") != "success":
                return {"success": False, "error": "Idea generation failed"}
            
            ideas = result.get("ideas", [])
            features = result.get("features", [])
            
            return {
                "success": True,
                "ideas_generated": len(ideas),
                "features_suggested": len(features),
                "has_implementation_plan": bool(result.get("implementation_plan")),
                "creativity_score": result.get("creativity_score", 0)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _test_orchestrator(self) -> Dict[str, Any]:
        """Test Orchestrator agent"""
        try:
            orchestrator = Orchestrator()
            
            # Test multi-agent coordination
            task = {
                "type": "code_review_and_optimize",
                "code": self.sample_javascript_code,
                "language": "javascript",
                "agents_required": ["code_optimizer", "security_analyzer", "test_generator"]
            }
            
            result = await orchestrator.coordinate_agents(task)
            
            if result.get("status") != "success":
                return {"success": False, "error": "Agent coordination failed"}
            
            agent_results = result.get("agent_results", {})
            completed_agents = len([r for r in agent_results.values() if r.get("status") == "completed"])
            
            return {
                "success": True,
                "agents_coordinated": len(agent_results),
                "successful_completions": completed_agents,
                "total_execution_time": result.get("total_execution_time", 0),
                "coordination_efficiency": result.get("coordination_efficiency", 0)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _test_pr_reviewer(self) -> Dict[str, Any]:
        """Test PRReviewer agent"""
        try:
            pr_reviewer = PRReviewer()
            
            # Mock PR data
            pr_data = {
                "title": "Add new user authentication system",
                "description": "Implements JWT-based authentication with role-based access control",
                "files_changed": [
                    {"filename": "auth.py", "additions": 150, "deletions": 20, "patch": self.sample_python_code},
                    {"filename": "utils.js", "additions": 80, "deletions": 10, "patch": self.sample_javascript_code}
                ],
                "author": "developer",
                "target_branch": "main"
            }
            
            result = await pr_reviewer.review_pull_request(pr_data)
            
            if result.get("status") != "success":
                return {"success": False, "error": "PR review failed"}
            
            review = result.get("review", {})
            
            return {
                "success": True,
                "overall_score": review.get("overall_score", 0),
                "issues_found": len(review.get("issues", [])),
                "suggestions_made": len(review.get("suggestions", [])),
                "security_concerns": len(review.get("security_concerns", [])),
                "approval_recommended": review.get("approval_recommended", False)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _test_security_analyzer(self) -> Dict[str, Any]:
        """Test SecurityAnalyzer agent"""
        try:
            security_analyzer = SecurityAnalyzer()
            
            # Test with potentially vulnerable code
            vulnerable_code = '''
import os
import subprocess

def execute_command(user_input):
    # Potential command injection vulnerability
    command = f"ls {user_input}"
    result = subprocess.run(command, shell=True, capture_output=True)
    return result.stdout

def get_user_data(user_id):
    # Potential SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query

def process_file(filename):
    # Potential path traversal vulnerability
    with open(f"/uploads/{filename}", "r") as f:
        return f.read()
'''
            
            result = await security_analyzer.analyze_security(
                code=vulnerable_code,
                language="python",
                scan_type="comprehensive"
            )
            
            if result.get("status") != "success":
                return {"success": False, "error": "Security analysis failed"}
            
            vulnerabilities = result.get("vulnerabilities", [])
            security_score = result.get("security_score", 0)
            
            return {
                "success": True,
                "vulnerabilities_found": len(vulnerabilities),
                "security_score": security_score,
                "critical_issues": len([v for v in vulnerabilities if v.get("severity") == "critical"]),
                "owasp_categories_covered": len(set(v.get("owasp_category") for v in vulnerabilities)),
                "scan_time": result.get("scan_time_ms", 0)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _test_test_generator(self) -> Dict[str, Any]:
        """Test TestGenerator agent"""
        try:
            test_generator = TestGenerator()
            
            result = await test_generator.generate_tests(
                code=self.sample_python_code,
                language="python",
                test_types=["unit", "integration", "edge_cases"]
            )
            
            if result.get("status") != "success":
                return {"success": False, "error": "Test generation failed"}
            
            tests = result.get("tests", {})
            
            return {
                "success": True,
                "unit_tests_generated": len(tests.get("unit_tests", [])),
                "integration_tests_generated": len(tests.get("integration_tests", [])),
                "edge_case_tests_generated": len(tests.get("edge_case_tests", [])),
                "test_coverage_estimate": result.get("coverage_estimate", 0),
                "generation_time": result.get("generation_time_ms", 0)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _generate_final_report(self):
        """Generate comprehensive final report"""
        print("\n" + "=" * 60)
        print("🎯 MONK-AI HACKATHON TEST RESULTS")
        print("=" * 60)
        
        total_tests = self.test_results["total_tests"]
        passed_tests = self.test_results["passed_tests"]
        failed_tests = self.test_results["failed_tests"]
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 Overall Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {failed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        print(f"\n🏥 AI Service Health:")
        for provider, status in self.test_results["api_health"].items():
            status_icon = "✅" if status.get("status") == "healthy" else "❌"
            print(f"   {status_icon} {provider}: {status.get('status', 'unknown')}")
        
        print(f"\n🤖 Agent Performance:")
        for agent_name, result in self.test_results["agent_results"].items():
            status_icon = "✅" if result["status"] == "PASSED" else "❌"
            exec_time = result.get("execution_time", 0)
            print(f"   {status_icon} {agent_name}: {result['status']} ({exec_time}s)")
        
        # Save detailed results to file
        with open("hackathon_test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: hackathon_test_results.json")
        
        if success_rate >= 80:
            print(f"\n🎉 EXCELLENT! Your Monk-AI system is ready for the hackathon demo!")
        elif success_rate >= 60:
            print(f"\n👍 GOOD! Minor issues to address before the demo.")
        else:
            print(f"\n⚠️  NEEDS WORK! Several issues need to be resolved.")

async def main():
    """Main test execution function"""
    test_suite = HackathonTestSuite()
    results = await test_suite.run_comprehensive_tests()
    return results

if __name__ == "__main__":
    # Run the test suite
    results = asyncio.run(main())
    print(f"\n🏁 Test suite completed. Check hackathon_test_results.json for detailed results.") 