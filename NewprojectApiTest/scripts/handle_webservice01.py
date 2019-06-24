# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2019/6/12 14:54 
  @Auth : 可优
  @File : handle_webservice.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
-------------------------------------------------
"""
import json

from suds.client import Client
import suds

from PreClass.LearnWebService.handle_log import do_log


class HandleWebServie:
    """
    定义发起webservice请求类
    """
    # def get_sendMCode(self, data):
    #     try:
    #         res = self.client.service.sendMCode(data)
    #     except Exception as e:
    #         do_log.error("出现异常：{}".format(e))
    #         res = e.fault.faultstring
    #
    #     return res
    #
    # def get_userRegister(self, data):
    #     try:
    #         res = self.client.service.userRegister(data)
    #     except Exception as e:
    #         do_log.error("出现异常：{}".format(e))
    #         res = e.fault.faultstring
    #
    #     return res
    #
    # def get_verifiedUserAuth(self, data):
    #     try:
    #         res = self.client.service.verifiedUserAuth(data)
    #     except Exception as e:
    #         do_log.error("出现异常：{}".format(e))
    #         res = e.fault.faultstring
    #
    #     return res
    #
    # def get_bindBankCard(self, data):
    #     try:
    #         res = self.client.service.bindBankCard(data)
    #     except Exception as e:
    #         do_log.error("出现异常：{}".format(e))
    #         res = e.fault.faultstring
    #
    #     return res

    def __call__(self, method, data):
        """

        :param method: 请求方式，为字符串，"sendMCode"、"userRegister"、"verifiedUserAuth"、"bindBankCard"
        :param data: 请求参数，可为json格式的字符串、字典类型的字符串、字典类型
        :return:
        """
        if method in ("sendMCode", ):
            url = "http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl"
        elif method in ("userRegister", "verifiedUserAuth", "bindBankCard"):
            url = "http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl"
        else:
            do_log.error("请求方法【{}】，有误！".format(method))
            return

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception as e:
                do_log.error("将json转换为Python类型时，出现异常：{}".format(e))
                data = eval(data)

        if not isinstance(data, dict):
            do_log.error("请求参数【{}】，不为字典类型！".format(data))
            return

        # 创建Client对象
        client = Client(url)
        request_method = getattr(client.service, method)    # 获取请求方式
        try:
            res = request_method(data)
            res = suds.sudsobject.asdict(res)
        except Exception as e:
            do_log.error("出现异常：{}".format(e))
            res = dict(e.fault)
        return res


if __name__ == '__main__':
    do_webservice = HandleWebServie()

    # params1 = {
    #     "client_ip": "172.16.100.1",
    #     "tmpl_id": "1",
    #     "mobile": "13866662234"
    # }
    # params2 = {
    #     "client_ip": "",
    #     "tmpl_id": "1",
    #     "mobile": "13866662234"
    # }
    # params3 = '{"client_ip": "172.16.100.1", "tmpl_id": "1", "mobile": "13866662235"}'
    #
    # print(do_webservice("sendMCode", params1))
    # print(do_webservice("sendMCode", params2))
    # print(do_webservice("sendMCode", params3))

    params4 = {
        "verify_code": "773775",
        "user_id": "keyou1",
        "channel_id": "1",
        "pwd": "123456",
        "mobile": "13866662234",
        "ip": "172.16.100.2"
    }
    params5 = {
        "verify_code": "",
        "user_id": "",
        "channel_id": "1",
        "pwd": "123456",
        "mobile": "13866662234",
        "ip": "172.16.100.2"
    }

    params6 = '{"verify_code": "773775", "user_id": "", "channel_id": "1", "pwd": "123456", "mobile": "13866662234", ' \
              '"ip": "172.16.100.2"}'

    print(do_webservice("userRegister", params4))
    print(do_webservice("userRegister", params5))
    print(do_webservice("userRegister", params6))
