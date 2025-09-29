import requests
import json

BASE_URL = "http://localhost:8000"

def test_all_endpoints():
    print("Testing ETN Authentication API...")
    print("=" * 50)
    
    # Test 1: Basic endpoints
    print("1. Testing basic endpoints:")
    response = requests.get(f"{BASE_URL}/")
    print(f"   Root: {response.status_code} - {response.json()}")
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Health: {response.status_code} - {response.json()}")
    
    # Test 2: Microsoft Auth (will fail without real credentials)
    print("\n2. Testing Microsoft Auth:")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/microsoft",
            json={"token": "mock_ms_token_123456"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Success: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    # Test 3: Google Auth (will fail without real credentials)
    print("\n3. Testing Google Auth:")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/google",
            json={"token": "mock_google_token_123456"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Success: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    # Test 4: LinkedIn Auth URL
    print("\n4. Testing LinkedIn Auth URL:")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/linkedin/url")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Success: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")

if __name__ == "__main__":
    test_all_endpoints()