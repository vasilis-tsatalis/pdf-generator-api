import os
import base64
from base64 import b64encode, b64decode

async def decode_from_base64_to_document(text: str, fullname: str):
    base64_message = text
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes, validate=True)
    with open(fullname, 'wb') as fn:
        fn.write(message_bytes)
    fn.close()
    if os.path.isfile(fullname):
        status = True
    else:
        status = False
    return status

async def document_convert_to_base64(fullname: str, encoding):
    """this function convert a document file to base64 format"""

    with open(fullname, 'rb') as open_file:
        byte_content = open_file.read()
    open_file.close()
    base64_bytes = b64encode(byte_content)
    base64_string = base64_bytes.decode(encoding)
    return base64_string

async def convertor_to_base64(text: str):
    """this function convert a text to base64 format"""
    base64_message = text
    base64_bytes = base64_message.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('utf-8')
    return message

async def encode_from_file_to_base64(fullname: str):
    with open(fullname, "rb") as file:
        encoded_string = base64.b64encode(file.read())
        return encoded_string
