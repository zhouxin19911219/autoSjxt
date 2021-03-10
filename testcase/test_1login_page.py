# #! /usr/bin/python
# # coding:utf-8
# import allure
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import pytest
# import time
# import sys
# sys.path.append('.')
# from pages.loginPage import LoginPage
# from common import param

# @allure.feature('登录测试')
# class Test_login_Page:

#     def setup_method(self,method):

#         self.driver = webdriver.Chrome()
#         self.url = param.url
#         self.assert_title = '大数据对内运营支撑系统（测试）'

#     def teardown_method(self,method):
#         self.driver.quit()

#     @allure.story('登录成功')
#     def test_login_success(self):
#         print ('-------admin登录成功----------')

#         usr = param.usr_suc
#         pwd = param.pwd_suc

#         driver = self.driver

#         login_Page = LoginPage(driver)

#         login_Page.open_login_page(self.url)

#         login_Page.click_login_btn(usr , pwd)

#         time.sleep(2)

#         login_Page.click_repeat_user_exit_btn()

#         time.sleep(2)

#         assert login_Page.get_title() == self.assert_title

#     @allure.story('登录密码错误')
#     def test_login_fail(self):
#         print ('-------admin登录失败----------')
#         usr = param.usr_err
#         pwd = param.pwd_err
#         error_msg = '密码错误'

#         driver = self.driver

#         login_Page = LoginPage(driver)

#         login_Page.open_login_page(self.url)

#         login_Page.click_login_btn(usr , pwd)

#         time.sleep(2)

#         assert error_msg in login_Page.get_error_msg()




# # if __name__ == '__main__':
# #     pytest.main(['-s','test_login_page.py'])