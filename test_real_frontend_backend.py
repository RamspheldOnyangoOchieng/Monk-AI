#!/usr/bin/env python3
"""
REAL FRONTEND-BACKEND COMMUNICATION TEST
=======================================
Tests the actual CORS preflight requests to verify the real frontend-backend communication.
This simulates what happens when React runs in a browser
"""

import asyncio
import aiohttp
import json

async def test_browser_like_communication():
    """Test the exact flow a browser uses: OPTIONS (preflight) + POST"""
    print("🌐 TESTING REAL BROWSER-LIKE FRONTEND-BACKEND COMMUNICATION")
    print("=" * 65)
    print("Simulating: Browser → CORS Preflight → Actual Request")
    print()
    
    backend_url = "http://localhost:8000"
    
    # Test the exact flow browsers use
    test_endpoints = [
        {
            "name": "Generate Project Scope",
            "url": f"{backend_url}/api/generate-project-scope",
            "payload": {
                "description": "Build a real-time messaging app with authentication",
                "template_key": "web_app"
            }
        },
        {
            "name": "Workflow Execute", 
            "url": f"{backend_url}/api/workflow/execute",
            "payload": {
                "project_description": "Create a task management system",
                "programming_language": "Python",
                "workflow_type": "full_development"
            }
        }
    ]
    
    async with aiohttp.ClientSession() as session:
        for test in test_endpoints:
            print(f"🔍 Testing: {test['name']}")
            print(f"   URL: {test['url']}")
            
            # STEP 1: Simulate CORS Preflight (OPTIONS request)
            print("   📡 Step 1: CORS Preflight (OPTIONS)...")
            try:
                preflight_headers = {
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type",
                }
                
                async with session.options(
                    test['url'],
                    headers=preflight_headers
                ) as preflight_response:
                    
                    print(f"   ✅ Preflight Status: {preflight_response.status}")
                    
                    if preflight_response.status == 200:
                        # Check CORS headers
                        cors_headers = {
                            "Access-Control-Allow-Origin": preflight_response.headers.get("Access-Control-Allow-Origin"),
                            "Access-Control-Allow-Methods": preflight_response.headers.get("Access-Control-Allow-Methods"),
                            "Access-Control-Allow-Headers": preflight_response.headers.get("Access-Control-Allow-Headers"),
                        }
                        print(f"   ✅ CORS Headers: {cors_headers}")
                        
                        # STEP 2: Actual POST request (if preflight passed)
                        print("   📡 Step 2: Actual POST Request...")
                        
                        post_headers = {
                            "Content-Type": "application/json",
                            "Origin": "http://localhost:3000",
                        }
                        
                        async with session.post(
                            test['url'],
                            json=test['payload'],
                            headers=post_headers
                        ) as post_response:
                            
                            print(f"   ✅ POST Status: {post_response.status}")
                            
                            if post_response.status == 200:
                                data = await post_response.json()
                                print(f"   ✅ Response Size: {len(str(data))} chars")
                                print(f"   ✅ Response Preview: {str(data)[:100]}...")
                                print("   🎉 COMPLETE BROWSER FLOW: SUCCESS!")
                            else:
                                error_text = await post_response.text()
                                print(f"   ❌ POST Failed: {error_text[:100]}...")
                                print("   ❌ BROWSER FLOW: FAILED")
                                
                    else:
                        print(f"   ❌ Preflight Failed: {preflight_response.status}")
                        print("   ❌ BROWSER FLOW: BLOCKED BY CORS")
                        
            except aiohttp.ClientConnectorError:
                print("   ❌ Cannot connect to backend server")
                print("   ❌ Make sure server is running: python -m uvicorn app.main:app --port 8000")
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
            
            print()
    
    # Test simple connectivity
    print("🔗 TESTING BASIC CONNECTIVITY")
    print("-" * 30)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{backend_url}/") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Backend Health: {response.status}")
                    print(f"✅ Backend Message: {data.get('message', 'No message')}")
                    print(f"✅ Backend Status: {data.get('status', 'Unknown')}")
                else:
                    print(f"❌ Backend Health: {response.status}")
    except:
        print("❌ Backend is not responding")

if __name__ == "__main__":
    asyncio.run(test_browser_like_communication()) 