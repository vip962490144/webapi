# -*- coding: utf-8 -*-

from datetime import datetime
import os
import unittest

from libs import HTMLTestRunnerNew
from scripts.handle_config import do_config
from scripts.constants import CASES_DIR, REPORTS_DIR, CONFIG_USER_FILE_PATH
from scripts.handle_user import genrate_users_config

if not os.path.exists(CONFIG_USER_FILE_PATH):
    genrate_users_config()

data_discover = unittest.defaultTestLoader.discover(CASES_DIR, pattern="test_web_*.py")

report_html_name = os.path.join(REPORTS_DIR, do_config("file path", "report_html_name"))
report_html_name_full = report_html_name + "_" + datetime.strftime(datetime.now(), "%Y%m%d%H%M%S") + ".html"
with open(report_html_name_full, mode='wb') as save_to_file:
    one_runner = HTMLTestRunnerNew.HTMLTestRunner(stream=save_to_file,
                                                  title=do_config("report", "title"),
                                                  verbosity=do_config("report", "verbosity"),
                                                  description=do_config("report", "description"),
                                                  tester=do_config("report", "tester"))
    one_runner.run(data_discover)

if __name__ == '__main__':
    unittest.main()
