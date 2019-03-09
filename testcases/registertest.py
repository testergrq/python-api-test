import unittest
from common import contants
from common.request import Request
from common.do_excel import DoExcel
from lib.ddt_new import ddt, data
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
        self.mysql = MysqlUtil(return_dict=True)
        sql = 'select max(mobilephone) as max_phone from future.member'
        self.max = self.mysql.fetch_one(sql)['max_phone']
    # logger.info(type(max), max)

    # @unittest.skip('不要执行')
    @data(*register_cases)
    def test_register(self, case):
        logger.info('开始执行第{0}条用例'.format(case.id))
        data_dict = json.loads(case.data)#字典
        if data_dict['mobilephone'] == '${phone}':
            data_dict['mobilephone'] = int(self.max) + 1
        if data_dict['mobilephone'] == '${phone2}':
            data_dict['mobilephone'] = int(self.max) + 2
        resp = self.request.request(case.method, case.url, data_dict)
        try:
            self.assertEqual(case.expected, resp.text)
            if resp.json()['msg'] == '注册成功':
                sql = 'select * from future.member where mobilephone ={0}'.\
                    format(data_dict['mobilephone'])
                results = self.mysql.fetch_all(sql)#列表里嵌套字典
                self.assertEqual(1,len(results))#首先判断是否有成功插入数据
                member = results[0]#获取到这一条数据，是一个字典
                self.assertEqual(0,member['LeaveAmount'])#判断注册成功余额是否为0
                self.assertEqual(1, member['Type'])  # 判断注册用户类型是否为1
                self.assertNotEqual(data_dict['pwd'], member['Pwd'])  # 判断密码是否加密
                if 'regname' in data_dict.keys():
                    self.assertEqual(data_dict['regname'], member['RegName'])
                else:
                    self.assertEqual('小蜜蜂',member['RegName'])#判断用户名是小蜜蜂
            self.do_excel.write_data('register',case.id + 1, resp.text, 'PASS')
            logger.info('第{0}条用例执行结果:pass'.format(case.id))
        except AssertionError as e:
            self.do_excel.write_data('register',case.id + 1, resp.text, 'FAIL')
            logger.error('第{0}条用例执行结果:fail'.format(case.id))
            raise e

    def tearDown(self):
        self.mysql.close()

    @classmethod
    def tearDownClass(cls):
        cls.request.session.close()
