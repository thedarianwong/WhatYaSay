from fastapi import APIRouter, Request, Depends, HTTPException, Response
from google_auth_oauthlib.flow import Flow
from starlette.responses import RedirectResponse
import os

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login")
async def login(request: Request):
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRET,
        scopes=['https://www.googleapis.com/auth/drive'],
        redirect_uri=GOOGLE_REDIRECT_URI
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        state='state_parameter_passthrough_value'
    )
    
    response = RedirectResponse(authorization_url)
    response.set_cookie('oauth2_state', state)
    return response

@router.get("/callback")
async def callback(request: Request, state: str = Depends()):
    # Check if the state matches
    state_cookie = request.cookies.get('oauth2_state')
    if not state_cookie or state_cookie != state:
        raise HTTPException(status_code=400, detail="State mismatch")

    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRET,
        scopes=['https://www.googleapis.com/auth/drive'],
        state=state,
        redirect_uri=GOOGLE_REDIRECT_URI
    )

    flow.fetch_token(authorization_response=request.url)

    # The token can now be used for Google Drive API calls.
    # You might want to store it in a secure place for future use.
    token = flow.credentials.token

    return {"access_token": token}
