#! /usr/bin/python
# coding=utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from common import param
from pages.loginPage import LoginPage
from pages.indexPage import IndexPage
import time
import pytest
import allure
import os
import sys

@allure.step('登录')
@pytest.fixture(scope='session',autouse=True)
def login(): 
    global driver
    if param.config['is_show'] == False:
        with allure.step('无浏览器模式：'):
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1300,1000")
            driver = webdriver.Chrome(chrome_options=chrome_options)
    else:
        with allure.step('chrome浏览器打开：'):
            driver = webdriver.Chrome()


    url = param.url
    login_Page = LoginPage(driver)

    driver.implicitly_wait(5)
    login_Page.open_login_page(url)
    login_Page.click_details_button_btn()
    login_Page.click_proceed_link_button_btn()
    with allure.step('用户名：{}，密码：{}'.format(param.usr,param.pwd)):
        usr = param.usr
        pwd = param.pwd
        login_Page.click_login_btn(usr , pwd)

    time.sleep(2)

    login_Page.click_repeat_user_exit_btn()


@allure.step('点击标签库')
@pytest.fixture
def label_lib(login):
    index_Page = IndexPage(driver)
    for dir in param.label_lib['file_dir']:
        time.sleep(0.5)
        index_Page.dir_click(dir)
        time.sleep(0.5)
    index_Page.menu_click(param.label_lib['menu'])
    index_Page.switch_to_frame(param.label_lib['menu'])
    return driver

@allure.step('点击自助报表')
@pytest.fixture
def auto_analy(login):
    index_Page = IndexPage(driver)
    for dir in param.auto_analy['file_dir']:
        index_Page.dir_click(dir)
        time.sleep(0.5)
    index_Page.menu_click(param.auto_analy['menu'])
    index_Page.switch_to_frame(param.auto_analy['menu'])
    return driver

@allure.step('点击清单发布')
@pytest.fixture
def list_build(login):
    # print ('----------清单发布-----------')
    index_Page = IndexPage(driver)
    for dir in param.list_build['file_dir']:
        index_Page.dir_click(dir)
        time.sleep(0.5)
    index_Page.menu_click(param.list_build['menu'])
    index_Page.switch_to_frame(param.list_build['menu'])
    return driver

@allure.step('点击清单下载')
@pytest.fixture
def list_download(login):
    # print ('----------清单下载-----------')
    index_Page = IndexPage(driver)
    for dir in param.list_download['file_dir']:
        index_Page.dir_click(dir)
        time.sleep(0.5)
    index_Page.menu_click(param.list_download['menu'])
    index_Page.switch_to_frame(param.list_download['menu'])
    return driver

@allure.step('点击清单查询')
@pytest.fixture
def list_search(login):
    # print ('----------清单查询-----------')
    index_Page = IndexPage(driver)
    for dir in param.list_search['file_dir']:
        index_Page.dir_click(dir)
        time.sleep(0.5)
    index_Page.menu_click(param.list_search['menu'])
    index_Page.switch_to_frame(param.list_search['menu'])
    return driver
    

@allure.step('点击资费测算')
@pytest.fixture
def zf_calculate(login):
    # print ('----------资费测算-----------')
    index_Page = IndexPage(driver)
    for dir in param.zf_calculate['file_dir']:
        index_Page.dir_click(dir)
        time.sleep(0.5)
    index_Page.menu_click(param.zf_calculate['menu'])
    index_Page.switch_to_frame(param.zf_calculate['menu'])
    return driver

@allure.step('点击策略创建')
@pytest.fixture
def policy_create(login):
    # print ('----------策略创建-----------')
    index_Page = IndexPage(driver)
    for dir in param.policy_create['file_dir']:
        index_Page.dir_click(dir)
        time.sleep(0.5)
    index_Page.menu_click(param.policy_create['menu'])
    index_Page.switch_to_frame(param.policy_create['menu'])
    return driver

@allure.step('点击SQL查询')
@pytest.fixture
def sql_search(login):
    # print ('----------sql查询-----------')
    index_Page = IndexPage(driver)
    for dir in param.sql_search['file_dir']:
        index_Page.dir_click(dir)
        time.sleep(0.5)
    index_Page.menu_click(param.sql_search['menu'])
    index_Page.switch_to_frame(param.sql_search['menu'])
    return driver

@allure.step('点击报表设计器')
@pytest.fixture
def report_design(login):
    index_Page = IndexPage(driver)
    for dir in param.report_design['file_dir']:
        index_Page.dir_click(dir)
        time.sleep(0.5)
    index_Page.menu_click(param.report_design['menu'])
    index_Page.switch_to_frame(param.report_design['menu'])
    return driver

@pytest.fixture
def to_parent_frame():
    yield
    # print ('----------返回父级frame-----------')
    index_Page = IndexPage(driver)
    index_Page.switch_parent_frame()

        
@allure.step('退出浏览器')
@pytest.fixture(scope='session',autouse=True)
def login_out():
    yield
    driver.quit()



