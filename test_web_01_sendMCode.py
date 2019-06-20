# -*- coding:utf-8 -*-
# @time     :2019/5/2821:56
# @Author   :xiaowang
# @File     :lemon_requests_0527.py

from libs.ddt import ddt, data
import unittest
import inspect
import json
from suds.client import Client

from scripts.handle_config import do_config
from scripts.handle_excel import HandleExcel
from scripts.handle_log import do_log
from scripts.constants import TEST_DATAS_FILE_PATH
from scripts.handle_context import HandleContext
from scripts.handle_pymusql import HandleMysql
from scripts.handle_webservce import HandleWebservice

do_excel = HandleExcel(TEST_DATAS_FILE_PATH, "sendMCode")


@ddt
class HandlesendMCode(unittest.TestCase):
    """
    测试用例类
    """
    case_list = do_excel.get_cases()

    @classmethod
    def setUpClass(cls):
        """
        所有测试类执行之前执行此程序。
        :return:
        """
        do_log.info("\n{:*^40s}".format("开始执行发送验证码功能用例"))

    @classmethod
    def tearDownClass(cls):
        """
        所有测试类执行之后执行此程序。
        :return:
        """
        do_log.info("\n{:*^40s}".format("发送验证码功能用例执行结束"))

    @data(*case_list)
    def test_case_01(self, data_ceses):
        do_log.info("\nRunning Test Method: {}".format(inspect.stack()[0][3]))
        case_id = data_ceses.case_id
        msg = data_ceses.title
        new_data = json.loads(data_ceses.data)
        case_url = do_config("web api", "url") + data_ceses.url
        do_client = HandleWebservice(case_url)
        actual = do_client(method=data_ceses.method, data=new_data)
        run_success_msg = do_config("msg", "success_result")
        run_fail_msg = do_config("msg", "fail_result")
        # mobile = new_data['mobile']
        # if len(mobile) == 11:
        #     # 获取excel中data数据输入的手机号。
        #     db = do_config("web api", "db") + new_data['mobile'][9:]
        #     table = do_config("web api", "table") + new_data['mobile'][8:9]
        #     db_table = db + "." + table
        #
        #     actual_captcha = HandleMysql().is_existed_mobile_captcha(db_table, mobile)
        #     HandleContext.captcha = actual_captcha['Fverify_code']

        try:
            self.assertEqual(json.loads(data_ceses.expected)["retCode"], actual["retCode"], msg="测试{}失败".format(msg))
        except AssertionError as e:
            do_log.error("具体异常为：{}".format(e))
            do_excel.write_result(row=case_id + 1, actual=actual, result=run_fail_msg)
            raise e
        else:
            do_excel.write_result(row=case_id + 1, actual=actual, result=run_success_msg)


if __name__ == '__main__':
    unittest.main()
    # data = '{"client_ip": "192.168.3.1", "tmpl_id": "1", "mobile": "18366661234"}'
    #
    # print(json.loads(data)["mobile"])



