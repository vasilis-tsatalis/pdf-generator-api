# import libraries
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
# include other functionality
from tools.logging import qlogging
from tools.reader import read_authenticated_users
# =======================================================
security = HTTPBasic()

async def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):

    auth_users = await read_authenticated_users()
    the_user = list(filter(lambda x: x['username'] == credentials.username, auth_users))
    if the_user:
        API_PASS = the_user[0]['password']
        correct_password = secrets.compare_digest(credentials.password, API_PASS)
        if correct_password:
            return credentials.username
    
    # add logging function for errors
    message = "Unauthorized 401"
    await qlogging('error', 'null', 'Request Blocked', credentials.username, 'Authentication', '401', message)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message,
        headers={"WWW-Authenticate": "Basic"},
    )
