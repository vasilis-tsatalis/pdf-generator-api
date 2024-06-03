# import libraries
from fastapi import FastAPI
from decouple import config
# include other functionality
from routes.home import home_router
from routes.templates import template_router
from routes.documents import document_router
# =======================================================

BASE_URL = f"{config('API_URL')}"

# Define app as fastapi app
description = """

Document Generator Api v2 helps you do awesome stuff. 🚀 \n

## Templates

* **Create template**

* **Read templates**

* **Read template content**

* **Delete template**

## Documents

* **Create document**

* **Read document**

"""

app = FastAPI(
    title = "Document Conventor Api v2 (DGA)",
    description = description + "\b",
    version = "0.2.2",
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
app.include_router(home_router,prefix=BASE_URL + f"{config('HOME_ROUTE')}",tags=[f"{config('HOME_TAG')}"])
app.include_router(template_router,prefix=BASE_URL + f"{config('TEMPLATES_ROUTE')}", tags=[f"{config('TEMPLATES_TAG')}"])
app.include_router(document_router,prefix=BASE_URL + f"{config('DOCUMENTS_ROUTE')}", tags=[f"{config('DOCUMENTS_TAG')}"])
