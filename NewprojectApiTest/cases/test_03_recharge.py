# -*- coding:utf-8 -*-
# @time     :2019/5/2821:56
# @Author   :xiaowang
# @File     :lemon_requests_0527.py

from libs.ddt import ddt, data
import unittest
import inspect
import json

from scripts.handle_requests import HandleRequest
from scripts.handle_config import HandleConfig
from scripts.handle_excel import HandleExcel
from scripts.handle_log import do_log
from scripts.constants import TEST_DATAS_FILE_PATH, CONFIG_USER_FILE_PATH, CONFIG_FILE_PATH
from scripts.handle_context import HandleContext
from scripts.handle_pymusql import HandleMysql

do_excel = HandleExcel(TEST_DATAS_FILE_PATH, "recharge")


@ddt
class HandleRecharge(unittest.TestCase):
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
        cls.send_res = HandleRequest()
        cls.handle_mysql = HandleMysql()
        cls.do_config = HandleConfig(CONFIG_FILE_PATH)

        cls.de_config = HandleConfig(CONFIG_USER_FILE_PATH)
        login_data = {"mobilephone": cls.de_config("invest_user", "mobilephone"),
                      "pwd": cls.de_config("invest_user", "pwd")}
        login_url = cls.do_config("api", "url") + "/member/login"
        cls.send_res(method="post", url=login_url, data=login_data)

        do_log.info("\n{:*^40s}".format("开始执行充值功能用例"))

    @classmethod
    def tearDownClass(cls):
        """
        所有测试类执行之后执行此程序。
        :return:
        """
        cls.send_res.close()
        cls.handle_mysql.close()
        do_log.info("\n{:*^40s}".format("充值功能用例执行结束"))

    @data(*case_list)
    def test_recharge(self, data_ceses):
        do_log.info("\nRunning Test Method: {}".format(inspect.stack()[0][3]))
        run_success_msg = self.do_config("msg", "success_result")
        run_fail_msg = self.do_config("msg", "fail_result")

        case_id = data_ceses.case_id
        msg = data_ceses.title
        case_data = HandleContext().register_parameterization(data_ceses.data)
        case_url = self.do_config("api", "url") + data_ceses.url

        check_sql = data_ceses.check_sql
        if check_sql:
            check_sql = HandleContext.register_parameterization(check_sql)
            mysql_data = self.handle_mysql(sql=check_sql)
            amount_recharge_before = float(mysql_data["LeaveAmount"])
            amount_recharge_before = round(amount_recharge_before, 2)

        actual_res = self.send_res(method=data_ceses.method,
                                   url=case_url,
                                   data=case_data)

        try:
            self.assertEqual(200, actual_res.status_code,
                             msg="测试{}时，请求失败！状态码为:{}".format(msg, actual_res.status_code))
        except ArithmeticError as e:
            do_log.error("具体异常为：{}".format(e))
            raise

        actual_code = actual_res.json()["code"]
        try:
            self.assertEqual(str(data_ceses.expected), actual_code, msg="测试{}失败".format(msg))
            if check_sql:
                check_sql = HandleContext.register_parameterization(check_sql)
                mysql_data = self.handle_mysql(sql=check_sql)
                amount_recharge_after = float(mysql_data["LeaveAmount"])
                amount_recharge_after = round(amount_recharge_after, 2)
                data_dict = json.loads(case_data, encoding="utf-8")
                case_amount = float(data_dict["amount"])

                actual_amount = round(amount_recharge_before + case_amount, 2)

                self.assertEqual(actual_amount, amount_recharge_after, msg="测试{}失败".format(msg))

        except AssertionError as e:
            do_log.error("具体异常为：{}".format(e))
            do_excel.write_result(row=case_id + 1, actual=actual_res.text, result=run_fail_msg)
            raise e
        else:
            do_excel.write_result(row=case_id + 1, actual=actual_res.text, result=run_success_msg)


if __name__ == '__main__':
    unittest.main()
    # case_list = do_excel.get_cases()
    # case = case_list[0].data
    # data = int(eval(case)["amount"])
    # # data = case["amount"]
    # print(type(data), data)
    # pass





