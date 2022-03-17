import os
from docx2pdf import convert  # convert docx to pdf

async def createPdf(input_file, output_file):
    """this function creates a new pdf document 
    based on a specific docx document"""
    #convert(r'' + input_file, r'' + output_file)
    convert(f'{input_file}',f'{output_file}')
    if os.path.isfile(output_file):
        status = True
    else:
        status = False
    return status


async def createTxt(content, output_file):
    """this function creates a new txt file 
    base on a specific string field"""
    with open(output_file, 'w') as open_file:
        open_file.write(content)
    open_file.close()
    
    if os.path.isfile(output_file):
        status = True
    else:
        status = False
    return status