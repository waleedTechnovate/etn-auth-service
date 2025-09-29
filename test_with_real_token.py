import requests
import json

BASE_URL = "http://localhost:8000"

# Your real ID token from Google
REAL_ID_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjkyN2I4ZmI2N2JiYWQ3NzQ0NWU1ZmVhNGM3MWFhOTg0NmQ3ZGRkMDEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDA4NTc0ODY4NTk5NzUzNzU5MzYiLCJlbWFpbCI6IndhbGVlZHNoYW56YXlAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJFZGd0RGlGN3gxTXc5Zl9ZSUlsVnR3IiwiaWF0IjoxNzU4NzgzMzU5LCJleHAiOjE3NTg3ODY5NTl9.OeH4ruBmwdN2seq_l77Klj8nRtWDRQWlf5Ma9Esg8FWI7cFI8wtCCB5Cgh_dlLCRvH9kYzth8uggbq7sMfKfr3mvWHa6viWaVUtm15dYLOki1Kv0IIxddJrHgzw9Uk1u6EtkUY-2TNGVTNyhm_6AOHeVUjNbwxb7ELFAmDS4LlZnhuD5RNHZRdqr33oZGYxpy_jwfVwDYp3JYxcJphPXfeLT6BdY4hqNrn4flKI488ybsI6eiYXw5Zk2FTc2iHjxRm2y_ltwbHLgdSsEvYf8p5a7Hwpf2MiaK36JTjw-Fo_wTQhrTCnLQAQT49HMADdOmYivUM8Vh0OjleEYIcN3Tg"

def test_real_google_auth():
    print("Testing Google OAuth with REAL ID Token")
    print("=" * 50)
    
    response = requests.post(
        f"{BASE_URL}/api/auth/google",
        json={"token": REAL_ID_TOKEN}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("\n🎉 SUCCESS! Google OAuth is working perfectly!")
        user_data = response.json()
        print(f"✅ Authenticated as: {user_data.get('email')}")
        print(f"✅ User ID: {user_data.get('user_id')}")
        print(f"✅ Name: {user_data.get('name', 'Not provided')}")
    else:
        print("\n❌ Authentication failed")
        print(f"Error: {response.json()}")

if __name__ == "__main__":
    test_real_google_auth()