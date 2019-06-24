# -*- coding:utf-8 -*-
# @time     :2019/5/2822:25
# @Author   :xiaowang
# @File     :lemon_def_requests_0527.py

import json
import suds
from suds.client import Client

from scripts.handle_log import do_log


class HandleWebservice:
    """
    封装一个请求的类。对应各种请求，进行处理。
    """
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
            # res = {"fail_code": "fail"}
        return res


if __name__ == '__main__':
    str1 = {"client_ip": "192.168.3.1", "tmpl_id": "2", "mobile": "18322221234"}
    str2 = '{"status": 0, "code": "20118", "data": null, "msg": "请输入数字"}'
    do_client = HandleWebservice()
    actual = do_client(method="sendMCode", data=str1)
    print(actual)
    print(type(actual))

    # print(json.loads(str))
    # print(json.loads(str)["data"])





