from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import jwt
from jwt import PyJWKClient

# Load env
load_dotenv()

# Clerk JWKS endpoint (replace with your instance if needed)
CLERK_JWKS_URL = "https://concrete-shad-27.clerk.accounts.dev/.well-known/jwks.json"
jwks_client = PyJWKClient(CLERK_JWKS_URL)

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
