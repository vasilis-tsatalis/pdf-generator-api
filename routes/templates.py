# import libraries
from fastapi import APIRouter, Depends, status, HTTPException, Request
from typing import List
from decouple import config
import os
import json
import secrets
from datetime import datetime
# include other functionality
from auth.authentication import authenticate_user
from tools.logging import qlogging
from tools.reader import read_configuration, read_bindings, read_templates_details
from tools.base64 import decode_from_base64_to_document
from tools.merge import findDocument_MergeFields
from tools.writer import write_json_bindings
from schemas.templates import Template, TemplateCreate


# # # Load System Values # # # 
ENCODING = read_configuration('encoding')
DOCX_FORMAT = read_configuration('ms_word_document')
ROOT_PATH = read_configuration('root_documents_path')
TEMPLATES_PATH = read_configuration('templates_path')

# # # Find Date # # #
now = datetime.now() # current date and time
date_time = now.strftime("%Y%m%d%H%M%S")
timestamp = now.strftime("%Y-%m-%d_%H%M%S")

# Route base url
template_router = APIRouter(
    prefix=f"{config('API_URL')}/templates",
    tags=['Document Templates with merge fields']
)

# Create method
@template_router.post("/", response_model=Template, status_code = status.HTTP_201_CREATED)
async def create_new_template(template: TemplateCreate, request: Request, username: str = Depends(authenticate_user)):
    """
    This function will check if template name already exists,
    if not exists convert base64 and create a new template in app
    """
    template_name = template.name.lower()
    # check if template name already exists
    templates = await read_templates_details()
    exist_template = list(filter(lambda x: x['name'] == template_name, templates))
    if exist_template:
        headers = dict(request.headers)
        headers['username'] = username
        message = "Template name already exists: " + template_name
        await qlogging('error', str(request.url), str(request.client), str(headers), '400', message)
        raise HTTPException(
            status_code=400, 
            detail=message, 
            headers={"WWW-Authenticate": "Basic", "Content-Type": "application/json"},
        )
    else:
        template_lang = template.language.upper()
        template_code = secrets.token_hex(12) + str(date_time)
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
                    "name": template_name, 
                    "language": template_lang,
                    "merge_fields": merge_fields,
                    "timestamp": timestamp
                    }
            await write_json_bindings(data)
            headers = dict(request.headers)
            headers['username'] = username
            message = "Template with code " + template_code + " has been created"
            await qlogging('access', str(request.url), str(request.client), str(headers), '201', message)
            return data

        # an error occured
        headers = dict(request.headers)
        headers['username'] = username
        message = "Unable to create template"
        await qlogging('error', str(request.url), str(request.client), str(headers), '501', message)
        return HTTPException(
                status_code=501, 
                detail=message, 
                headers={"WWW-Authenticate": "Basic", "Content-Type": "application/json"},
            )


# Read all method
@template_router.get("/", response_model=List[Template], status_code = status.HTTP_200_OK)
async def read_templates(request: Request, username: str = Depends(authenticate_user), skip: int = 0, limit: int = 300):
    templates = await read_templates_details()
    headers = dict(request.headers)
    headers['username'] = username
    message = "All templates have been found"
    await qlogging('access', str(request.url), str(request.client), str(headers), '200', message)
    return templates


# Read one method by id
@template_router.get("/{template_code}", response_model=Template, status_code = status.HTTP_200_OK)
async def read_template_by_code(template_code: str, request: Request, username: str = Depends(authenticate_user)):
    templates = await read_templates_details()
    template = list(filter(lambda x: x['code'] == template_code, templates))
    if template:
        headers = dict(request.headers)
        headers['username'] = username
        message = "Read specific template with code: " + template_code
        await qlogging('access', str(request.url), str(request.client), str(headers), '200', message)
        return template[0]
    headers = dict(request.headers)
    headers['username'] = username
    message = "Template code not found"
    await qlogging('error', str(request.url), str(request.client), str(headers), '404', message)    
    raise HTTPException(
        status_code=404, 
        detail=message,
        headers={"WWW-Authenticate": "Basic", "Content-Type": "application/json"},
        )
 

# Delete one method
@template_router.delete("/{template_code}", status_code = status.HTTP_202_ACCEPTED)
async def delete_template_by_code(template_code: str, request: Request, username: str = Depends(authenticate_user)):
    templates = await read_templates_details()
    data = list(filter(lambda x: x['code'] == template_code, templates))
    if data:
        deleted_template = data[0]
        template_fullname = ROOT_PATH + TEMPLATES_PATH + deleted_template.get('code') + DOCX_FORMAT
        with open('properties/bindings.json', 'rb') as fp:
            jsondata = json.load(fp)                                                   
        json.dumps(jsondata, indent=4)
        fp.close()
        jsondata['documents'].remove(deleted_template)
        # Output the updated file with pretty JSON                                      
        open("properties/bindings.json", "w").write(
            json.dumps(jsondata, sort_keys=True, indent=4, separators=(',', ': '))
        )

        # delete physical file
        if os.path.exists(template_fullname):
            os.remove(template_fullname)
        else:
            print("The file does not exist")

        return {'message': 'Template with code ' + template_code + ' deleted'}
    headers = dict(request.headers)
    headers['username'] = username
    message = "Template code not found"
    await qlogging('error', str(request.url), str(request.client), str(headers), '404', message)    
    raise HTTPException(
        status_code=404, 
        detail=message,
        headers={"WWW-Authenticate": "Basic", "Content-Type": "application/json"},
        )
