import os
import base64

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

async def document_convert_to_base64(fullname: str):
    """this function convert a document file to base64 format"""

    with open(fullname, 'rb') as fn:
        byte_content = fn.read()
    fn.close()
    message_bytes = byte_content.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

async def convertor_to_base64(text: str):
    """this function convert a text to base64 format"""
    base64_message = text
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message
