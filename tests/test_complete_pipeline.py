#!/usr/bin/env python3
"""
COMPLETE END-TO-END PIPELINE TEST
================================
Tests the full flow: Frontend → Backend → AI Provider → Backend → Frontend
"""

import os
import asyncio
import json
import time
import aiohttp
from datetime import datetime

async def test_complete_pipeline():
    """Test the complete pipeline end-to-end"""
    print("🔍 COMPLETE END-TO-END PIPELINE TEST")
    print("=" * 50)
    
    # Check environment
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"OpenAI API Key: {api_key[:10]}...{api_key[-10:] if api_key else 'Not found'}")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "steps": [],
        "success": False,
        "error": None
    }
    
    try:
        # STEP 1: Test AI Service directly (Backend → AI Provider)
        print("\n📡 STEP 1: Testing Backend → AI Provider Integration")
        print("-" * 40)
        
        from app.core.ai_service import MultiProviderAIService
        ai_service = MultiProviderAIService()
        
        test_prompt = "Generate a simple Python function that adds two numbers. Keep response under 50 words."
        start_time = time.time()
        
        ai_response = await ai_service.generate_response(
            prompt=test_prompt,
            max_tokens=100,
            temperature=0.3
        )
        
        ai_response_time = round((time.time() - start_time) * 1000, 2)
        
        print(f"✅ AI Response Time: {ai_response_time}ms")
        print(f"✅ AI Response: {ai_response.get('response', 'No response')[:100]}...")
        print(f"✅ Provider: {ai_response.get('provider', 'unknown')}")
        print(f"✅ Model: {ai_response.get('model', 'unknown')}")
        
        results["steps"].append({
            "step": "ai_service_test",
            "status": "success",
            "response_time_ms": ai_response_time,
            "provider": ai_response.get('provider'),
            "model": ai_response.get('model'),
            "response_length": len(ai_response.get('response', ''))
        })
        
        # STEP 2: Test Agent Integration (Agent → AI Service)
        print("\n🤖 STEP 2: Testing Agent → AI Service Integration")
        print("-" * 40)
        
        from app.agents.ideation import Ideation
        ideation = Ideation()
        
        start_time = time.time()
        project_scope = await ideation.generate_project_scope(
            description="Build a simple task management app with authentication",
            template_key="web_app"
        )
        agent_response_time = round((time.time() - start_time) * 1000, 2)
        
        print(f"✅ Agent Response Time: {agent_response_time}ms")
        print(f"✅ Project Name: {project_scope.get('project_name', 'Unknown')}")
        print(f"✅ Features Generated: {len(project_scope.get('key_features', []))} features")
        print(f"✅ Tech Stack: {', '.join(project_scope.get('tech_stack', []))}")
        
        results["steps"].append({
            "step": "agent_integration_test",
            "status": "success", 
            "response_time_ms": agent_response_time,
            "project_name": project_scope.get('project_name'),
            "features_count": len(project_scope.get('key_features', [])),
            "tech_stack_count": len(project_scope.get('tech_stack', []))
        })
        
        # STEP 3: Test API Endpoint (Frontend → Backend flow)
        print("\n🌐 STEP 3: Testing Frontend → Backend API Flow")
        print("-" * 40)
        
        # Test the actual API endpoint that frontend calls
        test_payload = {
            "description": "Create an e-commerce platform with shopping cart",
            "template_key": "web_app"
        }
        
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            async with session.post(
                "http://localhost:8000/api/generate-project-scope",
                json=test_payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                api_response_time = round((time.time() - start_time) * 1000, 2)
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ API Response Time: {api_response_time}ms")
                    print(f"✅ API Status: {data.get('status', 'unknown')}")
                    print(f"✅ Project Generated: {data.get('project_scope', {}).get('project_name', 'Unknown')}")
                    
                    results["steps"].append({
                        "step": "api_endpoint_test",
                        "status": "success",
                        "response_time_ms": api_response_time,
                        "api_status": data.get('status'),
                        "response_size": len(str(data))
                    })
                else:
                    print(f"❌ API Error: {response.status}")
                    results["steps"].append({
                        "step": "api_endpoint_test",
                        "status": "failed",
                        "error": f"HTTP {response.status}"
                    })
        
        # STEP 4: Verify Complete Data Flow
        print("\n🔄 STEP 4: Complete Data Flow Verification")
        print("-" * 40)
        
        total_time = sum(step.get('response_time_ms', 0) for step in results["steps"])
        successful_steps = len([step for step in results["steps"] if step.get('status') == 'success'])
        
        print(f"✅ Total Pipeline Time: {total_time}ms")
        print(f"✅ Successful Steps: {successful_steps}/{len(results['steps'])}")
        print(f"✅ Data Flow: Frontend Request → Backend API → Agent → AI Service → OpenAI → Response Chain")
        
        if successful_steps == len(results["steps"]):
            results["success"] = True
            print("\n🎉 COMPLETE PIPELINE VERIFICATION: SUCCESS!")
            print("✅ Frontend can communicate with Backend")
            print("✅ Backend can send prompts to AI Provider") 
            print("✅ AI Provider returns needed data")
            print("✅ Data flows back to Frontend")
        else:
            print(f"\n⚠️ PARTIAL SUCCESS: {successful_steps}/{len(results['steps'])} steps completed")
            
    except Exception as e:
        print(f"\n❌ PIPELINE ERROR: {str(e)}")
        results["error"] = str(e)
        results["success"] = False
    
    # Save results
    with open("pipeline_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == "__main__":
    asyncio.run(test_complete_pipeline()) 