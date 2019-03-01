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
class WithdrawTest(unittest.TestCase):
    do_excel = DoExcel(contants.excel_path)
    withdraw_cases = do_excel.read_data("withdraw")

    @classmethod
    def setUpClass(cls):
        cls.request = Request()

    def setUp(self):
        pass
    # logger.info(type(max), max)

    @data(*withdraw_cases)
    def test_withdraw(self, case):
        logger.info('开始执行第{0}条用例'.format(case.id))

        resp = self.request.request(case.method, case.url, case.data)
        try:
            self.assertEqual(case.expected, resp.json()['code'])
            self.do_excel.write_data('withdraw',case.id + 1, resp.text, 'PASS')
            logger.info('第{0}条用例执行结果:pass'.format(case.id))
        except AssertionError as e:
            self.do_excel.write_data('withdraw',case.id + 1, resp.text, 'FAIL')
            logger.error('第{0}条用例执行结果:fail'.format(case.id))
            raise e

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.request.session.close()
