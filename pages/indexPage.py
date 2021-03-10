#! /usr/bin/python
#coding:utf-8
from pages.basePage import Page
from selenium.webdriver.common.by import By
import time
import os

class IndexPage(Page):


    def __init__(self,driver):
        Page.__init__(self,driver)


    def dir_click(self,text):
        self.cover_is_display()
        # dir_ele = (By.LINK_TEXT,text)
        dir_ele = (By.XPATH,'//li[@title="'+text+'"]/a')
        dir_ul_ele = (By.XPATH,'//li[@title="'+text+'"]/ul')
        #判断文件夹是否打开
        if self.is_display(dir_ul_ele) == False:      
            self.move_to_element_click(dir_ele)
    def menu_click(self,text):
        #点击菜单
        # menu_ele = (By.LINK_TEXT,text)  
        # self.move_to_element_click(menu_ele)

        menu_ele = (By.XPATH,'//li[@title="'+text+'"]/a')
        print('ele:'+menu_ele[1])
        self.click(menu_ele)
        self.cover_is_display()

    def switch_to_frame(self,text):
        iframe = (By.XPATH,'//div[@title="'+text+'"]/iframe')
        #切换frame
        self.switch_frame(iframe)

    cover = (By.XPATH,'//body/div[@class="zMsg_cover cover_body"]')
    def cover_is_display(self):
        i = 0 
        while self.is_display(self.cover) == True and i < 30 :
            i = i + 1 
            time.sleep(3)

    # #自助分析
    # selfFilter = (By.LINK_TEXT,'自助分析')
    # selfFilter_ul = (By.XPATH,'//li[@title="自助分析"]/ul')
    # def selfFilter_click(self):
    #     #点击自助分析菜单
    #     if self.is_display(self.selfFilter_ul) == False:
    #         self.click(self.selfFilter)

    # labelLib = (By.LINK_TEXT,'标签库')
    # def labelLib_click(self):
    #     #点击标签库菜单
    #     self.click(self.labelLib)
    #     #切换iframe
    #     label_iframe = (By.XPATH,'//div[@title="标签库"]/iframe')
    #     self.switch_frame(label_iframe)


    # analysisGrap = (By.LINK_TEXT,'分析图表')
    # def analysisGrap_click(self):
    #     #点击分析图表菜单
    #     self.click(self.analysisGrap)

    # #清单推送
    # listPush = (By.LINK_TEXT,'清单推送')
    # listPush_ul = (By.XPATH,'//li[@title="清单推送"]/ul')
    # def listPush_click(self):
    #     #点击清单推送菜单
    #     if self.is_display(self.listPush_ul) == False:
    #         self.click(self.listPush)

    # listV2 = (By.LINK_TEXT,'清单v2')
    # listV2_ul = (By.XPATH,'//li[@title="清单v2"]/ul')
    # def listv2_click(self):
    #     #点击清单V2菜单
    #     if self.is_display(self.listV2_ul) == False:
    #         self.click(self.listV2)

    # listBuild = (By.LINK_TEXT,'清单发布')
    # def listBuild_click(self):
    #     #清单发布
    #     self.click(self.listBuild)
    #     #切换iframe
    #     listBuild_frame_ele = (By.XPATH,'//div[@title="清单发布"]/iframe')
    #     self.switch_label_frame(listBuild_frame_ele)

    def switch_parent_frame(self):
        self.switch_to_parent_frame()