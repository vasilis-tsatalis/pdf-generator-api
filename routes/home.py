from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from tools.logging import qlogging
import uuid

REQUEST_ID = str(uuid.uuid4())

home_router = APIRouter()

@home_router.get("/", response_class=HTMLResponse)
async def health_check(request: Request):
    
    headers = dict(request.headers)
    message = "Health Checker has been called"
    await qlogging('access', REQUEST_ID, str(request.url), str(request.client), str(headers), '200', message)
    
    return """
        <html>
            <head>
                <title>DGA</title>
            </head>
            <body>
                <h3><i>Document Generator Api v2</i></h3>
            </body>
        </html>
    """

