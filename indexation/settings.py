import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ES_CODE_DU_TRAVAIL = 'code_du_travail'
ES_FAQ = 'faq'
ES_FICHES_SERVICE_PUBLIC = 'fiches_service_public'

def get_logger(name, level=logging.INFO):
    console = logging.StreamHandler()
    formatter = logging.Formatter(fmt='[%(levelname)s - %(funcName)s] %(message)s')
    console.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(console)
    logger.setLevel(level)
    return logger
