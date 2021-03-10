

import pytest
from allure_pytest import plugin as allure_plugin
# import pytest_repeat as repeat
import os
import shutil




if __name__ == '__main__':
    if os.path.exists('./report')==True:
        shutil.rmtree('./report')

    pytest.main(['-s','--alluredir=report'])
    args = ['-s', '--alluredir=report', os.path.abspath('.')+'/testcase/']
    pytest.main(args=args, plugins=[allure_plugin])
    pytest.main('./testcase')

    # 生成exe后会提示pytest不是内部命令也不是外部命令
    # os.system('pytest testcase/ --alluredir report')
    # os.system('allure generate report -o report/html --clean')


    #可以运行但是只跑一次，遇到问题不会重新跑
    # pytest.main(['-s','--alluredir=report'])
    # args = ['-s', '-v', '--count=1', '--alluredir=report', os.path.abspath('.')+'/testcase/']
    # pytest.main(args=args, plugins=[allure_plugin, repeat])
    # pytest.main('./testcase/')






