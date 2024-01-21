from fastapi import APIRouter, Request, HTTPException, Depends  # Add Depends here
from google_auth_oauthlib.flow import Flow
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
from starlette.responses import JSONResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
import os


# Load environment variables
load_dotenv()

# Set the Google OAuth 2.0 information
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
CLIENT_SECRETS_FILE = os.path.join(os.getcwd(), 'routers', 'client_secret_611910765428-fge3l5u39si60j56utd6bssccn30j294.apps.googleusercontent.com.json')

# Create an APIRouter instance for authentication routes
router = APIRouter(prefix="/auth", tags=["auth"])

# Define the OAuth2 scheme using Google's OAuth 2.0 endpoints
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/v2/auth",
    tokenUrl="https://oauth2.googleapis.com/token"
)

# Login route: redirects the user to Google's OAuth 2.0 server
@router.get("/login")
async def login(request: Request):
    try:
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=['https://www.googleapis.com/auth/drive'],
            redirect_uri=GOOGLE_REDIRECT_URI
        )

    
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )


        
        response = RedirectResponse(authorization_url)
        response.set_cookie('oauth2_state', state, httponly=True, samesite='Lax')  # Set a secure cookie for state
        return response

    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))
    

# Callback route: handles the response from Google's OAuth 2.0 server
@router.get("/callback")
async def callback(request: Request):
    # Retrieve the state and code from the query parameters
    state = request.query_params.get('state')
    code = request.query_params.get('code')

    # You can log the state and code here for debugging purposes
    # print(f"State: {state}, Code: {code}")

    if not state:
        return JSONResponse(content={"detail": "State parameter is missing"}, status_code=400)

    # Compare the state parameter to the state cookie
    state_cookie = request.cookies.get('oauth2_state')
    if not state_cookie or state_cookie != state:
        return JSONResponse(content={"detail": "State mismatch"}, status_code=400)

    try:
        # Initialize the flow using the saved information
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=['https://www.googleapis.com/auth/drive'],
            state=state,
            redirect_uri=GOOGLE_REDIRECT_URI
        )

        # Use the code to fetch the token
        flow.fetch_token(code=code)

        # Extract token information
        credentials = flow.credentials
        response_data = {
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes
        }

        return JSONResponse(content=response_data)
    except Exception as e:
        # You can log the exception message here for debugging purposes
        # print(f"Exception: {e}")
        return JSONResponse(content={"detail": str(e)}, status_code=500)