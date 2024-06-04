import uvicorn
import os
from decouple import config
import logging
from datetime import date, datetime

PORT = config('API_PORT_1')
LOG_PATH = config('ROOT_PATH') + config('LOG_FILES_PATH_ENGINE')
LOG_EXT = config('LOG_FORMAT')

if __name__ == '__main__':
    print("This is the " + config('API_ENVIRONMENT') + " environment for DGA Web App v2 on port " + config('API_PORT_1'))
    print("ID of main process is: {}".format(os.getpid()))
    today = str(date.today())
    uvicorn.run(
        "app:app",
        host = config('API_HOST'),
        port = int(config('API_PORT_1')),
        reload = True,
        workers = 2,
        log_level = config('LOG_LEVEL'),
        access_log=True,
        log_config=logging.basicConfig(
            filename=f'{LOG_PATH}{today}_handler_1{LOG_EXT}',
            filemode='a',
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',
            ),
        ssl_keyfile = config('KEY_FILE'),
        ssl_certfile = config('CERT_FILE')
        )
