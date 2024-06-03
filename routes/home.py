from fastapi import APIRouter
from fastapi.responses import HTMLResponse

home_router = APIRouter()

@home_router.get("/", response_class=HTMLResponse)
async def health_check():
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

