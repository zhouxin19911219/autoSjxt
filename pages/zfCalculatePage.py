#! /usr/bin/python
#coding:utf-8

from pages.basePage import Page
from selenium.webdriver.common.by import By
import time
class ZfCalculatePage(Page):

    source_id = (By.ID,'labelSourceId')
    def get_source_id(self):
        return self.find_element_attr(self.source_id,'value')[0]

    #点击已传
    uploaded_user = (By.ID,'haveUploadUser')
    uploaded_sure_click = (By.ID,'selectGroupBtn')
    def uploaded_user_click(self,name):
        self.move_to_element_click(self.uploaded_user)
        self.cover_is_display()
        uploaded = '//*[@id="groupUserTab"]/tr'
        self.user_check(uploaded,name)
        
        self.move_to_element_click(self.uploaded_sure_click)
        self.cover_is_display()


    #点击已存
    saved_user = (By.ID,'labelUser')
    saved_sure_click = (By.ID,'selectSaveGroupBtn') 
    # dialog_savegroupUsers = (By.XPATH,'//div[@id="dialog_savegroupUsers"]')  
    def saved_user_click(self,name):
        self.move_to_element_click(self.saved_user)
        # if self.is_display_no_wait(self.dialog_savegroupUsers) == False:
        #     time.sleep(2)
        self.cover_is_display()
        saved = '//*[@id="saveGroupUserTab"]/tr'
        self.user_check(saved,name)
        self.move_to_element_click(self.saved_sure_click)
        self.cover_is_display()

      
    def user_check(self,user_ele,name):
        eles = self.find_elements((By.XPATH,user_ele))
        for i in range(0,len(eles)):
            if name in eles[i].text:
                e = user_ele+'['+str(i+1)+']/td[1]/input'
                self.move_to_element_click((By.XPATH,e))
                break

    #======================================添加规则===========================================


    #点击添加规则
    add_rule_btn = (By.ID,'addRuleBtn')
    dialog_labelCode = (By.ID,'dialog_labelCode')
    def add_rule_click(self):
        self.move_to_element_click(self.add_rule_btn)
        if self.is_display_no_wait(self.dialog_labelCode) == False:
            time.sleep(2)

    label_sure_btn = (By.ID,'saveLabelBtn')
    def label_sure_click(self):
        self.move_to_element_click(self.label_sure_btn)
        self.cover_is_display()

    product_type = (By.ID,'productType')
    def product_type_click(self,product_type):
        self.select_by_text(self.product_type,product_type)

    product_list = (By.ID,'productList')
    def product_click(self,product):
        self.select_by_text(self.product_list,product)
        self.cover_is_display()

    calculate = (By.ID,'forecastResult')
    def calculate_click(self):
        self.move_to_element_click(self.calculate)
        self.cover_is_display()

    
    calculate_result = (By.XPATH,'//table[@class="new_table"]/tbody/tr[2]')
    def get_calculate_result(self):
        ele = self.find_elements(self.calculate_result)
        return ele[0].text


    def calculate_result_click(self):
        self.move_to_element_click(self.calculate_result)

    
    #-----------弹框提示----------
    body_cover = (By.ID,'body_cover')
    alert = (By.CLASS_NAME,'zMsg_alert_new')
    sub = (By.XPATH,'//div[@class="zMsg_alert_new"]/table/tfoot/tr/td/button')
    def alert_btn_click(self):
        if True == self.is_exist(self.alert):
            self.click(self.sub)

    
    def alert_sure_btn_click(self,text):
        sure_sub = (By.XPATH,'//div[@class="zMsg_alert_new"]/table/tfoot/tr/td/button')
        if True == self.is_exist(self.alert):
            eles = self.find_elements(sure_sub)
            for ele in eles:
                if text in ele.text:
                    ele.click()

    def alert_tip(self):
        tip = ''
        
        if self.is_exist_no_wait(self.body_cover) and self.is_display_no_wait(self.body_cover) :
            tip = self.find_element_attr(self.alert,'data-text')[0]
        return tip
    #====================================================


    cover = (By.XPATH,'//body/div[@class="zMsg_cover cover_body"]')
    def cover_is_display(self):
        i = 0 
        while self.is_display(self.cover) == True and i < 30 :
            i = i + 1 
            time.sleep(3)
    
    