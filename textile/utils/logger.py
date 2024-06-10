# utils/logger.py

import logging
import os
from datetime import datetime

LOG_DIR = 'logs'
LOG_FILE_COUNT = 3

def setup_logger(log_file='textile.log', level=logging.INFO):

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    log_file_path = os.path.join(LOG_DIR, log_file)
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
    files = sorted([os.path.join(LOG_DIR, f) for f in os.listdir(LOG_DIR) if os.path.isfile(os.path.join(LOG_DIR, f))],
                   key=os.path.getmtime)

    while len(files) > LOG_FILE_COUNT:
        os.remove(files.pop(0))

def get_logger():
    return logging.getLogger('textile_logger')

log_file = f'./logs/textile_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logger = setup_logger(log_file)
