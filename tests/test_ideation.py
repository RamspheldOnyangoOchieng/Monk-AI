import requests
import json

def test_ideation_endpoint():
    url = 'http://localhost:8000/api/agents/ideate'
    data = {
        'description': 'A simple todo list application',
        'template_key': 'web_app'
    }
    
    try:
        response = requests.post(url, json=data)
        print(f'Status Code: {response.status_code}')
        print(f'Response Headers: {dict(response.headers)}')
        
        if response.status_code == 200:
            result = response.json()
            print('\n=== IDEATION RESPONSE ===')
            print(json.dumps(result, indent=2))
            
            # Check if it contains AI-generated content or mock data
            project_scope = result.get('project_scope', {})
            if 'Generated Project for' in str(project_scope):
                print('\n✅ SUCCESS: Using AI-generated content!')
            else:
                print('\n⚠️  WARNING: Might be using mock data')
                
        else:
            print(f'Error: {response.text}')
            
    except Exception as e:
        print(f'Error testing endpoint: {e}')

if __name__ == '__main__':
    test_ideation_endpoint()