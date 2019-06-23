#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os


# __file__固定变量
# 获取项目根目录路径。
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取测试用例cases的所在目录的路径
CASES_DIR = os.path.join(BASE_DIR, 'cases')

# 获取测试数据datas的所在目录的路径
DATAS_DIR = os.path.join(BASE_DIR, 'datas')

# 获取配置文件config的所在目录的路径
CONFIGS_DIR = os.path.join(BASE_DIR, 'configs')

# 获取日志文件logs的所在目录的路径
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# 获取报告文件reports的所在目录的路径
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# 获取配置文件的路径
CONFIG_FILE_PATH = os.path.join(CONFIGS_DIR, "config.conf")

CONFIG_USER_FILE_PATH = os.path.join(CONFIGS_DIR, "user_message.conf")

# 获取cases文件的路径
TEST_DATAS_FILE_PATH = os.path.join(DATAS_DIR, "cases.xlsx")








