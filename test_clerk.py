import os
import requests
from dotenv import load_dotenv

# Load env vars
load_dotenv()
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")

# Replace with your active session ID
SESSION_ID = "sess_33O576GwfJ15DRNXZlu8WmdJwnI"

# Asking Clerk for a fresh session JWT
jwt_url = f"https://api.clerk.dev/v1/sessions/{SESSION_ID}/tokens"
headers = {
    "Authorization": f"Bearer {CLERK_SECRET_KEY}",
    "Content-Type": "application/json"
}

res = requests.post(jwt_url, headers=headers, json={"jwt": {}})
res.raise_for_status()
jwt_token = res.json()["jwt"]

print("Got new Clerk JWT")

# Using JWT to call your backend
backend_url = "http://localhost:8000/protected"
backend_headers = {
    "Authorization": f"Bearer {jwt_token}"
}

backend_res = requests.get(backend_url, headers=backend_headers)
backend_res.raise_for_status()

print("Backend response:")
print(backend_res.json())
