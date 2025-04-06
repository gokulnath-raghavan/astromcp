import requests
import base64
import json

def test_api():
    # API credentials
    user_id = "639454"
    api_key = "0a2ba88ba63a2ca0cff8da7b6ed3a8616a8214ff"
    
    # Create Basic Auth header
    auth_string = f"{user_id}:{api_key}"
    auth_bytes = auth_string.encode('ascii')
    base64_auth = base64.b64encode(auth_bytes).decode('ascii')
    auth_header = f"Basic {base64_auth}"
    
    # Request headers
    headers = {
        "authorization": auth_header,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Request data
    data = {
        "day": 1,
        "month": 1,
        "year": 2000,
        "hour": 12,
        "min": 0,
        "lat": 0,
        "lon": 0,
        "tzone": 0
    }
    
    # Make the request
    url = "https://json.astrologyapi.com/v1/birth_details"
    print(f"\nMaking request to: {url}")
    print(f"Headers: {headers}")
    print(f"Data: {data}")
    
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(data),
        verify=False
    )
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Content: {response.text}")

if __name__ == "__main__":
    test_api() 