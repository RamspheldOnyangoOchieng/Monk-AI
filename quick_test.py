#!/usr/bin/env python3
"""
Quick Frontend-Backend Integration Test
Run this to verify everything is working for the demo
"""

import asyncio
import aiohttp
import json
from datetime import datetime

async def test_demo_endpoints():
    """Test all the endpoints the frontend needs"""
    base_url = "http://127.0.0.1:8000"
    
    print("🚀 QUICK DEMO TEST - Frontend-Backend Integration")
    print("=" * 55)
    
    endpoints_to_test = [
        ("GET", "/api/demo/scenarios", None),
        ("GET", "/api/demo/live-metrics", None),
        ("GET", "/api/agents/status", None),
        ("GET", "/api/workflow/available-workflows", None),
        ("POST", "/api/generate-project-scope", {
            "description": "Build a task management app with real-time collaboration",
            "template_key": "web_app"
        }),
        ("POST", "/api/agents/ideate", {
            "description": "Create an e-commerce platform with shopping cart",
            "template_key": "web_app"
        })
    ]
    
    results = []
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
        for method, endpoint, data in endpoints_to_test:
            try:
                url = f"{base_url}{endpoint}"
                print(f"Testing {method} {endpoint}...")
                
                if method == "GET":
                    async with session.get(url) as response:
                        status = response.status
                        response_data = await response.json()
            else:
                    async with session.post(url, json=data) as response:
                        status = response.status
                        response_data = await response.json()
                
                success = status == 200
                status_icon = "✅" if success else "❌"
                print(f"  {status_icon} {status} - {len(str(response_data))} bytes")
                
                if success and endpoint == "/api/demo/scenarios":
                    scenarios = response_data.get("scenarios", [])
                    print(f"    📋 Found {len(scenarios)} demo scenarios")
                
                elif success and endpoint == "/api/demo/live-metrics":
                    metrics = response_data.get("metrics", {})
                    print(f"    📊 Active agents: {metrics.get('active_agents', 0)}")
                
                elif success and "ideate" in endpoint:
                    if "project_scope" in response_data:
                        print(f"    💡 Project scope generated successfully")
                
                results.append({"endpoint": endpoint, "success": success, "status": status})
                
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                results.append({"endpoint": endpoint, "success": False, "error": str(e)})
    
    # Summary
    print("\n" + "=" * 55)
    print("📊 DEMO READINESS SUMMARY")
    print("=" * 55)
    
    working = sum(1 for r in results if r.get("success", False))
    total = len(results)
    
    for result in results:
        status = "✅ READY" if result.get("success") else "❌ ISSUE"
        print(f"{status} {result['endpoint']}")
    
    print(f"\n🎯 Demo Status: {working}/{total} endpoints working ({working/total*100:.0f}%)")
    
    if working >= 5:  # Most critical endpoints working
        print("🎉 DEMO IS READY! Your frontend should work perfectly!")
        print("💡 Start frontend with: cd frontend; npm start")
        else:
        print("⚠️  Some endpoints need attention before demo")
    
    return results

if __name__ == "__main__":
    asyncio.run(test_demo_endpoints())