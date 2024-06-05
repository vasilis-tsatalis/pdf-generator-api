import uvicorn
import os
from decouple import config
import logging
from datetime import date

HOST = config('API_HOST')
PORT = config('API_PORT_1')
LOG_PATH = config('ROOT_PATH') + config('LOG_FILES_PATH_ENGINE')
LOG_EXT = config('LOG_FORMAT')
LOG_LEVEL = config('LOG_LEVEL')

if __name__ == '__main__':
    print("This APP runs in the " + config('API_ENVIRONMENT') + " environment called DGA Web App v2 on port " + PORT)
    print("ID of main process is: {}".format(os.getpid()))
    today = str(date.today())
    uvicorn.run(
        "app:app",
        host = HOST,
        port = int(PORT),
        reload = True,
        workers = 2,
        log_level = LOG_LEVEL,
        access_log=True,
        use_colors=True,
        log_config=logging.basicConfig(
            filename=f'{LOG_PATH}{today}_handler_1{LOG_EXT}',
            filemode='a',
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',
            ),
        ssl_keyfile = config('KEY_FILE'),
        ssl_certfile = config('CERT_FILE')
        )
