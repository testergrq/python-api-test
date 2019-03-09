import unittest
from common import contants
from common.request import Request
from common.do_excel import DoExcel
from lib.ddt_new import ddt, data
from common import logger
from common.mysql import MysqlUtil
import json

logger=logger.get_logger(logger_name='case')

@ddt
class RechargeTest(unittest.TestCase):
    do_excel = DoExcel(contants.excel_path)
    recharge_cases = do_excel.read_data("recharge")

    @classmethod
    def setUpClass(cls):
        cls.request = Request()

    def setUp(self):
        self.mysql = MysqlUtil(return_dict=True)
    # logger.info(type(max), max)

    @data(*recharge_cases)
    def test_recharge(self, case):
        logger.info('开始执行第{0}条用例'.format(case.id))
        data_dict = json.loads(case.data)
        sql_1 = 'select LeaveAmount from future.member where mobilephone =18566668888'
        results_1 = self.mysql.fetch_one(sql_1)
        member_1 = results_1['LeaveAmount']
        resp = self.request.request(case.method, case.url, data_dict)
        try:
            self.assertEqual(case.expected, resp.json()['code'])
            if resp.json()['msg'] == '充值成功':
                sql_2 = 'select * from future.member where mobilephone ={0}'. \
                    format(data_dict['mobilephone'])
                results_2 = self.mysql.fetch_all(sql_2)
                member_2 = results_2[0]
                self.assertEqual(member_1+500000,member_2['LeaveAmount'])#判断充值后余额是否正确
                sql_3 = 'select incomemembermoney from future.financelog ORDER BY createtime DESC LIMIT 1'
                results_3 = self.mysql.fetch_one(sql_3)#字典
                member_3 = results_3['incomemembermoney']#从字典取值
                self.assertEqual(member_2['LeaveAmount'], member_3)#判断会员流水记录表余额是否与会员表余额一致
            self.do_excel.write_data('recharge',case.id + 1, resp.text, 'PASS')
            logger.info('第{0}条用例执行结果:pass'.format(case.id))
        except AssertionError as e:
            self.do_excel.write_data('recharge',case.id + 1, resp.text, 'FAIL')
            logger.error('第{0}条用例执行结果:fail'.format(case.id))
            raise e

    def tearDown(self):
        self.mysql.close()

    @classmethod
    def tearDownClass(cls):
        cls.request.session.close()