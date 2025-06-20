import requests
import json

def test_ideation_endpoint():
    url = "http://localhost:8000/api/agents/ideate"
    
    payload = {
        "description": "A simple web app for task management"
    }
    
    try:
        print("Testing ideation endpoint...")
        response = requests.post(url, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"Response keys: {list(data.keys())}")
            
            if 'user_stories' in data:
                print(f"User stories count: {len(data['user_stories'])}")
            
            # Check if it's mock data
            response_text = json.dumps(data)
            if "mock" in response_text.lower() or "example" in response_text.lower():
                print("⚠️ Response appears to contain mock data")
            else:
                print("✅ Response appears to be AI-generated")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - is the server running?")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_ideation_endpoint()