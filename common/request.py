import requests
import json
from common.config import ReadConfig
from common import logger

logger = logger.get_logger('request')


class Request:
    def __init__(self):
        self.session = requests.sessions.session()

    def request(self, method, url, data=None):
        method = method.upper()
        config = ReadConfig()
        value = config.get('api', 'pre_url')
        url = value + url
        if data is not None and type(data) == str:
            data = json.loads(data)
        logger.info('method:{0} url:{1}'.format(method, url))
        logger.info('data:{0}'.format(data))

        if method == 'GET':
            resp = self.session.request(method, url=url, params=data)
            logger.info('response:{0}'.format(resp.text))
            return resp
        elif method == 'POST':
            resp = self.session.request(method, url=url, data=data)
            logger.info('response:{0}'.format(resp.text))
            return resp
        else:
            logger.error('unsupport method')

    def close(self):
        self.session.close()
