#!/usr/bin/env python3
"""
Direct API Test - Tests the running server endpoints directly
Run this while the server is running on port 8000
"""

import asyncio
import json
import aiohttp
import sys
from datetime import datetime

async def test_api_endpoints():
    """Test the actual API endpoints that are running"""
    base_url = "http://127.0.0.1:8000"
    
    print("🌐 Testing Multi-Agent API Endpoints")
    print("=" * 50)
    print(f"🎯 Target: {base_url}")
    print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test cases
    test_cases = [
        {
            "name": "Agent Status Check",
            "method": "GET",
            "endpoint": "/api/agents/status",
            "expected_status": 200,
            "data": None
        },
        {
            "name": "Agent Health Check", 
            "method": "GET",
            "endpoint": "/api/agents/health",
            "expected_status": 200,
            "data": None
        },
        {
            "name": "Available Workflows",
            "method": "GET", 
            "endpoint": "/api/workflow/available-workflows",
            "expected_status": 200,
            "data": None
        },
        {
            "name": "Ideation Agent - Simple Test",
            "method": "POST",
            "endpoint": "/api/agents/ideate",
            "expected_status": 200,
            "data": {
                "description": "Build a simple todo app with user authentication",
                "template_key": "web_app"
            }
        },
        {
            "name": "Ideation Agent - E-commerce Test",
            "method": "POST", 
            "endpoint": "/api/agents/ideate",
            "expected_status": 200,
            "data": {
                "description": "Create an e-commerce platform with shopping cart and payment processing",
                "template_key": "web_app"
            }
        }
    ]
    
    results = []
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
        for i, test in enumerate(test_cases, 1):
            print(f"📋 Test {i}/{len(test_cases)}: {test['name']}")
            
            try:
                url = f"{base_url}{test['endpoint']}"
                
                if test['method'] == 'GET':
                    async with session.get(url) as response:
                        status = response.status
                        try:
                            data = await response.json()
                        except:
                            data = await response.text()
                
                elif test['method'] == 'POST':
                    async with session.post(url, json=test['data']) as response:
                        status = response.status
                        try:
                            data = await response.json()
                        except:
                            data = await response.text()
                
                # Check result
                success = status == test['expected_status']
                status_emoji = "✅" if success else "❌"
                
                print(f"  {status_emoji} Status: {status} (expected {test['expected_status']})")
                
                if success and isinstance(data, dict):
                    # Show some meaningful data
                    if test['endpoint'] == '/api/agents/status':
                        agents = data.get('agents', {})
                        print(f"    📊 Active agents: {len(agents)}")
                        
                    elif test['endpoint'] == '/api/agents/ideate':
                        if 'project_scope' in data:
                            scope = data['project_scope']
                            features = scope.get('key_features', [])
                            print(f"    💡 Generated project with {len(features)} features")
                            if features:
                                print(f"    🎯 First feature: {features[0][:60]}...")
                        
                        if 'user_stories' in data:
                            stories = data['user_stories']
                            print(f"    📖 Generated {len(stories)} user stories")
                    
                    elif test['endpoint'] == '/api/workflow/available-workflows':
                        workflows = data.get('workflows', [])
                        print(f"    🔄 Available workflows: {len(workflows)}")
                
                elif not success:
                    print(f"    💬 Response: {str(data)[:100]}...")
                
                results.append({
                    "test": test['name'],
                    "success": success,
                    "status": status,
                    "endpoint": test['endpoint']
                })
                
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                results.append({
                    "test": test['name'], 
                    "success": False,
                    "error": str(e),
                    "endpoint": test['endpoint']
                })
            
            print()
    
    # Summary
    print("=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for r in results if r['success'])
    total = len(results)
    
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{status} {result['test']}")
        if not result['success'] and 'error' in result:
            print(f"    Error: {result['error']}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your multi-agent system is working correctly!")
        print("💡 The backend API is fully functional with OpenAI integration.")
    elif passed > 0:
        print("⚠️  SOME TESTS PASSED! Parts of your system are working.")
        print("💡 Check the failed tests above for issues to resolve.")
    else:
        print("❌ ALL TESTS FAILED! Please check:")
        print("  1. Is the server running? (python -m uvicorn app.main:app --reload --port 8000)")
        print("  2. Is your OpenAI API key set correctly?")
        print("  3. Are all dependencies installed? (pip install -r requirements.txt)")
    
    return results

async def main():
    """Main function"""
    try:
        results = await test_api_endpoints()
        
        # Save results
        with open("api_test_results.json", "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "results": results
            }, f, indent=2)
        
        print(f"\n📝 Detailed results saved to: api_test_results.json")
        
    except Exception as e:
        print(f"❌ Test runner error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())