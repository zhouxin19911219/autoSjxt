#! /usr/bin/python
#coding:utf-8
import sys
sys.path.append('.')
from pages.basePage import Page
from selenium.webdriver.common.by import By
from testcase.test_report_design_page import Test_reportDesign_Page
from common import param
import time


class LoginPage(Page):

    login_usr = (By.ID, 'username')
    login_pwd = (By.ID, 'password')
    login_btn = (By.ID,'submitBtn')
    repeat_user_exit_alert = (By.CLASS_NAME,'zMsg_alert_new')
    repeat_user_exit_btn = (By.ID , 'confirm')
    error_msg = (By.CLASS_NAME, 'error_txt')
    details_button_btn = (By.ID, 'details-button')
    proceed_link_button_btn = (By.ID, 'proceed-link')

    def __init__(self,driver):
        Page.__init__(self,driver)

    def open_login_page(self,url):
        #'-------打开登录页面----------'
        self.driver.get(url)
        self.driver.maximize_window()


    def click_login_btn(self , usr , pwd ):
       #'-------模拟登录----------'
        self.send_keys(self.login_usr , usr)
        self.send_keys(self.login_pwd , pwd)
        self.click(self.login_btn)

    def click_details_button_btn(self):
        #'---------点击高级确定按钮------'
        if True == self.is_exist_no_wait(self.details_button_btn) :
            self.not_wait_click(self.details_button_btn)

    def click_proceed_link_button_btn(self):
        #'---------点击继续链接------'
        if True == self.is_exist_no_wait(self.proceed_link_button_btn) :
            self.not_wait_click(self.proceed_link_button_btn)

    def click_repeat_user_exit_btn(self):
        #'---------点击踢出重复登录确定按钮------'
        if True == self.is_exist_no_wait(self.repeat_user_exit_alert) :
            self.click(self.repeat_user_exit_btn)

    def get_title(self):
        return self.driver.title

    def get_error_msg(self):
        return self.get_text(self.error_msg)



    # def get_staff_no(self):
    #     sql = '''select grade_value from sys_staff_grade_rel where staff_no = %s ''',param.staff_no

    #     datasource = 'sysMySQL'
    #     test_reportDesign_Page = Test_reportDesign_Page()
    #     result = test_reportDesign_Page.sql_search_pubulic(self.driver,datasource,sql)
    #     return result
