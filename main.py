from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import auth modules and models
from auth.microsoft import microsoft_auth
from auth.google import google_auth
from auth.linkedin import linkedin_auth
from models.auth import TokenRequest, MicrosoftAuthResponse, GoogleAuthResponse, LinkedInAuthResponse

# Initialize FastAPI app
app = FastAPI(
    title="ETN Platform Authentication API",
    description="Authentication endpoints for Microsoft Outlook, Google, and LinkedIn",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "ETN Platform Authentication API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "authentication-api"}

# Microsoft Outlook Authentication Endpoint
@app.post("/api/auth/microsoft", response_model=MicrosoftAuthResponse)
async def microsoft_auth_endpoint(token_request: TokenRequest):
    """
    Authenticate user using Microsoft Outlook OAuth
    """
    return await microsoft_auth.authenticate(token_request)

# Google Authentication Endpoint
@app.post("/api/auth/google", response_model=GoogleAuthResponse)
async def google_auth_endpoint(token_request: TokenRequest):
    """
    Authenticate user using Google OAuth
    """
    return await google_auth.authenticate(token_request)

# LinkedIn Authentication Endpoints
@app.get("/auth/linkedin/callback", response_model=LinkedInAuthResponse)
async def linkedin_callback(code: str = Query(..., description="Authorization code from LinkedIn")):
    """
    Handle LinkedIn OAuth callback
    """
    return await linkedin_auth.handle_callback(code)

@app.get("/api/auth/linkedin/url")
async def get_linkedin_auth_url():
    """
    Get LinkedIn authorization URL for frontend redirection
    """
    client_id = os.getenv("LINKEDIN_CLIENT_ID")
    redirect_uri = "http://localhost:8000/auth/linkedin/callback"
    scope = "openid profile email"
    
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
    )
    
    return {"auth_url": auth_url}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)