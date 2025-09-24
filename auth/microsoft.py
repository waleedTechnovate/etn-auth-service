import os
from fastapi import HTTPException
from msal import ConfidentialClientApplication
import requests
from models.auth import TokenRequest, MicrosoftAuthResponse

class MicrosoftAuth:
    def __init__(self):
        self.client_id = os.getenv("MS_CLIENT_ID")
        self.client_secret = os.getenv("MS_CLIENT_SECRET")
        self.tenant_id = os.getenv("MS_TENANT_ID")
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.graph_endpoint = "https://graph.microsoft.com/v1.0/me"

    async def authenticate(self, token_request: TokenRequest) -> MicrosoftAuthResponse:
        try:
            # Create MSAL application instance
            app_msal = ConfidentialClientApplication(
                self.client_id,
                authority=self.authority,
                client_credential=self.client_secret
            )

            # Acquire token on behalf of the user
            result = app_msal.acquire_token_on_behalf_of(
                user_assertion=token_request.token,
                scopes=["User.Read", "Mail.Read", "Calendars.Read"]
            )

            if "access_token" not in result:
                raise HTTPException(status_code=401, detail="Token validation failed")

            # Get user info from Microsoft Graph
            headers = {"Authorization": f"Bearer {result['access_token']}"}
            graph_response = requests.get(self.graph_endpoint, headers=headers)
            
            if graph_response.status_code != 200:
                raise HTTPException(status_code=401, detail="Failed to fetch user info")

            user_data = graph_response.json()

            return MicrosoftAuthResponse(
                user_id=user_data.get("id"),
                email=user_data.get("mail") or user_data.get("userPrincipalName"),
                name=user_data.get("displayName"),
                picture=None  # Microsoft Graph requires separate call for profile picture
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")

# Create global instance
microsoft_auth = MicrosoftAuth()