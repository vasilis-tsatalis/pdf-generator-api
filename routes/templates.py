# import libraries
from fastapi import APIRouter, Depends, status, HTTPException, Request
from typing import List
from decouple import config
import os
import json
import secrets
import uuid
from datetime import datetime
# include other functionality
from auth.authentication import authenticate_user
from tools.logging import qlogging
from tools.reader import read_templates_details
from tools.base64 import decode_from_base64_to_document, encode_from_file_to_base64
from tools.merge import findDocument_MergeFields
from tools.writer import write_json_bindings
from schemas.templates import Template, TemplateCreate, Template_Content


# # # Load System Values .env # # # 
ENCODING = f"{config('ENCODING')}"
DOCX_FORMAT = f"{config('DOCX_FORMAT')}"
ROOT_PATH = f"{config('ROOT_PATH')}"
TEMPLATES_PATH = f"{config('TEMPLATES_PATH')}"

# Route base url
template_router = APIRouter()

# Create method
@template_router.post("/", response_model=Template, status_code = status.HTTP_201_CREATED)
async def create_new_template(template: TemplateCreate, request: Request, username: str = Depends(authenticate_user)):
    """
    This function will convert base64 and create a new template in docx format
    """
    REQUEST_ID = str(uuid.uuid4())
    # # # Find Date # # #
    now = datetime.now() # current date and time
    date_time = now.strftime("%Y%m%d%H%M%S")
    timestamp = now.strftime("%Y-%m-%d_%H%M%S")

    template_name = template.name.lower()    
    template_lang = template.language.upper()
    template_code = REQUEST_ID # secrets.token_hex(16)
    template_fullname = ROOT_PATH + TEMPLATES_PATH + template_code + DOCX_FORMAT
    # write received value in txt temporary file
    template_status  = await decode_from_base64_to_document(template.content, template_fullname)
    # Procedure check
    if template_status == True and os.path.exists(template_fullname):
        # find merge fields into the document
        merge_fields = await findDocument_MergeFields(template_fullname)
        # python object to be appended
        data = {
                "code": template_code,
                "name": template_code + DOCX_FORMAT,
                "origin_name": template_name, 
                "language": template_lang,
                "merge_fields": merge_fields,
                "timestamp": timestamp,
                "created_by": username
                }
        await write_json_bindings(data)
        headers = dict(request.headers)
        message = "Template with code " + template_code + " has been created from the user: " + username
        await qlogging('access', REQUEST_ID, str(request.url), str(request.client), str(headers), '201', message)
        return data

    # an error occured
    headers = dict(request.headers)
    headers['username'] = username
    message = "Unable to create template from the user: " + username
    await qlogging('error', REQUEST_ID, str(request.url), str(request.client), str(headers), '501', message)
    return HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, 
            detail=message, 
            headers={"WWW-Authenticate": "Basic", "Content-Type": "application/json"},
        )


# Read all method
@template_router.get("/", response_model=List[Template], status_code = status.HTTP_200_OK)
async def read_templates(request: Request, username: str = Depends(authenticate_user), skip: int = 0, limit: int = 300):

    REQUEST_ID = str(uuid.uuid4())
    now = datetime.now() # current date and time
    date_time = now.strftime("%Y%m%d%H%M%S")
    timestamp = now.strftime("%Y-%m-%d_%H%M%S")

    templates = await read_templates_details()
    user_templates = list(filter(lambda x: x['created_by'] == username, templates))
    headers = dict(request.headers)
    message = "All templates have been found for the user: " + username
    await qlogging('access', REQUEST_ID, str(request.url), str(request.client), str(headers), '200', message)
    return user_templates


# Read one method by id
@template_router.get("/{template_code}", response_model=Template, status_code = status.HTTP_200_OK)
async def read_template_details(template_code: str, request: Request, username: str = Depends(authenticate_user)):

    REQUEST_ID = str(uuid.uuid4())
    now = datetime.now() # current date and time
    date_time = now.strftime("%Y%m%d%H%M%S")
    timestamp = now.strftime("%Y-%m-%d_%H%M%S")

    templates = await read_templates_details()
    template = list(filter(lambda x: x['code'] == template_code, templates))
    if template:
        headers = dict(request.headers)
        message = "Read specific template with code: " + template_code + " from the user: " + username
        await qlogging('access', REQUEST_ID, str(request.url), str(request.client), str(headers), '200', message)
        return template[0]
    headers = dict(request.headers)
    message = "Template code not found for the user: " + username
    await qlogging('error', REQUEST_ID, str(request.url), str(request.client), str(headers), '404', message)    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=message,
        headers={"WWW-Authenticate": "Basic", "Content-Type": "application/json"},
        )

# Read content method by id
@template_router.get("/{template_code}/content", response_model=Template_Content, status_code = status.HTTP_200_OK)
async def read_template_content(template_code: str, request: Request, username: str = Depends(authenticate_user)):

    REQUEST_ID = str(uuid.uuid4())
    now = datetime.now() # current date and time
    date_time = now.strftime("%Y%m%d%H%M%S")
    timestamp = now.strftime("%Y-%m-%d_%H%M%S")

    templates = await read_templates_details()
    template = list(filter(lambda x: x['code'] == template_code, templates))
    if template:
        readed_template = template[0]
        template_fullname = ROOT_PATH + TEMPLATES_PATH + readed_template.get('name')
        encoded_template = await encode_from_file_to_base64(template_fullname)
        readed_template['content'] = encoded_template
        headers = dict(request.headers)
        message = "Read specific template with code: " + template_code + " from the user: " + username
        await qlogging('access', REQUEST_ID, str(request.url), str(request.client), str(headers), '200', message)
        return readed_template
    headers = dict(request.headers)
    message = "Template code not found for the user: " + username
    await qlogging('error', REQUEST_ID, str(request.url), str(request.client), str(headers), '404', message)    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=message,
        headers={"WWW-Authenticate": "Basic", "Content-Type": "application/json"},
        )

# Delete one method
@template_router.delete("/{template_code}", status_code = status.HTTP_202_ACCEPTED)
async def delete_template(template_code: str, request: Request, username: str = Depends(authenticate_user)):

    REQUEST_ID = str(uuid.uuid4())
    now = datetime.now() # current date and time
    date_time = now.strftime("%Y%m%d%H%M%S")
    timestamp = now.strftime("%Y-%m-%d_%H%M%S")
    
    templates = await read_templates_details()
    data = list(filter(lambda x: x['code'] == template_code, templates))
    if data:
        deleted_template = data[0]
        template_fullname = ROOT_PATH + TEMPLATES_PATH + deleted_template.get('name')
        with open(f"{config('BINDINGS_FILE')}", 'rb') as fp:
            jsondata = json.load(fp)                                                   
        json.dumps(jsondata, indent=4)
        fp.close()
        jsondata['documents'].remove(deleted_template)
        # Output the updated file with pretty JSON                                      
        open(f"{config('BINDINGS_FILE')}", "w").write(
            json.dumps(jsondata, sort_keys=True, indent=4, separators=(',', ': '))
        )

        # delete physical file
        if os.path.exists(template_fullname):
            os.remove(template_fullname)
        else:
            print("The file does not exist")

        return {'message': 'Template with code ' + template_code + ' has been deleted'}
    headers = dict(request.headers)
    headers['username'] = username
    message = "Template code not found"
    await qlogging('error', REQUEST_ID, str(request.url), str(request.client), str(headers), '404', message)    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=message,
        headers={"WWW-Authenticate": "Basic", "Content-Type": "application/json"},
        )
