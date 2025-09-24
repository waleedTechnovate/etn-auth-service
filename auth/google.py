import os
from fastapi import HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from models.auth import TokenRequest, GoogleAuthResponse

class GoogleAuth:
    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")

    async def authenticate(self, token_request: TokenRequest) -> GoogleAuthResponse:
        try:
            # Verify the OAuth 2.0 ID token
            idinfo = id_token.verify_oauth2_token(
                token_request.token,
                google_requests.Request(),
                self.client_id
            )

            # Extract user information
            user_id = idinfo["sub"]
            email = idinfo["email"]
            name = idinfo.get("name")
            picture = idinfo.get("picture")

            return GoogleAuthResponse(
                user_id=user_id,
                email=email,
                name=name,
                picture=picture
            )

        except ValueError as e:
            raise HTTPException(status_code=400, detail="Invalid Google token")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Google authentication failed: {str(e)}")

# Create global instance
google_auth = GoogleAuth()