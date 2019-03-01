import unittest
from common import contants
from common.request import Request
from common.do_excel import DoExcel
from ddt import ddt, data
from common.mysql import MysqlUtil
import json
from common import logger


logger=logger.get_logger(logger_name='case')

@ddt
class RegisterTest(unittest.TestCase):
    do_excel = DoExcel(contants.excel_path)
    register_cases = do_excel.read_data('register')

    @classmethod
    def setUpClass(cls):
        cls.request = Request()

    def setUp(self):
        self.mysql = MysqlUtil()
        sql = 'select max(mobilephone) from future.member'
        self.max = self.mysql.fetch_one(sql)[0]
    # logger.info(type(max), max)

    # @unittest.skip('不要执行')
    @data(*register_cases)
    def test_register(self, case):
        logger.info('开始执行第{0}条用例'.format(case.id))
        data_dict = json.loads(case.data)
        if data_dict['mobilephone'] == '${phone}':
            data_dict['mobilephone'] = int(self.max) + 1
        if data_dict['mobilephone'] == '${phone2}':
            data_dict['mobilephone'] = int(self.max) + 2
        resp = self.request.request(case.method, case.url, data_dict)
        try:
            self.assertEqual(case.expected, resp.text)
            self.do_excel.write_data('register',case.id + 1, resp.text, 'PASS')
            logger.info('第{0}条用例执行结果:pass'.format(case.id))
        except AssertionError as e:
            self.do_excel.write_data('register',case.id + 1, resp.text, 'FAIL')
            logger.error('第{0}条用例执行结果:fail'.format(case.id))
            raise e

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.request.session.close()
