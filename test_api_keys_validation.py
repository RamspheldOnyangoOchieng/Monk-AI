#!/usr/bin/env python3
"""
Google Gemini API Key Validation Script
Test both API keys provided by the user to ensure they are valid
"""

import asyncio
import sys
import os
from google import genai
from google.genai import types

async def test_api_key(api_key: str, key_name: str):
    """Test a single API key"""
    print(f"\n🔑 Testing {key_name}: {api_key[:20]}...")
    
    try:
        # Initialize the client
        client = genai.Client(api_key=api_key)
        
        # Test with a simple generation request
        response = await client.models.generate_content_async(
            model="gemini-2.5-flash-preview",
            contents="Hello, please respond with 'API key is working'"
        )
        
        print(f"✅ {key_name}: VALID")
        print(f"   Response: {response.text[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ {key_name}: INVALID")
        print(f"   Error: {str(e)}")
        return False

async def main():
    """Main validation function"""
    print("🚀 GOOGLE GEMINI API KEY VALIDATION")
    print("=" * 50)
    
    # Test keys provided by user
    test_keys = [
        ("AIzaSyBmNAM-rtTY5TkRrv43x3C9nRe9ovY33GA", "User Key 1"),
        ("AIzaSyCl_92cZ5Q3S7zSWbcy-258HXPNzMFXauk", "User Key 2"),
        ("AIzaSyC9jhYOrQn0OU3wM4BR_Uzz60I2ZQQa1rI", "Current .env Key")
    ]
    
    valid_keys = []
    
    for api_key, key_name in test_keys:
        if await test_api_key(api_key, key_name):
            valid_keys.append((api_key, key_name))
    
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    if valid_keys:
        print(f"✅ Valid keys found: {len(valid_keys)}/{len(test_keys)}")
        print("\n🏆 RECOMMENDED KEY FOR USE:")
        best_key = valid_keys[0]  # Use first valid key
        print(f"   {best_key[1]}: {best_key[0][:20]}...")
        print(f"\n📝 UPDATE YOUR .env FILE:")
        print(f"   GOOGLE_API_KEY={best_key[0]}")
    else:
        print("❌ No valid keys found!")
        print("🔗 Get a valid key at: https://ai.google.dev/gemini-api/docs/api-key")
    
    print("\n🔍 TESTING google-genai LIBRARY:")
    try:
        import google.genai
        print(f"✅ google-genai library installed: version available")
        print(f"   Module path: {google.genai.__file__}")
    except ImportError as e:
        print(f"❌ google-genai library not found: {e}")
        print("📦 Install with: pip install google-genai")

if __name__ == "__main__":
    asyncio.run(main()) 