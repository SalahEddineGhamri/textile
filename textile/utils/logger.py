# utils/logger.py

import logging
import os
from datetime import datetime
from textile.config import LOG_PATH

LOG_FILE_COUNT = 3

def setup_logger(log_file='textile.log', level=logging.INFO):

    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)

    log_file_path = os.path.join(LOG_PATH, log_file)
    clean_old_logs()

    logger = logging.getLogger('textile_logger')
    logger.setLevel(level)

    f_handler = logging.FileHandler(log_file)
    f_handler.setLevel(level)

    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)

    logger.addHandler(f_handler)

    return logger

def clean_old_logs():
    files = sorted([os.path.join(LOG_PATH, f) for f in os.listdir(LOG_PATH) if os.path.isfile(os.path.join(LOG_PATH, f))],
                   key=os.path.getmtime)

    while len(files) > LOG_FILE_COUNT:
        os.remove(files.pop(0))

def get_logger():
    return logging.getLogger('textile_logger')

log_file = f'{LOG_PATH}/textile_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logger = setup_logger(log_file)
