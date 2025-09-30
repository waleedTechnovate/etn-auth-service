from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import jwt
from jwt import PyJWKClient
import requests
from pydantic import BaseModel, EmailStr

# Load env
load_dotenv()

# Clerk endpoints (replace with your instance if needed)
CLERK_JWKS_URL = "https://concrete-shad-27.clerk.accounts.dev/.well-known/jwks.json"
jwks_client = PyJWKClient(CLERK_JWKS_URL)

# Clerk Management API
CLERK_API_BASE = os.getenv("CLERK_API_BASE", "https://api.clerk.com/v1")
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")

app = FastAPI()

# CORS (configurable via env CORS_ORIGINS, comma-separated)
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to verify Clerk JWT
async def get_current_user(authorization: str = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing auth token")

    token = authorization.split(" ")[1]
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False}  # disable audience check unless you set it
        )
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/protected")
async def protected_route(user=Depends(get_current_user)):
    return {
        "message": "This is protected",
        "user": user
    }

@app.get("/me")
async def me(user=Depends(get_current_user)):
    return user


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None


@app.post("/signup")
async def signup(payload: SignupRequest):
    if not CLERK_SECRET_KEY:
        raise HTTPException(status_code=500, detail="CLERK_SECRET_KEY is not configured")

    url = f"{CLERK_API_BASE}/users"
    headers = {
        "Authorization": f"Bearer {CLERK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "email_address": [payload.email],
        "password": payload.password,
    }
    if payload.first_name:
        body["first_name"] = payload.first_name
    if payload.last_name:
        body["last_name"] = payload.last_name

    try:
        resp = requests.post(url, json=body, headers=headers, timeout=10)
        if resp.status_code >= 400:
            # Bubble Clerk error up to client with minimal proxying
            try:
                detail = resp.json()
            except Exception:
                detail = {"message": resp.text}
            raise HTTPException(status_code=resp.status_code, detail=detail)
        return resp.json()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(exc)}")
