# import libraries
from datetime import date, datetime
from decouple import config

async def qlogging(log_type, log_uuid, the_url, the_client, req_headers, status, message=''):
    """
    This function will keep the calling requests
    """
    # log type could be access or error
    # # # System Values # # # 

    ROOT = f"{config('ROOT_PATH')}"
    LOGGING = f"{config('LOG_FILES_PATH_API')}"
    ENCODING = f"{config('ENCODING')}"
    SEPARATOR = f"{config('SEPARATOR')}"

    today = str(date.today())
    now = str(datetime.now())

    txt_fullname = ROOT + LOGGING + today + '_' + log_type + f"{config('LOG_FORMAT')}"

    with open(txt_fullname, mode="a", encoding=ENCODING) as f:
        f.write(now + SEPARATOR + "ID: " + log_uuid + SEPARATOR + the_url + SEPARATOR + the_client + SEPARATOR + req_headers + SEPARATOR + status + SEPARATOR + message + '\n')
        f.close()
