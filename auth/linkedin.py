import os
import requests
from fastapi import HTTPException
from models.auth import LinkedInAuthResponse

class LinkedInAuth:
    def __init__(self):
        self.client_id = os.getenv("LINKEDIN_CLIENT_ID")
        self.client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
        self.redirect_uri = "http://localhost:8000/auth/linkedin/callback"

    async def handle_callback(self, code: str) -> LinkedInAuthResponse:
        try:
            # Exchange authorization code for access token
            token_url = "https://www.linkedin.com/oauth/v2/accessToken"
            token_data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }

            token_response = requests.post(token_url, data=token_data, timeout=30)
            
            if token_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get access token from LinkedIn")

            token_json = token_response.json()
            access_token = token_json.get("access_token")

            if not access_token:
                raise HTTPException(status_code=400, detail="No access token received")

            # Get user info using OpenID Connect
            userinfo_url = "https://api.linkedin.com/v2/userinfo"
            headers = {"Authorization": f"Bearer {access_token}"}
            userinfo_response = requests.get(userinfo_url, headers=headers, timeout=30)
            
            if userinfo_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get user info from LinkedIn")

            userinfo = userinfo_response.json()

            return LinkedInAuthResponse(
                user_id=userinfo.get("sub"),
                email=userinfo.get("email"),
                name=userinfo.get("name"),
                given_name=userinfo.get("given_name"),
                family_name=userinfo.get("family_name"),
                picture=userinfo.get("picture"),
                locale=userinfo.get("locale")
            )

        except requests.exceptions.Timeout:
            raise HTTPException(status_code=408, detail="Request to LinkedIn timed out")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LinkedIn authentication failed: {str(e)}")

# Create global instance
linkedin_auth = LinkedInAuth()