# import libraries
from fastapi import FastAPI
from decouple import config
# include other functionality
from routes.home import home_router
from routes.templates import template_router
from routes.documents import document_router
# =======================================================

# Define app as fastapi app
description = """

Document Generator Api helps you do awesome stuff. 🚀 \n

## Templates

* **Create templates**

* **Read templates**

* **Delete templates**

## Documents

* **Create documents**

"""

app = FastAPI(
    title = "Document Conventor Api (DGA)",
    description = description + "\b",
    version = "0.1.0",
    openapi_url=f"{config('API_URL')}/openapi.json",
    docs_url=f"{config('API_URL')}/documentation", 
    redoc_url=f"{config('API_URL')}/redocs",
    contact = {
        "name": "Vasilis Tsatalis",
        "url": "https://vasilis-tsatalis.w3spaces.com/"
    },
    license_info = {
        "name": "MIT License",
        "url": "https://www.mit.edu/~amini/LICENSE.md",
    },
    terms_of_service= 
        "https://github.com/vasilis-tsatalis/pdf-generator-api.git",
)

# Main Routes of API
app.include_router(home_router)
app.include_router(template_router)
app.include_router(document_router)
