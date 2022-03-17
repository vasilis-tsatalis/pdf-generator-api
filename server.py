import uvicorn
import os
from decouple import config
import logging
from datetime import date, datetime

if __name__ == '__main__':
    print("This is the " + f"{config('API_ENVIRONMENT')}" + " environment for DGA")
    print("ID of main process is: {}".format(os.getpid()))
    today = str(date.today())
    uvicorn.run(
        "app:app",
        host = f"{config('API_HOST')}",
        port = int(f"{config('API_PORT_1')}"),
        reload = True,
        workers = 2,
        log_level = "info",
        access_log=True,
        log_config=logging.basicConfig(
            filename=f'./storage/logs/uvicorn/{today}_handler_1.log',
            filemode='a',
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',
            )
        #ssl_keyfile = './key.pem',
        #ssl_certfile = './cert.pem'
        )
