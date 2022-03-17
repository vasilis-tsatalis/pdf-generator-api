from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from decouple import config

home_router = APIRouter(
    prefix=f"{config('API_URL')}/",
    tags=['Default Home Page']
)

@home_router.get("/", response_class=HTMLResponse)
async def index():
    return """
        <html>
            <head>
                <title>DGA</title>
            </head>
            <body>
                <h3><i>Document Generator Api</i></h3>
            </body>
        </html>
    """

