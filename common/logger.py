import logging
import logging.handlers
from common import contants
import os
from common.config import ReadConfig

config = ReadConfig()

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel('DEBUG')#总开关设置为最低级别

    fmt = "%(asctime)s - %(levelname)s - %(name)s - %(message)s - [%(filename)s:%(lineno)d]"
    formate = logging.Formatter(fmt)
    file_name = os.path.join(contants.logs_path,'case.log')
    #日志清理
    file_handler = logging.handlers.RotatingFileHandler(file_name,maxBytes=20*1024*1024,backupCount=10,
                                                        encoding='utf-8')
    level = config.get('log','file_handler')
    file_handler.setLevel(level)
    file_handler.setFormatter(formate)

    console_handler = logging.StreamHandler()
    level = config.get('log', 'console_handler')
    console_handler.setLevel(level)
    console_handler.setFormatter(formate)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

if __name__ == '__main__':
    logger=get_logger('register')
    logger.error('this is error')
    logger.debug('this is debug')
    logger.info('this is info')

