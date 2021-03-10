#! /usr/bin/python
#coding = utf-8

from pages.basePage import Page
from selenium.webdriver.common.by import By
import time
import math


class PolicyCreatePage(Page):
   
    #选择策略
    def policy_click(self,policyName):
        policy_ele = (By.XPATH,'//a[@title="'+policyName+'"]')
        policy_id = self.find_element_attr(policy_ele,'id')
        policy_check_id = policy_id[0][0:-1]+'check'
        self.move_to_element_click((By.ID,policy_check_id))
        self.cover_is_display()

    #点击场景设置口径
    policy_selected_str = '//div[@class="section-body"]/table/tbody/tr[@class="color2"]'
    dialog_labelCode = (By.ID,'dialog_labelCode')
    def policy_label_click(self,policyName):
        policy_selecteds = self.get_eles_text((By.XPATH,self.policy_selected_str+'/td[1]'))
        i = 0 
        scene_id = ''
        for policy_selected in policy_selecteds:
            i = i + 1
            if policyName == policy_selected:
                caliber_i = (By.XPATH,self.policy_selected_str+'['+str(i)+']/td[2]/i')
                onclick_str = self.find_element_attr(caliber_i,'onclick')[0]
                scene_id = onclick_str.split(',')[1].split("\"")[1]
                self.move_to_element_click(caliber_i)
                if self.is_display(self.dialog_labelCode) == False:
                    time.sleep(2)
                break
        return scene_id


    def input_max_val(self,policyName,maxVal):
        policy_selecteds = self.get_eles_text((By.XPATH,self.policy_selected_str+'/td[1]'))
        i = 0 
        for policy_selected in policy_selecteds:
            i = i + 1
            if policyName == policy_selected:
                input_val_ele = (By.XPATH,self.policy_selected_str+'['+str(i)+']/td[3]/input')
                val = self.find_element_attr(input_val_ele,'data-print')
                if val != maxVal:
                    self.clear(input_val_ele)
                    self.send_keys(input_val_ele,maxVal)
                    self.move_to_element_click((By.XPATH,self.policy_selected_str+'['+str(i)+']/td[1]'))
                    self.cover_is_display()
                

    label_filter_table = (By.XPATH,'//*[@id="labelFilterTable"]/tr')
    def delete_label_caliber(self):

        if self.find_elements((By.ID,'labelFilterTable'))[0].text != '':
            table_eles = self.find_elements(self.label_filter_table)
            i = 0
            for tabel in table_eles:
                i = i + 1
                delete_ele = (By.XPATH,'//*[@id="labelFilterTable"]/tr['+str(i)+']/td[5]/input[1]')
                self.move_to_element_click(delete_ele)
                if self.alert_is_exist == False:
                    time.sleep(2)
                else:
                    tip = self.alert_tip()
                    if '移除' in tip:
                        self.alert_btn_sure_click()
                    i = i-1
            

    saveLabelBtn = (By.ID,'saveLabelBtn')
    def save_caliber(self):
        self.move_to_element_click(self.saveLabelBtn)
        if self.alert_body_is_exist == False:
            time.sleep(2)
        else:
            tip = self.alert_tip()
            if '保存' in tip:
                self.alert_btn_sure_click()
                self.cover_is_display()
                if self.alert_body_is_exist == False:
                    time.sleep(2)
                else:
                    tip = self.alert_tip()
                    if '操作成功' in tip:
                        self.alert_btn_sure_click()

    #人员调整
    sceneAdjust = (By.XPATH,'//span[@class="icon-sceneAdjust"]')
    mathCeil = (By.ID,'mathCeil')
    def scene_adjust(self):
        self.move_to_element_click(self.sceneAdjust)
        while self.is_display(self.mathCeil) == True:
            time.sleep(2)


    def set_num(self,sceneId,marketNum,adjustNum,maxVal):
        class_name = 'target_customers_input input_scene_'+sceneId
        maxVal = float(maxVal)

        marketNum_show = self.get_eles_text((By.XPATH,'//tr[@class="main_tr color2 sceneid_'+sceneId+'"]/td[3]/ul/li/span'))
        market = float(marketNum_show[0])
        # with allure.step('dddddddddddddddd'):
        if market != 0 :
            if marketNum != 0 :
                if '%' in marketNum :
                    pencent = float(marketNum.split('%')[0])/100
                    marketNum = math.floor(market*pencent)
                    if marketNum > maxVal:
                        marketNum = maxVal  
                    if marketNum < 1:
                        marketNum = 1
                self.clear((By.XPATH,'//input[@class="'+class_name+'"][@data-type="first"]'))
                self.send_keys((By.XPATH,'//input[@class="'+class_name+'"][@data-type="first"]'),marketNum)
                self.move_to_element_click((By.XPATH,'//*[@id="sceneList"]/tbody/tr[@class="table_title"]/td[3]'))
        if adjustNum != 0 :
            adjustNum_show = self.get_eles_text((By.XPATH,'//tr[@class="main_tr color2 sceneid_'+sceneId+'"]/td[3]/ul/li/span'))
            adjust = float(adjustNum_show[1])
            if adjust != 0:
                if '%' in adjustNum:
                    pencent = float(adjustNum.split('%')[0])/100
                    adjustNum = math.floor(adjust*pencent)
                if marketNum + adjustNum > maxVal:
                    adjustNum = maxVal - marketNum
                if adjustNum < 1:
                        adjustNum = 1
                self.send_keys((By.XPATH,'//input[@class="'+class_name+'"][@data-type="other"]'),adjustNum)
                self.move_to_element_click((By.XPATH,'//*[@id="sceneList"]/tbody/tr[@class="table_title"]/td[3]'))


    def change_strategy_cnt(self,sceneId):
        self.move_to_element_click((By.XPATH,'//tr[@class="main_tr color2 sceneid_'+sceneId+'"]/td[4]/span[2]'))
        self.cover_is_display()
        while self.is_display(self.mathCeil) == True:
            time.sleep(2)

    delete_strategy_ele = (By.XPATH,'//table[@id="ruleTable"]/tbody/tr/td[4]/a[1]')
    def delete_strategy(self):
        if len(self.find_elements((By.XPATH,'//table[@id="ruleTable"]/tbody/tr/td[4]')))>1:
            dels = self.find_elements(self.delete_strategy_ele)
            for d in dels:
                d.click()
                if self.alert_body_is_exist() == False:
                    time.sleep(2)
                else:
                    if '移除' in self.alert_tip():
                        self.cover_is_display()
                        self.alert_btn_sure_click()
                        if self.alert_body_is_exist() == False:
                            time.sleep(2)
                        else:
                            if '删除成功' in self.alert_tip():
                                self.alert_btn_sure_click()
                                time.sleep(0.5)


    showRuleBtn = (By.ID,'showRuleBtn')
    def add_strategy(self):
        self.move_to_element_click(self.showRuleBtn)
            
    product_type = (By.ID,'productTypeList')
    def product_type_click(self,product_type):
        self.select_by_text(self.product_type,product_type)
        self.cover_is_display()

    product_list = (By.ID,'productList')
    def product_click(self,product):
        self.select_by_text(self.product_list,product)

    addRuleBtn = (By.ID,'addRuleBtn')
    def save_strategy(self):
        self.move_to_element_click(self.addRuleBtn)
        self.cover_is_display()

    checkRuleBtn = (By.ID,'checkRuleBtn')
    close_strategy_justify = (By.ID,'close_strategy_justify')
    def check_strategy(self):
        self.move_to_element_click(self.checkRuleBtn)
        self.cover_is_display()
        if self.alert_body_is_exist() == False:
            time.sleep(2)
        else:
            if '匹配成功' in self.alert_tip():
                self.alert_btn_sure_click()
                self.cover_is_display()
                self.move_to_element_click(self.close_strategy_justify)
                time.sleep(0.4)

    strategy_preview = (By.XPATH,'//div[@class="panel_wraper strategy_preview"]')
    def preview(self):
        self.move_to_element_click((By.LINK_TEXT,'收入预测'))
        if self.is_display(self.strategy_preview) == False:
            time.sleep(2)

    execCalculateBtn = (By.ID,'execCalculateBtn')
    close_btn = (By.XPATH,'//div[@class="panel_wraper strategy_preview"]/div/h2/i[@class="close_btn"]')
    def preview_calculate(self):
        self.move_to_element_click(self.execCalculateBtn)
        self.cover_is_display()
        self.move_to_element_click(self.close_btn)
        time.sleep(0.5)

    def save_person(self):
        self.move_to_element_click((By.LINK_TEXT,'生成清单'))
        if self.alert_body_is_exist() == False:
            time.sleep(2)
        else:
            if '确认生成清单' in self.alert_tip():
                self.alert_btn_sure_click()
                self.cover_is_display()
                self.alert_body_is_exist()


    lists = (By.XPATH,'//table[@id="sceneList"]/tbody/tr[@class="main_tr color3"]')
    def get_result(self,sceneName):
        texts = self.get_eles_text(self.lists)
        result = ''
        for text in texts:
            if sceneName in text:
                result = text
        return result
    #==================================手动场景=====================================     
    manual_button_ele = (By.XPATH,'//div[@class="section-title clear-fixed-after"]/i[2]')
    def manual_scene_click(self):
        self.move_to_element_click(self.manual_button_ele)
        self.cover_is_display()


    user_group_str = '//div[@id="selectUserGroupTab"]/button'     
    def select_user_group(self,groupType):
        dataVal = ''
        if '场景' in groupType :
            dataVal = 'SCENE'
        elif '已传' in groupType:
            dataVal = 'UPLOAD'
        elif '已存' in groupType:
            dataVal = 'LABEL'     

        self.move_to_element_click((By.XPATH,self.user_group_str+'[@data-val="'+dataVal+'"]'))
        self.cover_is_display()


    def select_group_name(self,groupType,groupName):
        id = ''
        if '场景' in groupType :
            id = 'groupSceneUserTab'
        elif '已传' in groupType:
            id = 'groupImportUserTab'
        elif '已存' in groupType:
            id = 'groupUserTab'
        groups_ele = (By.XPATH,'//tbody[@id="'+id+'"]/tr/td[2]')
        groupsNames = self.get_eles_text(groups_ele)
        i = 0
        result = False
        for groups in groupsNames:
            i = i + 1
            if groupName == groups:
                self.move_to_element_click((By.XPATH,'//tbody[@id="'+id+'"]/tr['+str(i)+']/td[1]'))
                result = True
                break
        return result


    def delete_group_name(self,groupType,groupName):
        id = ''
        if '场景' in groupType :
            id = 'groupSceneUserTab'
        elif '已传' in groupType:
            id = 'groupImportUserTab'
        elif '已存' in groupType:
            id = 'groupUserTab'
        groups_ele = (By.XPATH,'//tbody[@id="'+id+'"]/tr/td[2]')
        groupsNames = self.get_eles_text(groups_ele)
        i = 0
        for groups in groupsNames:
            i = i + 1
            if groupName == groups:
                self.move_to_element_click((By.XPATH,'//tbody[@id="'+id+'"]/tr['+str(i)+']/td[5]/input'))
                if self.alert_body_is_exist() == False:
                    time.sleep(2)
                else:
                    if '移除' in self.alert_tip():
                        self.alert_btn_sure_click()
                        self.alert_body_is_exist()
                        self.cover_is_display()
                        if self.alert_body_is_exist() == False:
                            time.sleep(2)
                        else:
                            if '删除成功' in self.alert_tip():
                                self.alert_btn_sure_click()
                                self.alert_body_is_exist()
                



    #用户分配/产品匹配
    product_ass = (By.XPATH,'//span[@class="icon-product"]')
    def product_assignment(self):
        self.move_to_element_click(self.product_ass)
        self.cover_is_display()

    #用户选择
    person_sel = (By.XPATH,'//span[@class="icon-person-image"]')
    def person_select(self):
        self.move_to_element_click(self.person_sel)
        self.cover_is_display()

        


    #-----------弹框提示----------
    alert = (By.CLASS_NAME,'zMsg_alert_new')
    sub = (By.XPATH,'//div[@class="zMsg_alert_new"]/table/tfoot/tr/td/button')
    def alert_btn_click(self):
        if True == self.is_exist(self.alert):
            self.click(self.sub)
    sub_sure = (By.XPATH,'//div[@class="zMsg_alert_new"]/table/tfoot/tr/td/button[@class="btn btn-normal"]')
    def alert_btn_sure_click(self):
        if True == self.is_exist(self.alert):
            self.click(self.sub_sure)

    def alert_tip(self):
        if True == self.is_exist(self.alert):
            return self.find_element_attr(self.alert,'data-text')[0]

    def alert_is_exist(self):
        return self.is_exist_no_wait(self.alert)

    alert_body_cover = (By.ID,'body_cover')
    def alert_body_is_exist(self):
        return self.is_exist(self.alert_body_cover)    

    label_source_id = (By.ID,'labelSourceId')           
    def get_source_id(self):
        return self.find_element_value(self.label_source_id)


















    cover = (By.XPATH,'//body/div[@class="zMsg_cover cover_body"]')
    def cover_is_display(self):
        i = 0 
        while self.is_display(self.cover) == True and i < 30 :
            i = i + 1 
            time.sleep(3)