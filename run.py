# coding=utf-8
import unittest

from lib import HTMLTestRunnerNew

from common import contants

discover = unittest.defaultTestLoader.discover(contants.testcases_path, pattern='*test.py', top_level_dir=None)

with open(contants.reports_html, 'wb+') as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file,
                                              title='API',
                                              description='API测试报告',
                                              tester='深圳-改变自己')
    runner.run(discover)