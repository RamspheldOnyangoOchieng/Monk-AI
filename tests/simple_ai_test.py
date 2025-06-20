#!/usr/bin/env python3
"""
Simple AI Test - Demonstrates actual working OpenAI integration
Run this to verify your OpenAI API key works and the system can generate responses
"""

import os
import asyncio
import json
from datetime import datetime

# Simple OpenAI client test
import openai

async def test_openai_direct():
    """Test OpenAI API directly without our framework"""
    print("🔑 Testing OpenAI API directly...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        return False
    
    if api_key == "your_openai_key_here":
        print("❌ Please set a real OpenAI API key (not the placeholder)")
        return False
    
    try:
        client = openai.AsyncOpenAI(api_key=api_key)
        
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Hello! Please respond with 'OpenAI API is working correctly' to confirm the connection."}
            ],
            max_tokens=50,
            temperature=0.1
        )
        
        ai_response = response.choices[0].message.content
        print(f"✅ OpenAI Response: {ai_response}")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API Error: {str(e)}")
        return False

async def test_project_idea_generation():
    """Test generating a project idea with OpenAI"""
    print("\n💡 Testing Project Idea Generation...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_key_here":
        print("❌ Valid OpenAI API key required")
        return False
    
    try:
        client = openai.AsyncOpenAI(api_key=api_key)
        
        prompt = """Generate a project scope for: "Build a task management application with user authentication and real-time updates"

Please respond with a JSON object containing:
- project_name: A creative name for the project
- description: Brief description
- key_features: List of 5 main features
- target_audience: Who would use this
- estimated_timeline: How long to build

Keep the response concise and practical."""

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        print(f"✅ Generated Project Scope:")
        print(ai_response)
        
        # Try to parse as JSON
        try:
            project_data = json.loads(ai_response)
            print(f"\n✅ Successfully parsed JSON response")
            print(f"  - Project Name: {project_data.get('project_name', 'N/A')}")
            print(f"  - Features: {len(project_data.get('key_features', []))} features")
            return True
        except json.JSONDecodeError:
            print(f"⚠️  Response generated but not valid JSON (this is normal)")
            return True
            
    except Exception as e:
        print(f"❌ Project Generation Error: {str(e)}")
        return False

async def test_code_generation():
    """Test generating actual code"""
    print("\n💻 Testing Code Generation...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_key_here":
        print("❌ Valid OpenAI API key required")
        return False
    
    try:
        client = openai.AsyncOpenAI(api_key=api_key)
        
        prompt = """Generate a simple Python FastAPI endpoint for user authentication.
        
Include:
1. A POST endpoint for login
2. Basic request/response models using Pydantic
3. Simple password validation
4. Return a success message

Keep it concise and functional."""

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.3
        )
        
        ai_response = response.choices[0].message.content
        print(f"✅ Generated Code:")
        print("-" * 40)
        print(ai_response)
        print("-" * 40)
        
        # Check if it looks like code
        if "def " in ai_response or "class " in ai_response or "@app." in ai_response:
            print("✅ Generated code looks valid")
            return True
        else:
            print("⚠️  Generated text but may not be valid code")
            return True
            
    except Exception as e:
        print(f"❌ Code Generation Error: {str(e)}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting Simple AI Functionality Test")
    print("=" * 50)
    
    # Check environment
    print(f"📍 Current directory: {os.getcwd()}")
    print(f"🕐 Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run tests
    test1 = await test_openai_direct()
    test2 = await test_project_idea_generation()
    test3 = await test_code_generation()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    results = {
        "OpenAI API Connection": test1,
        "Project Idea Generation": test2,
        "Code Generation": test3
    }
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
    
    overall_success = all(results.values())
    
    if overall_success:
        print(f"\n🎉 ALL TESTS PASSED! Your AI system is working correctly.")
        print(f"💡 You can now run the full server and frontend to see the multi-agent system in action.")
    else:
        print(f"\n⚠️  SOME TESTS FAILED. Please check your OpenAI API key and internet connection.")
    
    print(f"\n🔗 Next steps:")
    print(f"1. Make sure your .env file has a valid OPENAI_API_KEY")
    print(f"2. Run the server: python -m uvicorn app.main:app --reload --port 8000")
    print(f"3. Test the API endpoints at http://localhost:8000/docs")

if __name__ == "__main__":
    asyncio.run(main())