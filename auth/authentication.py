# import libraries
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from decouple import config
# include other functionality
from tools.logging import qlogging
# =======================================================
security = HTTPBasic()

async def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    API_USERNAME = f"{config('API_USERNAME')}"
    API_PASS = f"{config('API_PASS')}"
    correct_username = secrets.compare_digest(credentials.username, API_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, API_PASS)
    if not (correct_username and correct_password):
        # add logging function for errors
        message = "Unauthorized 401"
        await qlogging('error', 'Request Blocked', credentials.username, 'Authentication', '401', message)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
