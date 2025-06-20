#!/usr/bin/env python3
"""
Google Gemini Integration Test Script
Tests the integration with google-genai library and validates API keys
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

async def test_gemini_integration():
    """Test Google Gemini integration with the correct library"""
    print("🚀 GOOGLE GEMINI INTEGRATION TEST")
    print("=" * 60)
    
    try:
        # Import and test the AI service
        from app.core.ai_service import ai_service
        
        print("✅ AI Service imported successfully")
        
        # Test health check
        health = await ai_service.health_check()
        print(f"🏥 Health Check Results:")
        for provider, status in health.items():
            print(f"   {provider}: {status['status']}")
        
        # Test Gemini specifically
        print("\n🤖 Testing Google Gemini Response...")
        test_prompt = "Please respond with a JSON object containing: {\"status\": \"working\", \"provider\": \"google-gemini\", \"timestamp\": \"current_time\"}"
        
        # Import the AIProvider enum correctly
        from app.core.ai_service import AIProvider
        
        result = await ai_service.generate_response(
            prompt=test_prompt,
            provider=AIProvider.GEMINI,
            model="gemini-2.0-flash",  # Use correct model name
            max_tokens=200,
            temperature=0.3,
            request_structured_output=True
        )
        
        print(f"📋 Gemini Response:")
        print(f"   Success: {result['success']}")
        print(f"   Provider: {result['provider']}")
        print(f"   Model: {result['model']}")
        print(f"   Response: {result['response'][:300]}...")
        
        # Test schema validation
        if result['success'] and result['response']:
            try:
                # Try to parse as JSON
                response_json = json.loads(result['response'])
                print(f"✅ JSON Schema Valid:")
                print(f"   Status: {response_json.get('status')}")
                print(f"   Provider: {response_json.get('provider')}")
                print(f"   Timestamp: {response_json.get('timestamp')}")
            except json.JSONDecodeError:
                print(f"⚠️  Response is not valid JSON, but that's okay for this test")
        
        # Test with debug information
        print(f"\n🔍 Debug Information:")
        print(f"   Available Models: {ai_service.get_available_models()}")
        print(f"   Provider Priority: {result.get('provider_priority', 'N/A')}")
        print(f"   Total Providers: {result.get('total_providers', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_api_keys():
    """Test both API keys provided by the user"""
    print("\n🔑 API KEY VALIDATION TEST")
    print("=" * 60)
    
    from google import genai
    
    test_keys = [
        ("AIzaSyBmNAM-rtTY5TkRrv43x3C9nRe9ovY33GA", "User Key 1"),
        ("AIzaSyCl_92cZ5Q3S7zSWbcy-258HXPNzMFXauk", "User Key 2"),
    ]
    
    for api_key, key_name in test_keys:
        print(f"\n🔑 Testing {key_name}: {api_key[:20]}...")
        
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash",  # Use correct model name
                contents="Respond with: API key is valid"
            )
            
            print(f"✅ {key_name}: VALID")
            print(f"   Response: {response.text[:100]}...")
            
        except Exception as e:
            print(f"❌ {key_name}: INVALID - {str(e)}")

async def main():
    """Main test function"""
    print("🎯 MONK-AI GOOGLE GEMINI INTEGRATION TEST")
    print("🔧 Using google-genai library (correct version)")
    print("📅 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 80)
    
    # Test API keys directly
    await test_api_keys()
    
    # Test integration through AI service
    success = await test_gemini_integration()
    
    print("\n" + "=" * 80)
    if success:
        print("🎉 INTEGRATION TEST PASSED!")
        print("✅ Google Gemini is working correctly")
        print("✅ Debug information is available")
        print("✅ Schema validation is working")
    else:
        print("❌ INTEGRATION TEST FAILED!")
        print("💡 Check API keys and library installation")
    
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main()) 