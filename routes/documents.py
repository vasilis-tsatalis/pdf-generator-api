# import libraries
from fastapi import APIRouter, Depends, status, HTTPException, Request
from decouple import config
import os
import secrets
from datetime import datetime
# include other functionality
from auth.authentication import authenticate_user
from tools.logging import qlogging
from tools.reader import read_configuration, read_templates_details
from tools.merge import createDocument
from tools.convert import createPdf
from tools.base64 import document_convert_to_base64
from schemas.documents import DocumentCreate, DocumentContent


# # # Load System Values # # # 
ENCODING = read_configuration('encoding')
DOCX_FORMAT = read_configuration('ms_word_document')
PDF_FORMAT = read_configuration('pdf_document')
ROOT_PATH = read_configuration('root_documents_path')
TEMPLATES_PATH = read_configuration('templates_path')
TEMPORARY_PATH = read_configuration('temporary_documents_path')
PDFDOCUMENT_PATH = read_configuration('pdf_documents_path')

# # # Find Date # # #
now = datetime.now() # current date and time
date_time = now.strftime("%Y%m%d%H%M%S")
timestamp = now.strftime("%Y-%m-%d_%H%M%S")

# Route base url
document_router = APIRouter(
    prefix=f"{config('API_URL')}/documents",
    tags=['Documents']
)


# Create document from template
@document_router.post("/template/{template_code}", response_model=DocumentContent, status_code = status.HTTP_201_CREATED)
async def create_document_from_template(template_code: str, document: DocumentCreate, request: Request, username: str = Depends(authenticate_user)):
    templates = await read_templates_details()
    template = list(filter(lambda x: x['code'] == template_code, templates))
    if not template:
        headers = dict(request.headers)
        headers['username'] = username
        message = "Template code not found"
        await qlogging('error', str(request.url), str(request.client), str(headers), '404', message)    
        raise HTTPException(
            status_code=404, 
            detail=message,
            headers={"WWW-Authenticate": "Basic", "Content-Type": "application/json"},
            )

    # build template fullname
    template_fullname = ROOT_PATH + TEMPLATES_PATH + template_code + DOCX_FORMAT
    # build temporary docx document name
    docx_temp_name = date_time + '_' + template_code + '_' + DOCX_FORMAT
    merge_fullname = ROOT_PATH + TEMPORARY_PATH + docx_temp_name
    # build document name
    file_name = secrets.token_hex(12) + str(date_time) + PDF_FORMAT
    document_fullname = ROOT_PATH + PDFDOCUMENT_PATH + file_name
    
#################################################################################
    # Convert Requested data to be acceptable
    # Initialize values
    _lists = []
    _temp_list = []
    _temp_list_dictionary = {}
    _working_list_value = []
    final_dictionary = {}

    received_data = document.content
    # Iterating through the json list
    for item in received_data['metadata']:

        if (item['mergetype'] == 'object') or (item['mergetype'].__contains__('object')):
            final_dictionary[item['mergename']] = item['mergevalue']

        elif (item['mergetype'] not in _lists) and (item['mergetype'].__contains__('list')):
            _lists.append(item['mergetype'])

        else:
            # expand in the future for other data types
            continue

    # check if there are lists for document content
    if len(_lists) != 0:

        for list_name in _lists:

            _temp_list = list(filter(lambda x: x['mergetype'] == list_name, received_data['metadata']))

            # Sort the list by line key to find 
            # last record counter number
            _temp_list = sorted(_temp_list, key = lambda x: x['line'])
            # find last record into the list
            last_record = _temp_list[-1]
            last_record_counter_number = int(last_record['line'])
            # Define a value for reading current line
            current_line = 1
            # # 
            while current_line <= last_record_counter_number:
                # read record for specific line into the list
                for item in _temp_list:

                    if int(item['line']) == current_line:

                        _temp_list_dictionary[item['mergename']] = item['mergevalue']

                current_line += 1
                item = {}
                _working_list_value.append(_temp_list_dictionary)
                _temp_list_dictionary = {}
                
            final_dictionary[list_name] = _working_list_value
            _temp_list = []
            _working_list_value = []

#################################################################################
    # create temporary docx document and merge content
    status_temp = await createDocument(template_fullname, final_dictionary, merge_fullname)
    if os.path.exists(merge_fullname):
        # convert and store document from docx to pdf
        status_doc = await createPdf(merge_fullname, document_fullname)
        if status_doc == True and os.path.exists(document_fullname):
            os.remove(merge_fullname)

            headers = dict(request.headers)
            headers['username'] = username
            message = "Document from template_code " + template_code + " has been created: " + file_name
            await qlogging('access', str(request.url), str(request.client), str(headers), '201', message)           
            b64_data = await document_convert_to_base64(document_fullname, ENCODING)

            docu_final = {
                "template_code": template_code,
                "name": file_name,
                "encoding": b64_data
            }
            return docu_final
    # an error occured
    headers = dict(request.headers)
    headers['username'] = username
    message = "Unable to create pdf document"
    await qlogging('error', str(request.url), str(request.client), str(headers), '501', message)
    return HTTPException(
            status_code=501, 
            detail=message, 
            headers={"WWW-Authenticate": "Basic", "Content-Type": "application/json"},
        )
