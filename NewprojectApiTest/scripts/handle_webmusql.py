#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
import random

from scripts.handle_config import do_config


class HandleWebMysql:
    """
    数据库处理类
    """

    def __init__(self):
        # 创建连接
        self.connect_one = pymysql.connect(host=do_config("web mysql", "host"),
                                           user=do_config("web mysql", "user"),
                                           password=do_config("web mysql", "password"),
                                           # db=do_config("web mysql", "db"),
                                           port=do_config("web mysql", "port"),
                                           charset=do_config("web mysql", "charset"),
                                           cursorclass=pymysql.cursors.DictCursor)
        # 创建游标
        self.cursor = self.connect_one.cursor()

    @staticmethod
    def create_moblie():
        """
        随机生成11位手机号。
        :return:
        """
        start_mobile = ('139', '138', '137', '136', '135', '134', '159', '158', '157', '152', '151', '150', '188',
                        '187', '130', '131', '132', '155', '156', '186', '185', '133', '153', '189', '180')
        start_num = random.choice(start_mobile)
        one_str = "0123456789"
        end_num = "".join(random.sample(one_str, 8))
        return start_num + end_num

    def is_existed_mobile(self, db_table, mobile):
        """
        判断给定的手机号在数据库中是否存在
        :param mobile:待判断的手机号，为字符串类型
        :return: True or False
        """
        sql = "SELECT * FROM {} WHERE Fmobile_no = {}".format(db_table, mobile)
        if self(sql):
            return True
        else:
            return False

    def create_not_mobile(self):
        """
        判断手机号是否存在，无限循环，直到取出一个不存在的手机号。
        :return:
        """
        while True:
            one_mobile = self.create_moblie()
            db = do_config("web api", "db") + one_mobile[-2:]
            table = do_config("web api", "table") + one_mobile[8]
            db_table = db + "." + table
            if not self.is_existed_mobile(db_table, one_mobile):
                break

        return one_mobile

    def __call__(self, sql, arg=None, is_more=False):
        """
        获取值
        :param sql:sql查询语句。
        :param arg:参数，只能是序列类型。可以带入%s（占位符）处。
        :param is_more: 判读获取多个值还是一个值，默认False获取一个值
        :return:
        """
        self.cursor.execute(sql, arg)
        self.connect_one.commit()

        if is_more:
            result = self.cursor.fetchall()
        else:
            result = self.cursor.fetchone()

        return result

    @staticmethod
    def create_user_id():
        start_helder = "小王"
        one_str = "0123456789"
        num = "".join(random.sample(one_str, 9))
        return start_helder + num

    def is_existed_user_id(self, user_id):
        """
        判断给定的user_id号在数据库中是否存在
        :param user_id:待判断的id号，为字符串类型
        :return: True or False
        """
        sql = "SELECT * FROM user_db.t_user_info WHERE Fuser_id = %s"
        if self(sql, arg=(user_id, )):
            return True
        else:
            return False

    def create_not_user_id(self):
        while True:
            user_id = self.create_user_id()
            if not self.is_existed_user_id(user_id):
                break

        return user_id

    def is_existed_captcha(self, db_table, mobile):
        """
        判断手机号存在，则返回该用户的用户验证码
        :param mobile:
        :return:
        """
        sql = "SELECT * FROM {} WHERE Fmobile_no = {}".format(db_table, mobile)
        return self(sql)

    def existed_fuser_id(self):
        sql = "SELECT * FROM user_db.t_user_info WHERE `Fip` = '1.1.1.1' AND `Fauth_id` IS NULL"
        return self(sql)['Fuid']

    def close(self):
        """
        关闭游标，关闭连接
        :return:
        """
        self.cursor.close()
        self.connect_one.close()


if __name__ == '__main__':

    do_mysql = HandleWebMysql()
    sql = "SELECT * FROM user_db.t_user_info WHERE (Fip = '1.1.1.1' AND Fauth_id IS NULL)"
    #
    # db = do_config("web api", "db") + "34"
    # table = do_config("web api", "table") + '7'
    # db_table1 = db + '.' + table
    # mobile1 = '13078423734'
    # res = do_mysql.is_existed_captcha(db_table1, mobile1)
    # res = do_mysql(sql, arg=(db_table, mobile,))['Fverify_code']
    res = do_mysql.existed_fuser_id()
    # res = do_mysql.is_existed_fuser_id(16024979)
    # res = do_mysql(sql)
    print(res)
    do_mysql.close()
    # print(mobile1[9:])
