import unittest
from common import contants
from common.request import Request
from common.do_excel import DoExcel
from ddt import ddt, data
from common import context
from common.mysql import MysqlUtil
from common.context import Context
from common import logger

logger = logger.get_logger(logger_name='case')


@ddt
class BidloanTest(unittest.TestCase):
    do_excel = DoExcel(contants.excel_path)
    bidloan_cases = do_excel.read_data("bidloan")

    @classmethod
    def setUpClass(cls):  # 每个测试类里面去运行的操作放到类方法里面
        cls.request = Request()
        cls.mysql = MysqlUtil()

    def setUp(self):  # 每个测试方法里面去运行的操作放到setup里面
        pass

    @data(*bidloan_cases)
    def test_bidloan(self, case):
        logger.info('开始执行第{0}条用例'.format(case.id))
        data_new = context.replace(case.data)  # 查找参数化的测试数据，动态替换
        resp = self.request.request(case.method, case.url, data_new)
        try:
            self.assertEqual(case.expected, resp.json()['code'])
            self.do_excel.write_data('bidloan', case.id + 1, resp.text, 'PASS')
            logger.info('第{0}条用例执行结果:pass'.format(case.id))
            # 判断是否加标成功，如果成功就按照借款人id去数据库查询最新的loanid
            if resp.json()['msg'] == '加标成功':
                loan_member_id = getattr(Context, 'loan_member_id')
                sql = "select id from future.loan where memberID='{0}'" \
                      " order by createTime desc limit 1".format(loan_member_id)
                loan_id = self.mysql.fetch_one(sql)[0]
                logger.info(type(loan_id))
                setattr(Context, 'loan_id', str(loan_id))  # 记得转成str,后续通过正则替换
        except AssertionError as e:
            self.do_excel.write_data('bidloan', case.id + 1, resp.text, 'FAIL')
            logger.error('第{0}条用例执行结果:fail'.format(case.id))
            raise e

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.request.session.close()
        cls.mysql.close()
