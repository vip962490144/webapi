# -*- coding:utf-8 -*-
# @time     :2019/5/2821:56
# @Author   :xiaowang
# @File     :lemon_requests_0527.py

from libs.ddt import ddt, data
import unittest
import inspect

from scripts.handle_requests import HandleRequest
from scripts.handle_config import do_config
from scripts.handle_excel import HandleExcel
from scripts.handle_log import do_log
from scripts.constants import TEST_DATAS_FILE_PATH
from scripts.handle_context import HandleContext

do_excel = HandleExcel(TEST_DATAS_FILE_PATH, "login")


@ddt
class HandleLogin(unittest.TestCase):
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
        do_log.info("\n{:*^40s}".format("开始执行登录功能用例"))

    @classmethod
    def tearDownClass(cls):
        """
        所有测试类执行之后执行此程序。
        :return:
        """
        cls.send_res.close()
        do_log.info("\n{:*^40s}".format("登录功能用例执行结束"))

    @data(*case_list)
    def test_case_01(self, data_ceses):
        do_log.info("\nRunning Test Method: {}".format(inspect.stack()[0][3]))
        case_id = data_ceses.case_id
        msg = data_ceses.title
        case_data = HandleContext().register_parameterization(data_ceses.data)
        case_url = do_config("api", "url") + data_ceses.url
        actual = self.send_res(method=data_ceses.method,
                               url=case_url,
                               data=case_data)
        run_success_msg = do_config("msg", "success_result")
        run_fail_msg = do_config("msg", "fail_result")
        try:
            self.assertEqual(data_ceses.expected, actual.text, msg="测试{}失败".format(msg))
        except AssertionError as e:
            do_log.error("具体异常为：{}".format(e))
            do_excel.write_result(row=case_id + 1, actual=actual.text, result=run_fail_msg)
            raise e
        else:
            do_excel.write_result(row=case_id + 1, actual=actual.text, result=run_success_msg)


if __name__ == '__main__':
    unittest.main()



