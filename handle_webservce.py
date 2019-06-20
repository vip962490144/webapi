#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
from scripts.constants import CONFIG_FILE_PATH
from scripts.handle_config import HandleConfig
from scripts.handle_log import do_log
from suds.client import Client


do_config = HandleConfig(CONFIG_FILE_PATH)


class HandleWebservice:
    """
    封装一个请求的类。对应各种请求，进行处理。
    """
    def __init__(self, url):
        self.client = Client(url)

    def get_sendmcode(self, data):
        resquetst = self.client.service.sendMCode(data)
        return resquetst

    def get_sendsm(self, data):
        resquetst = self.client.service.sendSM(data)
        return resquetst

    def get_verifymcode(self, data):
        resquetst = self.client.service.verifyMCode(data)
        return resquetst

    def __call__(self, method, data):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception as e:
                do_log.error("将json转换为python时，出现异常：{}".format(e))
                data = eval(data)

        if method == "sendMCode":
            res = self.get_sendmcode(data=data)
        elif method == "sendSM":
            res = self.get_sendsm(data=data)
        elif method == "verifyMCode":
            res = self.get_verifymcode(data=data)
        else:
            res = None
            do_log.error("不支持{}请求方法".format(method))

        return res


if __name__ == '__main__':
    # client = Client("")
    client = HandleWebservice(do_config("web api", "url") + "/sms-service-war-1.0/ws/smsFacade.ws?wsdl")
    # print(client)
    params1 = '{"client_ip": "192.168.3.1", "tmpl_id": "1", "mobile": "18355551234"}'
    params = json.loads(params1)
    mobile = params["mobile"]
    expected = '{"retCode": "0"}'
    expected_code = json.loads(expected)["retCode"]
    print(expected_code)
    resquests = client("sendMCode", params)
    print(mobile)
    print(resquests["retCode"])
    # print(client(url=), data)
    pass

