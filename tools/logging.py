# import libraries
from datetime import date, datetime
from tools.reader import read_configuration

async def qlogging(log_type, the_url, the_client, req_headers, status, message=''):
    """
    This function will keep the calling requests
    """
    # log type could be access or error
    # # # System Values # # # 
    ROOT = read_configuration('root_documents_path')
    LOGGING = read_configuration('log_files_path_api')
    ENCODING = read_configuration('encoding')
    SEPARATOR = read_configuration('separator')

    today = str(date.today())
    now = str(datetime.now())

    txt_fullname = ROOT + LOGGING + today + '_' + log_type + read_configuration('txt_document')

    with open(txt_fullname, mode="a", encoding=ENCODING) as f:
        f.write(now + SEPARATOR + the_url + SEPARATOR + the_client + SEPARATOR + req_headers + SEPARATOR + status + SEPARATOR + message + '\n')
        f.close()
