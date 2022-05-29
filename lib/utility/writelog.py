
import logging
from logging.handlers import TimedRotatingFileHandler
from lib.utility.path import *

def log():
    '''创建日志
    '''

    # 创建logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


    if not logger.hasHandlers():
        # 创建Handler
        fh = TimedRotatingFileHandler(LOG_PATH + "/log.txt", when="MIDNIGHT", encoding="utf-8")
        sh = logging.StreamHandler()

        # 创建Formatter
        formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s",
                                  datefmt = "%Y-%m-%d %H:%M:%S")

        fh.setFormatter(formatter)
        sh.setFormatter(formatter)


        logger.addHandler(fh)
        logger.addHandler(sh)



    # 输出log
    # logger.info(msg)
    return logger


