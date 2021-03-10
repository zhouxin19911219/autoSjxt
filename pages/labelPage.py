#! /usr/bin/python
#coding:utf-8

from pages.basePage import Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
sys.path.append('.')
from common import param
import datetime
import os


class LabelPage(Page):


    month_labSourceId = (By.ID,'labSourceId_month')
    day_labSourceId = (By.ID, 'labSourceId_day')
    #===================================更改日月标签库===============================
    #更改日月标签库
    def label_data_type(self,text):
        if '日' == text:
            ele = (By.XPATH,'//div[@id="data_type"]/button[@id="day"]')
            self.ele_is_exist(ele)
            self.move_to_element_click(ele)
        elif '月' == text:
            ele = (By.XPATH,'//div[@id="data_type"]/button[@id="month"]')
            self.ele_is_exist(ele)
            self.move_to_element_click(ele)
    #===================================更改日月标签库===============================


    #===================================更改月数据源===============================
    #更改数据源
    source_month = (By.ID,'labSourceId_month')
    source_day = (By.ID,'labSourceId_day')
    def label_source_select(self,source_type,text):
        if source_type == '月':
            self.select_by_text(self.source_month,text)
        elif source_type == '日':
            self.select_by_text(self.source_day,text)
    #获取数据源id
    def get_label_source(self,source_type):
        sourceid = ''
        if source_type == '月':
            sourceid = self.find_element_value(self.source_month)
        elif source_type == '日':
            sourceid = self.find_element_value(self.source_day)
        return sourceid

    #===================================更改月数据源===============================


    #===================================获取title===============================
    #获取title，全量 “订单” “数据”
    source_title = (By.CLASS_NAME,'source_title')
    def get_source_title(self):
        title = self.get_eles_text(self.source_title)
        if len(title) >= 1 :
            return self.get_eles_text(self.source_title)[0]
    #===================================获取title===============================

    #================================搜索标签名 或 枚举值名======================
    #切换标签名 或 枚举值名
    label_search_change_month = (By.ID,'treeSearchType_month')
    label_search_change_day = (By.ID,'treeSearchType_day')
    def label_search_select(self,sourceType,value):
        if sourceType=='月' or sourceType=='month':
            self.select_by_value(self.label_search_change_month,value)
        elif sourceType=='日' or sourceType=='day':
            self.select_by_value(self.label_search_change_day,value)

    #标签名称搜索
    def label_search(self,sourceType,label_type_search,labelName):

        if label_type_search == '枚举值':
            self.label_search_select(sourceType,'1')
        else:
            self.label_search_select(sourceType,'0')
        time.sleep(0.5)
        self.search_label_clear(sourceType)
        self.search_label_key(sourceType,labelName)
        self.search_label_btn(sourceType)


    #输入日标签名称，点击查询
    day_label_key_search = (By.ID,'filter_form_groupid_day')
    day_label_key_search_btn = (By.ID,'treeSearchBtn_day')
    #输入月标签名称，点击查询
    month_label_key_search = (By.ID,'filter_form_groupid_month')
    month_label_key_search_btn = (By.ID,'treeSearchBtn_month')

    def search_label_clear(self,sourceType):
        if sourceType == '月' :
            self.label_data_type('月')
            self.clear(self.month_label_key_search)
        elif sourceType=='month':
            self.clear(self.month_label_key_search)
        elif sourceType == '日':
            self.label_data_type('日')
            self.clear(self.day_label_key_search)
        elif sourceType=='day':
            self.clear(self.day_label_key_search)

    def search_label_key(self,sourceType,label):
        if sourceType == '月' or sourceType=='month':
            self.send_keys(self.month_label_key_search,label)
        elif sourceType == '日' or sourceType=='day':
            self.send_keys(self.day_label_key_search,label)

    def search_label_btn(self,sourceType):
        if sourceType == '月' or sourceType=='month':
            self.move_to_element_click(self.month_label_key_search_btn)
        elif sourceType == '日' or sourceType=='day':
            self.move_to_element_click(self.day_label_key_search_btn)
        

    #================================搜索标签名 或 枚举值名======================
    

    #=======================点击标签库高级==========================
    senior_button = (By.ID,'toSeniorBtn')
    def senior_button_click(self):
        self.move_to_element_click(self.senior_button)
        time.sleep(0.5)
        self.cover_is_display()

    senior_search = (By.XPATH,'//div[@class="main"]/div/div/div/h3[@data-sheet="self_help_search"]')
    def select_search(self):
        self.move_to_element_click(self.senior_search)


    #=======================点击标签库高级==========================

    add_acct_month = (By.XPATH,'//div[@class="contain"]/div/div[@class="month_tree"]/input[@class="date_add_btn"]')
    add_acct_day = (By.XPATH,'//div[@class="contain"]/div/div[@class="day_tree"]/input[@class="date_add_btn"]')
    def add_acct_month_click(self,source_type):
        if source_type == '月' or source_type == 'month':
            self.click(self.add_acct_month)
        elif source_type == '日' or source_type == 'day':
            self.click(self.add_acct_day)
    #点击and or
    symbol ='//div[@class="sql_area"]/div[@id="symbolList"]/span[@data-selname="'
    def label_symbol_click(self,text,*n):
        #n没有传值过来
        if len(n)==0:
            n=(1,)
        
        if text !='' and text!='输入框':
            for i in range(0,n[0]):
                symbol_ele = (By.XPATH,self.symbol+text+'"]')
                self.move_to_element_click(symbol_ele)
        elif text=='输入框':
            symbol ='//div[@class="sql_area"]/div[@id="symbolList"]/span[@class="input"]'
            self.move_to_element_click((By.XPATH,symbol))
        

    
    #================================枚举值/数值/时间 公用方法===================
    #点击查询结果的标签
    def label_btn_click(self,label):
        ele = (By.LINK_TEXT,label)
        # WebDriverWait(self.driver,20,0.5).until(self.ele_is_exist(ele))
        self.move_to_element_click(ele)
        self.cover_is_display()

    #标签上级目录点击
    def file_click(self,sourceType,labelFile):
        self.search_label_clear(sourceType)
        self.search_label_btn(sourceType)
        for f in labelFile:
            self.label_file_click(f)
    
    #点击标签上级目录
    def label_file_click(self,labelfile):
        #判断文件夹是否打开
        ele = (By.LINK_TEXT,labelfile)
        ids = self.find_element_attr(ele,'id')
        ele_span = (By.XPATH,'//*[@id="'+ ids[0] +'"]/span[1]')
        classes = self.find_element_attr(ele_span,'class')
        if 'ico_open' not in classes[0]:
            self.click((By.LINK_TEXT,labelfile))

    #查询的标签是否存在
    def label_exist(self,label):
        ele = (By.LINK_TEXT,label)
        return self.is_exist(ele)

    
    #打开文件拼接内容
    def file_content(self,file):
        filec = open(os.path.abspath('.')+file,encoding='gbk')
        cont = filec.readlines()
        return ','.join("'"+str(i)+"'" for i in cont ).replace('\n','')
        
    #账期选择
    acct_month = (By.ID, 'partitionName_month')
    acct_day = (By.ID,'partitionName_day')

    def select_acct_month(self,sourceType,timeformat,timeVal):
        if sourceType == '月' or sourceType=='month':
            self.move_to_element_click(self.acct_month)
        elif sourceType == '日' or sourceType=='day':
            self.move_to_element_click(self.acct_day)
        time.sleep(1)
        # self.click((By.XPATH, '//*[@id="jedatebox"]/ul/li[@ym="'+timeVal+'"]'))
        self.time_input(timeformat,timeVal)


    #点击枚举信息的保存按钮
    label_enum_btn = (By.ID,'saveLabelCodeBtn')
    def click_label_code_save(self):
        self.click(self.label_enum_btn)

    #点击数据类型信息的保存按钮
    label_data_ele = (By.ID,'saveLabelDataBtn')
    def click_labelData_save(self):
        self.click(self.label_data_ele)
    #点击时间类型信息的保存按钮
    label_time_ele = (By.ID,'saveLabelTimeBtn')
    def click_labelTime_save(self):
        self.click(self.label_time_ele)
    #点击大枚举值类型信息的保存按钮
    label_bigcode_btn = (By.ID,'saveLabelBigCodeBtn')
    def click_labelBigCode_save(self):
        self.move_to_element_click(self.label_bigcode_btn)

    #-----------弹框提示----------
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
        if True == self.is_exist(self.alert):
            return self.find_element_attr(self.alert,'data-text')[0]
    
    def alert_is_exist(self):
        return self.is_exist_no_wait(self.alert)


    def wait_alert(self):
        WebDriverWait(self.driver,20,0.5).until(self.ele_is_exist(self.alert))
    #-----------弹框提示----------

    #关闭按钮
    alert_close_btn = (By.ID,'close_dialog_labelCode')
    def click_label_code_close(self):
        self.click(self.alert_close_btn)

    #-----------点击关闭05标签的下钻图层---------------
    type5 = (By.XPATH,'//div[@id="ztreeWraper_month"]/div[@class="filter_ztree_type05"]')
    type5_close = (By.XPATH,'//div[@id="ztreeWraper_month"]/div[@class="filter_ztree_type05"]/i')
    def close_type5(self):
        if True == self.is_display_no_wait(self.type5):
            self.click(self.type5_close)

    #---------------高级版查询条件勾选账期------------
    
    def select_acct_month_condition(self,acct_months,acct_ele):
        id = '-1' 
        is_select = False
        if acct_months!='':
            labels = self.get_eles_text((By.XPATH,acct_ele))
            for i in range(0,len(labels)):
                if (labels[i][-7:-1] not in acct_months ) or (is_select == True):
                    ele = (By.XPATH,acct_ele+'['+str(i+1)+']/input')
                    if True == self.ele_is_selected(ele):
                        self.move_to_element_click(ele)
                else:
                    ele = (By.XPATH,acct_ele+'['+str(i+1)+']/input')
                    id = self.find_element_attr(ele,'data-datatype')[0]
                    is_select = True

        return id   

    #================================枚举值/数值/时间 公用方法===================

    #================================枚举值标签=================================
    #枚举值点击

    body_cover_id = (By.ID,'body_cover')
    def enum_click(self,labelname,labelValue,*acct_month):
        self.label_btn_click(labelname)
        
        #高级版勾选账期
        id=''
        if acct_month!=():
            id = self.select_acct_month_condition(acct_month[0],'//div[@id="dialog_labelCode"]/div/div/label')

        self.select_enum_info(labelValue)
        self.click_label_code_save()
        # if self.is_display(self.cover) == True:
        #     time.sleep(2)
        # elif self.is_display(self.body_cover_id) == True:
        #     alert = self.alert_tip()
        #     if '不能勾选全部' in alert:
        #         self.alert_btn_click()
        #         id = 'not_all'
        #     time.sleep(1)
        assert self.is_display(self.cover) == True
         
        return id 

    #点击枚举值的值
    def select_enum_info(self,labelValues):
        for labelValue in labelValues:
            label_a = (By.XPATH,'//ul[@id="labelCodeTree_1_ul"]/li/a[@title="'+labelValue+'"]')
            if self.is_exist(label_a):
                a_id = self.find_element_attr(label_a,'id')
                check_id = a_id[0][0:-1]+'check'
                self.move_to_element_click((By.ID,check_id))


    #================================枚举值标签=================================


    #================================数值标签=================================
    #数据类型点击
    def num_click(self,labelName,labelValue,*acct_month):
        self.label_btn_click(labelName)

        #高级版勾选账期
        id=''
        if acct_month!=():
            id = self.select_acct_month_condition(acct_month[0],'//div[@id="dialog_labelData"]/div/div/div/label')

        # 选择大于2分钟，小于100分钟
        if labelValue[0] == '' :
            self.start_sign_select('>')
        else :
            self.start_sign_select(labelValue[0])

        if len(labelValue) > 1:
            self.input_Tmonth_start_info(labelValue[1])
        if len(labelValue) > 2:
            self.middle_flag_select(labelValue[2])
        if len(labelValue) > 3:
            self.end_sign_select(labelValue[3])
        if len(labelValue) > 4:
            self.input_Tmonth_end_info(labelValue[4])
        time.sleep(1)
        #点击确定保存按钮
        self.click_labelData_save()
        return id

    #数据类型输入
    T_month_call_start_ele = (By.ID,'startVal')
    T_month_call_end_ele = (By.ID,'endVal')
    middle_flag_ele = (By.ID,'middleFlag')
    end_Sign_ele = (By.ID,'endSign')
    start_Sign_ele = (By.ID,'startSign')
    def input_Tmonth_start_info(self,startVal):
        self.send_keys(self.T_month_call_start_ele,startVal)
    def middle_flag_select(self,middle_flag):
        self.select_by_value(self.middle_flag_ele,middle_flag)
    def end_sign_select(self,end_sign):
        self.select_by_value(self.end_Sign_ele,end_sign)
    def start_sign_select(self,startSign):
        self.select_by_value(self.start_Sign_ele,startSign)
    def input_Tmonth_end_info(self,endVal):
        self.send_keys(self.T_month_call_end_ele,endVal)
    #================================数值标签=================================

    
    #=========================时间选择框点击==========================


    def time_click(self,labelName,dateFormate,values,*acct_month):
        self.label_btn_click(labelName)

        #高级版勾选账期
        id=''
        if acct_month!=():
            id = self.select_acct_month_condition(acct_month[0],'//div[@id="dialog_labelTime"]/div/div/div/label')

        if values[0]!='':
            self.input_time_start_info(dateFormate,values[0])
        if len(values) == 2 and values[1]!='':
            self.input_time_end_info(dateFormate,values[1])
        self.click_labelTime_save()
        return id

    #时间类型输入
    time_start_ele = (By.ID,'tagTimerStart')
    time_end_ele = (By.ID,'tagTimerEnd')
    def input_time_start_info(self,label_formate,startTime):
        self.move_to_element_click(self.time_start_ele)
        self.time_input(label_formate,startTime)
    def input_time_end_info(self,label_formate,endTime):
        self.move_to_element_click(self.time_end_ele)
        self.time_input(label_formate,endTime)



    #根据时间格式进行选择
    def time_input(self,label_formate,time):
        if label_formate == 'YYYYMMDD': 
            if time != '': 
                self.change_YYYYMMDD(time)
        elif label_formate == 'YYYYMM':
            if time != '': 
                self.change_YYYYMM(time)
        elif label_formate == 'YYYYMMDDhhmmss':
            if time != '': 
                self.change_YYYYMMDDHHMMSS(time)

    #-------------年月格式选日期----------------
    date = (By.CLASS_NAME,'jedateyear')
    pre_date = (By.XPATH,'//i[@class="prev triangle yearprev"]')
    next_date = (By.XPATH,'//i[@class="next triangle yearnext"]')
    def change_YYYYMM(self,time):
        time = datetime.datetime.strptime(time,'%Y%m')
        yy = time.strftime('%Y')
        while yy < self.get_text(self.date).split('-')[0]:
            self.click(self.pre_date)
        while yy > self.get_text(self.date).split('-')[0]:
            self.click(self.next_date)
        
        time = time.strftime('%Y-%m')
        ele = (By.XPATH,'//ul[@class="jedaym"]/li[@ym="'+time+'"]')
        self.click(ele)

    #----------------年月日格式选日期---------------
    def change_year(self,yy):
        #切换年份
        ele_year = (By.XPATH,'//em[@class="jedateyear"]')
        self.click(ele_year)
        ele_year_min = (By.XPATH,'//ul[@class="ymdropul"]/li[1]')
        ele_year_max = (By.XPATH,'//ul[@class="ymdropul"]/li[15]')
        year_min = self.find_element_attr(ele_year_min,'yy')[0]
        year_max = self.find_element_attr(ele_year_max,'yy')[0]
        if yy < year_min:
            self.move_to_element_click((By.XPATH,'//span[@class="jedateymchle"]'))
        if yy > year_max:
            self.move_to_element_click((By.XPATH,'//span[@class="jedateymchri"]'))
        ele_yy = (By.XPATH,'//li[@yy="'+yy+'"]')
        self.move_to_element_click(ele_yy)
    def change_month(self,mm):
        #切换月份
        ele_month = (By.XPATH,'//em[@class="jedatemonth"]')
        self.click(ele_month)
        ele_mm = (By.XPATH,'//li[@mm="'+mm+'"]')
        self.click(ele_mm)
    def change_YYYYMMDD(self,time):
        #字符串转日期格式
        time = datetime.datetime.strptime(time,'%Y%m%d')
        yy = time.strftime('%Y')
        mm = time.strftime('%m')

        self.change_year(yy)
        self.change_month(mm)      
        #转字符串格式，并将01变成1
        time = time.strftime('%Y-%m-%d').replace('-0','-')
        ele = (By.XPATH,'//div[@id="jedatebox"]/ul/li[@data-ymd="'+time+'"]')
        self.click(ele)
    #------------------年月日时分秒格式选日期--------------------
    datehms = (By.CLASS_NAME,'jedatehms')
    def change_hms(self,ele):
        self.click(self.datehms)
        self.click(ele)
    def change_YYYYMMDDHHMMSS(self,time):
        #字符串转日期格式
        time = datetime.datetime.strptime(time,'%Y%m%d%H%M%S')
        yy = time.strftime('%Y')
        mm = time.strftime('%m')
        self.change_year(yy)
        self.change_month(mm)  
        hh = time.strftime('%H')
        MM = time.strftime('%M')
        SS = time.strftime('%S')
        self.change_hms((By.XPATH,'//div[@class="jedatehmscon jedateprophours"]/p['+str(int(hh)+1)+']'))
        self.change_hms((By.XPATH,'//div[@class="jedatehmscon jedatepropminutes"]/p['+str(int(MM)+1)+']'))
        self.change_hms((By.XPATH,'//div[@class="jedatehmscon jedatepropseconds"]/p['+str(int(SS)+1)+']'))
        #转字符串格式，并将01变成1
        time = time.strftime('%Y-%m-%d').replace('-0','-')
        ele = (By.XPATH,'//div[@id="jedatebox"]/ul/li[@data-ymd="'+time+'"]')
        self.click(ele)

    #================================上传大数量枚举值标签，超过500条的需要上传勾选的标签===================================

    def enum_bigCode_click(self,labelName,labelValue,inverse,labelSelects,*acct_month):
        self.label_btn_click(labelName)
        time.sleep(0.5)

        #高级版勾选账期
        id=''
        if acct_month!=():
            id = self.select_acct_month_condition(acct_month[0],'//div[@id="dialog_labelCode"]/div/div/label')

        if labelValue!='':
            self.label_upload(labelValue)
            if '.txt' in self.get_label_upload_result():
                self.label_upload_btn_click()
                time.sleep(1)
                alert = self.alert_tip()
                self.alert_btn_click()
                assert '上传成功' in alert
                time.sleep(1)
        #搜索
        labels = []
        if labelSelects!='':
            for  labelSelect in labelSelects:
                self.label_value_search(labelSelect['labelSearch'])
                time.sleep(1)

                if labelSelect['labelValue'] == 'all' :
                    labels = labels + self.get_label_values()
                    time.sleep(0.5)
                    for ll in labels:
                        self.label_btn_click(ll)
                else:
                    labels = labels + labelSelect['labelValue']
                    for labelValue in labelSelect['labelValue']:
                        self.label_btn_click(labelValue)


        #反选
        if '是' == inverse and False == self.alert_is_exist():
            self.inverse_enum_click()
                    
        self.click_label_code_save()
        assert self.is_display(self.cover) == True

        return labels,id

    #枚举值大数量上传枚举值文件
    upload_enum = (By.ID,'uploadEnumFile')
    def label_upload(self,value):
        self.send_keys(self.upload_enum,os.path.abspath('.')+value)
    #获取上传结果
    def get_label_upload_result(self):
        return self.find_element_value(self.upload_enum)

    upload_enum_btn = (By.ID,'uploadEnumBtn')
    def label_upload_btn_click(self):
        self.click(self.upload_enum_btn)

    #枚举值大数据量反选
    inverse_enum_ele = (By.ID,'inverseEnumBtn')
    def inverse_enum_click(self):
        self.click(self.inverse_enum_ele)

    #枚举值名称搜索
    def label_value_search(self,labelValueName):
        self.search_value_label_clear()
        self.search_value_label_key(labelValueName)
        self.search_value_label_btn()

    #获取查询的所有枚举值
    label_values= (By.XPATH,'//ul[@id="labelCodeTree_1_ul"]/li')
    def get_label_values(self):
        return self.get_eles_text(self.label_values)

    #输入枚举值名称，点击查询
    label_key_search = (By.ID,'labelCodeGroupId')
    label_key_search_btn = (By.ID,'searchMunmBtn')

    def search_value_label_clear(self):
        self.clear(self.label_key_search)

    def search_value_label_key(self,label):
        self.send_keys(self.label_key_search,label)

    def search_value_label_btn(self):
        self.move_to_element_click(self.label_key_search_btn)
    #================================上传大数量枚举值标签===================================
    
    
    #=================================大枚举值，userid这类，type=07类型的=================================================

    def bigCode_click(self,labelName,value,inverse,*acct_month):
        self.label_btn_click(labelName)
        time.sleep(0.5)

        #高级版勾选账期
        id=''
        if acct_month!=():
            id = self.select_acct_month_condition(acct_month[0],'//div[@id="dialog_labelBigCode"]/div/div/label')

        self.bigcode_upload_sendkeys(value)
        if '.txt' in self.bigcode_upload_result():
            self.bigcode_upload_click()
            alert = self.alert_tip()
            time.sleep(1)
            self.alert_btn_click()
            assert '上传成功' in alert
            time.sleep(1)
        #反选
        if '是' == inverse and False == self.alert_is_exist():  
            self.bigcode_inverse_click()
        self.click_labelBigCode_save()
        return id


    #大枚举值上传
    bigcode_upload = (By.ID,'uploadBigCodeEnumFile')
    def bigcode_upload_sendkeys(self,value):
        self.send_keys(self.bigcode_upload,os.path.abspath('.')+value)

    #获取上传结果
    def bigcode_upload_result(self):
        return self.find_element_value(self.bigcode_upload)

    #点击上传
    bigcode_uplaod_click = (By.ID,'uploadBigCodeEnumBtn')
    def bigcode_upload_click(self):
        self.move_to_element_click(self.bigcode_uplaod_click)

    #反选
    bigcode_inverse = (By.ID,'inverseBigCodeEnumBtn')
    def bigcode_inverse_click(self):
        self.move_to_element_click(self.bigcode_inverse)

    #=======================================大枚举值=================================================



    #=======================================标签查询列表=========================================
    # 获取标签code

    # label_filter = (By.XPATH,'//tbody[@id="labelFilterTable"]/tr/td[1]')
    # def get_label_code(self,labelName):
    #     # label_filter_text = self.get_eles_text(self.label_filter)
    #     # i = 0 
    #     # code = ''
    #     # for label in label_filter_text:
    #     #     i = i + 1
    #     #     if labelName == label :
    #     #         break
    #     # code = self.find_element_attr((By.XPATH,'//tbody[@id="labelFilterTable"]/tr['+str(i)+']'),'data_id')[0]
    #     # return code






    def get_format(self,labelValues):
        labelValue = ''
        for value in labelValues:
            if value != '':
                labelValue = value
        label_format = 'YYYYMM'
        if len(labelValue) == 8:
            label_format = 'YYYYMMDD'
        elif len(labelValue) == 14:
            label_format = 'YYYYMMDDhhmmss'
        return label_format

    #获取查询标签列表
    label_filter_table_info = (By.XPATH,'//tbody[@id="labelFilterTable"]/tr/td[@class="condition_tooltip"]')
    data_title = 'data-original-title'
    def get_label_filter_table_info(self):
        return self.find_element_attr(self.label_filter_table_info,self.data_title)

    #获取是否反选
    label_filter_inverse = (By.CLASS_NAME,'invert_select')
    def get_label_filter_inverse(self):
        return self.is_exist(self.label_filter_inverse)

    #=======================================标签查询列表=========================================

    
    #===============================点击提交按钮==========================================
    #点击提交查询按钮
    commit_btn = (By.ID,'queryDataBtn')
    def query_data_btn_click(self):
        self.move_to_element_click(self.commit_btn)
        self.cover_is_display()

    #===============================点击提交按钮==========================================

    #======================================获取查询结果列表=====================================
    #获取查询结果列表
    label_return_count_table_info = (By.XPATH,'//table[@id="returnCountTable"]/tbody/tr[2]/td')
    returnCount = (By.ID,'returnCountDiv') 
    def get_return_count_table_info(self):
        while self.is_display_no_wait(self.returnCount) == False:
            time.sleep(1)
        return self.get_eles_text(self.label_return_count_table_info)
    #======================================获取查询结果列表=====================================

    #=====================================全量用户=================================
    #点击全量按钮
    all_user = (By.ID,'allUser')
    def all_user_click(self):
        self.move_to_element_click(self.all_user)
    #====================================上传用户===============================
    #上传按钮
    upload_user_radio_ele = (By.ID,'updataUser')
    def upload_user_click(self):
        self.move_to_element_click(self.upload_user_radio_ele)

    dataType_label = '//ul/li[@class="userDataFlag"]/span/label'
    def upload_dataType_click(self,dataType):
        ele = self.find_elements((By.XPATH,self.dataType_label))
        for i in range(0,len(ele)):
            if ele[i].text == dataType:
                self.move_to_element_click((By.XPATH,self.dataType_label+'['+str(i+1)+']/input'))
                time.sleep(0.3)
                break

    #输入上传文件名称
    upload_user_name = (By.ID,'groupName')
    def upload_user_sendkeys(self,name):
        self.send_keys(self.upload_user_name,name)

    #点击剔除radio
    upload_notinner_radio_ele = (By.ID,'userType06')
    def upload_user_notinner_click(self):
        self.click(self.upload_notinner_radio_ele)
    
    #上传文件
    upload_file_ele = (By.ID,'uploadFile')
    def upload_user_file(self,file_path):
        self.send_keys(self.upload_file_ele,os.path.abspath('.')+file_path)

    #点击上传按钮
    upload_file_btn_ele = (By.ID,'uploadBtn')
    def upload_user_btn(self):
        self.move_to_element_click(self.upload_file_btn_ele)
        self.cover_is_display()

    #输入描述
    upload_file_remark = (By.ID,'remarkGroup')
    def upload_user_remark(self,remark):
        self.send_keys(self.upload_file_remark,remark)
    
    #点击确定提交按钮
    upload_file_submit = (By.XPATH,'//div[@id="dialog_uploadUsers"]/div/div[@class="my_btns"]/input[@id="addGroupBtn"]')
    def upload_user_submit_click(self):
        self.move_to_element_click(self.upload_file_submit)
        self.cover_is_display()
    #====================================上传用户===============================

    #====================================已传用户===============================
    #点击已传按钮
    uploaded_user_radio_ele = (By.ID,'updataUsered')
    def uploaded_user_click(self):
        if self.is_exist(self.uploaded_user_radio_ele):
            self.move_to_element_click(self.uploaded_user_radio_ele)


    #选择已传数据群
    uploaded_users_ele_str = '//div[@id="dialog_groupUsers"]/div/div/table/tbody[@id="groupUserTab"]/tr'
    dialog_groupUsers = (By.XPATH,'//div[@id="dialog_groupUsers"]')
    #勾选关联和剔除查询
    uploaded_users_ele = (By.XPATH,uploaded_users_ele_str)
    def uploaded_users_click(self,texts):
        if self.is_display_no_wait(self.dialog_groupUsers) == False:
            time.sleep(3)
        upload_users = self.find_elements(self.uploaded_users_ele)
        l = len(upload_users)
        inner = True
        tichu = True
        tables = {}
        if l > 1:
            table_len = len(self.get_eles_text((By.XPATH,self.uploaded_users_ele_str+'[1]/td')))

        for i in range(0,l):
            ele = (By.XPATH,self.uploaded_users_ele_str+'['+str(i+1)+']')
            if inner != True and tichu != True:
                break
            for text in texts:
                if (self.text_is_exist_no_wait(ele,text) == True ) and (inner == True or tichu == True):


                    if '关联查询' == self.get_text((By.XPATH,self.uploaded_users_ele_str+'['+str(i+1)+']/td['+str(table_len-2)+']')) and inner == True:
                        inner = False
                        ele1 = (By.XPATH,self.uploaded_users_ele_str+'['+str(i+1)+']/td[1]/input')
                        if False == self.ele_is_selected(ele1):
                            self.click(ele1)
                        ele2 = (By.XPATH,self.uploaded_users_ele_str+'['+str(i+1)+']/td['+str(table_len)+']/input')

                        tables['inner']=(self.find_element_attr(ele2,'data_val')[0].split('.')[0])
                        tables['inner_id'] = (self.find_element_attr(ele2,'data_id')[0].split('.')[0])

                    elif '剔除查询' == self.get_text((By.XPATH,self.uploaded_users_ele_str+'['+str(i+1)+']/td['+str(table_len-2)+']')) and tichu == True:
                        tichu = False
                        ele1 = (By.XPATH,self.uploaded_users_ele_str+'['+str(i+1)+']/td[1]/input')
                        if False == self.ele_is_selected(ele1):
                            self.click(ele1)
                        ele2 = (By.XPATH,self.uploaded_users_ele_str+'['+str(i+1)+']/td['+str(table_len)+']/input')

                        tables['tichu']=(self.find_element_attr(ele2,'data_val')[0].split('.')[0])
                        tables['tichu_id'] = (self.find_element_attr(ele2,'data_id')[0].split('.')[0])

        return tables
    #删除已传客户群
    del_tip = (By.XPATH,'//div[@class="zMsg_alert_new"]/table/tbody/tr/td')
    del_alert = (By.XPATH,'//div[@class="zMsg_alert_new"]/table/tfoot/tr/td/button[@class="btn btn-normal"]')
    def delete_uploaded_users_click(self,texts):
        upload_users = self.find_elements(self.uploaded_users_ele)
        l = len(upload_users)
        if l > 1:
            table_len = len(self.get_eles_text((By.XPATH,self.uploaded_users_ele_str+'[1]/td')))
        i = 0
        text_list = []
        if type(texts)==str:           
            text_list.append(texts)
        elif type(texts)==list:
            text_list = texts
        while i < l :
            ele = (By.XPATH,self.uploaded_users_ele_str+'['+str(i+1)+']')
            ele_select = (By.XPATH,self.uploaded_users_ele_str+'['+str(i+1)+']/td[1]/input')
            for text in text_list:
                if self.text_is_exist_no_wait(ele,text) == True and self.ele_is_selected(ele_select) == False:
                    ele1 = (By.XPATH,self.uploaded_users_ele_str+'['+str(i+1)+']/td['+str(table_len)+']/input')
                    self.move_to_element_click(ele1)
                    while self.alert_is_exist()==False :
                        time.sleep(1)
                    if "移除" in self.get_text(self.del_tip):
                        time.sleep(1)
                        self.click(self.del_alert)
                    if "删除成功" in self.get_text(self.del_tip):
                        time.sleep(1)
                        self.click(self.del_alert)
                        l = l - 1 
                        i = i - 1 
                    elif "此客群不能删除" in self.get_text(self.del_tip):
                        time.sleep(1)
                        self.click(self.del_alert)
            i = i + 1
        
        return 'success'
    

    #点击关闭筛选按钮
    uploaded_close_btn_ele = (By.ID,'closeGroupBtn')
    def uploaded_close_btn_click(self):
        self.move_to_element_click(self.uploaded_close_btn_ele)

    #弹框确定按钮
    uploaded_users_btn = (By.ID,'selectGroupBtn')
    def uploaded_user_btn_click(self):
        self.move_to_element_click(self.uploaded_users_btn)

    
    #====================================已传用户===============================

    #==================================保存筛选==================================

    #点击保存筛选按钮
    # save_filter = (By.XPATH,'//div[@id="select_group"]/span[@class="table_btns"]/input[@id="toSaveLabelFilterBtn"]')
    save_filter = (By.XPATH,'//*[@id="toSaveLabelFilterBtn"]')
    def save_filter_click(self):
        # self.scroll_to_position('0')
        self.add_attr('body > div.main',0,'style','height: 98%;')
        self.scroll_to_ele(self.save_filter)        
        # self.scroll_to_ele('#toSaveLabelFilterBtn') 
        time.sleep(1)
        self.click(self.save_filter)


    # dialog_labelFilter = (By.ID,'dialog_labelFilter')
    # def alert_is_show(self):
    #     while self.is_display_no_wait(self.dialog_labelFilter) == False:
    #         time.sleep(1)

    #保存筛选信息
    filter_name = (By.XPATH,'//*[@id="dialog_labelFilter"]/div/div[@class="panel_body"]/ul/li/input[@id="filterName"]')
    filter_remark = (By.XPATH,'//*[@id="dialog_labelFilter"]/div/div[@class="panel_body"]/ul/li/textarea[@id="remark"]')
    filter_type =  '//*[@id="dialog_labelFilter"]/div/div[@class="panel_body"]/ul/li/span/input'
    filter_staff_search = (By.XPATH,'//li[@id="showFilterDiv"]/div/span/input[@id="input_staff"]')
    filter_staff_search_click = (By.XPATH,'//li[@id="showFilterDiv"]/div/span/input[@id="searchBtn"]')
    # filter_staff_list = (By.ID,'dialog_authorize_staff')
    # filter_staff = '//div[@id="dialog_authorize_staff"]/table/tbody/tr'
    filter_staff_list = (By.XPATH,'//li[@id="showFilterDiv"]/div/div')
    filter_staff = '//li[@id="showFilterDiv"]/div/div/div/table/tbody/tr'

    def save_filter_info(self,name,type,remark,is_senior,*staffs):

        self.send_keys(self.filter_name,name)
        self.send_keys(self.filter_remark,remark)
        if '我的' == type and is_senior == False:
            ele = (By.XPATH,self.filter_type+'[@value="02"]')
            self.move_to_element_click(ele)
        elif '公共' == type and is_senior == False:
            ele = (By.XPATH,self.filter_type+'[@value="01"]')
            self.move_to_element_click(ele)
        elif '我的' == type and is_senior == True:
            ele = (By.XPATH,self.filter_type+'[@value="12"]')
            self.move_to_element_click(ele)
        elif '公共' == type and is_senior == True:
            ele = (By.XPATH,self.filter_type+'[@value="11"]')
            self.move_to_element_click(ele)
        elif '分享' == type :
            if is_senior == False:
                ele = (By.XPATH,self.filter_type+'[@value="03"]')
            elif is_senior == True:
                ele = (By.XPATH,self.filter_type+'[@value="13"]')
            self.move_to_element_click(ele)
            time.sleep(1)
            if self.is_display(self.filter_staff_search):
                for staff in staffs[0]:
                    self.clear(self.filter_staff_search)
                    self.send_keys(self.filter_staff_search,staff)
                    self.click(self.filter_staff_search_click)
                    self.cover_is_display()
                    filter_list = self.find_elements((By.XPATH,self.filter_staff))
                    
                    if  len(filter_list) > 0:
                        for i in range(1,len(filter_list)+1):
                            staff_name = self.get_text((By.XPATH,self.filter_staff+'['+str(i)+']/td[2]'))
                            if staff_name == staff:
                                self.move_to_element_click((By.XPATH,self.filter_staff+'['+str(i)+']/td[1]'))
                                break
        return 'success'




    #点击弹框确定
    filter_staff_btn = (By.XPATH,'//div[@id="dialog_labelFilter"]/div/div[@class="my_btns"]/input[@id="saveLabelFilterBtn"]')
    def filter_staff_btn_click(self):
        self.move_to_element_click(self.filter_staff_btn)
        self.cover_is_display()





    #==================================保存筛选==================================


    #===================================保存用户====================================
    #点击保存用户
    save_user_btn_ele = (By.ID,'addMktGroupUser')
    def save_user_click(self):
        self.move_to_element_click(self.save_user_btn_ele)

    #保存客户群名称
    save_user_name_ele = (By.ID,'groupMktName')
    save_user_remark_ele = (By.ID,'remarkMktGroup')
    def save_user_name_sendkeys(self,usersName):
        self.send_keys(self.save_user_name_ele,usersName)

    save_user_expiration_time_ele = (By.ID,'addExpirationTime')
    def save_user_expiration_time(self,timeVal):
        self.click(self.save_user_expiration_time_ele)
        time.sleep(0.5)
        self.time_input('YYYYMMDD',timeVal)

    def save_user_remark_sendkeys(self,usersRemark):
        self.send_keys(self.save_user_remark_ele,usersRemark)

    #点击保存按钮
    save_user_submit_ele = (By.ID,'addMktGroupBtn')   
    def save_user_submit_click(self):
        self.click(self.save_user_submit_ele)
        self.cover_is_display()
    #===================================保存用户====================================


    #==================================已存用户=====================================
    #点击已存按钮
    saved_user_radio_ele = (By.ID,'saveUsered')
    def saved_user_click(self):
        self.move_to_element_click(self.saved_user_radio_ele)
        self.cover_is_display()


    #选择已存数据群
    saved_users_ele_str = '//tbody[@id="saveGroupUserTab"]/tr'
    saved_users_ele = (By.XPATH,saved_users_ele_str)
    def saved_users_click(self,text):
        save_users = self.find_elements(self.saved_users_ele)
        l = len(save_users)
        for i in range(0,l):
            ele = (By.XPATH,self.saved_users_ele_str+'['+str(i+1)+']')
            if self.text_is_exist_no_wait(ele,text):
                ele1 = (By.XPATH,self.saved_users_ele_str+'['+str(i+1)+']/td[1]/input')
                if False == self.ele_is_selected(ele1):
                    self.click(ele1)
                ele2 = (By.XPATH,self.saved_users_ele_str+'['+str(i+1)+']/td[2]')
                return self.find_element_attr(ele2,'data-sql')[0]
                
    #删除已存数据群
    def delete_saved_users_click(self,text):
        save_users = self.find_elements(self.saved_users_ele)
        l = len(save_users)
        i = 0 
        while i < l:
            ele = (By.XPATH,self.saved_users_ele_str+'['+str(i+1)+']')
            ele_select = (By.XPATH,self.saved_users_ele_str+'['+str(i+1)+']/td[1]/input')
            if self.text_is_exist_no_wait(ele,text)==True and self.ele_is_selected(ele_select) == False:
                ele1 = (By.XPATH,self.saved_users_ele_str+'['+str(i+1)+']/td/input[@value="删除"]')
                time.sleep(1)
                self.move_to_element_click(ele1)
                if "移除" in self.get_text(self.del_tip):
                    time.sleep(1)
                    self.click(self.del_alert)
                if "删除成功" in self.get_text(self.del_tip):
                    time.sleep(1)
                    self.click(self.del_alert)
                    l = l - 1
                elif "此客群不能删除" in self.get_text(self.del_tip):
                    time.sleep(1)
                    self.click(self.del_alert)
                    i = i + 1
            else:
                i = i + 1
        
        return 'success'
    
    #点击已存用户确定按钮
    saved_user_btn_ele = (By.ID,'selectSaveGroupBtn')
    def saved_user_btn_click(self):
        self.move_to_element_click(self.saved_user_btn_ele)

    #点击已存用户关闭按钮
    saved_close_btn_ele = (By.ID,'closeSaveGroupBtn')
    def saved_close_btn_click(self):
        self.move_to_element_click(self.saved_close_btn_ele)

    #==================================已存用户=====================================
    

    #==================================明细提取=====================================
    #点击明细提取
    get_data_btn = (By.ID,'getDataBtn')
    def get_data_btn_click(self):
        self.click(self.get_data_btn)

    #点击标签后的添加导出标签按钮
    add_user_upload = (By.ID,'setAdd')
    def add_user_click(self):
        self.click(self.add_user_upload)

    #点击导出按钮
    export_data_btn = (By.ID,'exportDataBtn')
    def export_data_btn_click(self):
        self.move_to_element_click(self.export_data_btn)
        self.cover_is_display()

    #点击取消
    close_btn = (By.XPATH,'//div[@id="dialog_dataSet"]/div/div[@class="data_extract"]/ul/li/div[@class="my_btns"]/input[@class="close_btn"]')
    def close_btn_click(self):
        self.click(self.close_btn)
    #==================================明细提取=====================================

    #==================================统计分析=====================================
    #统计分析按钮
    count_analy_btn = (By.ID,'showCountBtn')
    def count_analy_btn_click(self):
        self.click(self.count_analy_btn)
    
    #统计分析普通版切换数据源
    analy_source = (By.ID,'selectCountFunId')
    def select_analy_source(self,source):
        self.select_by_text(self.analy_source,source)
    
    #统计分析高级版切换数据源
    analy_source_senior = '//div[@id="analyzeSelect"]'
    def select_analy_source_senior(self,source):
        analy_source_senior_click = self.analy_source_senior+'/div/ul/li'
        # self.move_to_element_click((By.XPATH,self.analy_source_senior))
        self.ele_show('$("#analyzeSelect>div")')
        texts = self.get_eles_text((By.XPATH,analy_source_senior_click))
        i = 0
        for text in texts:
            if source == text :
                self.move_to_element_click((By.XPATH,analy_source_senior_click+'['+str(i+1)+']'))
                break
            i = i+1

    #点击指标库
    dimension_panel = (By.XPATH,'//div[@id="countDiv"]/div[@class="row"]/div/div/div/div/dl/dd[@data-sheet="dimension_panel2"]/small')
    target_panel = (By.XPATH,'//div[@id="countDiv"]/div[@class="row"]/div/div/div/div/dl/dd[@data-sheet="target_panel2"]/small')
    def dimension_panel_click(self):
        self.click(self.dimension_panel)

    def target_panel_click(self):
        self.click(self.target_panel)

    #点击统计数据
    count_data_btn = (By.ID,'selectCountBtn')
    def count_data_btn_click(self):
        self.move_to_element_click(self.count_data_btn)
        self.cover_is_display()

    
    #统计分析结果
    countResultTable = (By.ID,'countResultTable')
    def get_count_result(self):
        self.is_display(self.countResultTable)

    #维度
    def dim_input_click(self,label):
        label_ele = (By.XPATH,'//ul[@id="dimList"]/li/label/input[@data-val="'+label+'"]')
        self.click(label_ele)
    #指标
    def quota_input_click(self,label):
        label_ele = (By.XPATH,'//ul[@id="quotaList"]/li/label/input[@data-val="'+label+'"]')
        self.click(label_ele)

    #统计分析结果
    result_is_display= (By.ID,'countResultTable')
    count_result = (By.XPATH,'//table[@id="countResultTable"]/tbody/tr[1]/td')
    def analy_result(self):
        if False == self.is_display(self.result_is_display):
            time.sleep(3)
        return self.get_eles_text(self.count_result)
    #==================================统计分析=====================================


    #===============================模板====================================

    filter_ele = (By.XPATH,'//*[@id="userFilterLi"]/span')
    def filter_user_click(self):
        self.move_to_element_click(self.filter_ele)


    def filter_click(self,filter_type):
        id = 'my_panel'
        if filter_type == '我的':
            id ='my_panel'
        elif filter_type == '分享':
            id ='share_panel'
        elif filter_type == '公共':
            id ='sys_panel'
        ele = (By.ID,id)
        time.sleep(0.5)
        if self.is_exist(ele):
            self.move_to_element_click(ele)
            self.cover_is_display()

    def select_filter(self,filter_type,name):
        self.filter_click(filter_type)
        time.sleep(1)
        id = 'myLabels'
        if filter_type == '我的':
            id ='myLabels'
        elif filter_type == '分享':
            id ='shareLabels'
        elif filter_type == '公共':
            id ='sysLabels'
        ele = (By.XPATH,'//ul[@id="'+id+'"]/li')
        if self.is_exist_no_wait(ele)==True:   
            eles = self.find_elements(ele)
            for ele in eles:
                if name in ele.text:
                    ele.click()
                    break

    def delete_filter(self,filter_type,names):
        
        self.filter_click(filter_type)
        time.sleep(1)

        id = 'myLabels'
        if filter_type == '我的':
            id ='myLabels'
        elif filter_type == '分享':
            id ='shareLabels'
        elif filter_type == '公共':
            id ='sysLabels'
        ele = (By.XPATH,'//ul[@id="'+id+'"]/li')
        if self.is_exist_no_wait(ele)==True:   
            texts = self.get_eles_text(ele)
            l = len(texts)
            i = 0
            while i < l:
                for name in names:
                    time.sleep(1)
                    if (name in self.get_eles_text(ele)[i]) and ('×' in self.get_eles_text(ele)[i]) :
                        ele_colse = (By.XPATH,'//ul[@id="'+id+'"]/li['+str(i+1)+']/i')
                        self.move_to_element_click(ele_colse)
                        time.sleep(0.5)
                        self.alert_sure_btn_click('确 定')
                        i = i-1
                        l = l-1
                        break
                i = i+1





    #=============================================高级输入框=====================================================

    input_value = '//*[@class="changewidth"]'
    def set_input_value(self,val):
        val = val.replace('\'','\\\'')
        eles = self.find_elements((By.XPATH,self.input_value))
        l = len(eles)
        if l-1 > 0:
            self.add_attr('#sqlLabel .input .changewidth',l-1,'value',val)
        else:
            self.add_attr('#sqlLabel .input .changewidth',0,'value',val)


    # =============================================已存模板===============================================================

    save_download_btn = (By.ID,'toSaveDownloadFilterBtn')
    download_filter = (By.XPATH,'//*[@id="dialog_downloadlabelFilter"]/div[@class="panel_main"]')
    downlaod_filter_name = (By.XPATH,'//*[@id="downloadfilterName"]')
    download_filter_remark = (By.XPATH,'//*[@id="downloadremark"]')
    download_filter_type = '//*[@id="dialog_downloadlabelFilter"]/div/div[1]/ul/li[2]/span/input'
    download_filter_staff_search = (By.XPATH,'//*[@id="input_staff_export"]')
    download_filter_staff_search_click = (By.ID,'searchExportBtn')
    download_filter_staff = '//*[@id="export_table_body"]/tr'
    def add_template(self,temName,temtype,temSub,is_senior,*staffs):
        self.move_to_element_click(self.save_download_btn)
        self.is_exist(self.download_filter)

        self.send_keys(self.downlaod_filter_name,temName)

        self.send_keys(self.download_filter_remark,temSub)

        if '我的' == temtype :
            if is_senior == '普通':
                ele = (By.XPATH,self.download_filter_type+'[@value="01"]')
            elif is_senior == '高级':
                ele = (By.XPATH,self.download_filter_type+'[@value="02"]')
            self.move_to_element_click(ele)
        elif '分享' == temtype :
            if is_senior == '普通':
                ele = (By.XPATH,self.download_filter_type+'[@value="11"]')
            elif is_senior == '高级':    
                ele = (By.XPATH,self.download_filter_type+'[@value="12"]')
            self.move_to_element_click(ele)
            self.cover_is_display()
            time.sleep(0.2)
            if self.is_display(self.download_filter_staff_search):
                for staff in staffs[0]:
                    self.clear(self.download_filter_staff_search)
                    self.send_keys(self.download_filter_staff_search,staff)
                    self.click(self.download_filter_staff_search_click)
                    filter_list = self.find_elements((By.XPATH,self.download_filter_staff))
                    
                    if  len(filter_list) > 0:
                        for i in range(1,len(filter_list)+1):
                            staff_name = self.get_text((By.XPATH,self.download_filter_staff+'['+str(i)+']/td[2]'))
                            if staff_name == staff:
                                self.move_to_element_click((By.XPATH,self.download_filter_staff+'['+str(i)+']/td[1]'))
                                break

        return 'success'

    
    #点击弹框确定
    download_filter_staff_btn = (By.XPATH,'//*[@id="saveDownloadFilterBtn"]')
    def download_filter_staff_btn_click(self):
        self.move_to_element_click(self.download_filter_staff_btn)

    download_selected_btn = (By.XPATH,'//*[@id="selectDownloadFilterBtn"]')
    def download_selected_btn_click(self):
        self.move_to_element_click(self.download_selected_btn)
        self.cover_is_display()
    #选择保存的下载模板
    saved_filter_staff_btn = (By.XPATH,'//*[@id="toSelectDownloadFilterBtn"]')
    saved_filter_type = '//*[@id="dialog_savelabelFilter"]/div/div[@class="panel_body"]/div/button'
    saved_filter_template = '//*[@id="labelDownloadFilterTab"]/tr'
    def select_template(self,temType,temName,is_senior):
        self.move_to_element_click(self.saved_filter_staff_btn)
        self.cover_is_display()
        if temType == '我的':
            if is_senior == '普通':
                self.move_to_element_click((By.XPATH,self.saved_filter_type+'[@filtertype="01"]'))
            elif is_senior == '高级':
                self.move_to_element_click((By.XPATH,self.saved_filter_type+'[@filtertype="02"]'))
        elif temType == '分享':
            if is_senior == '普通':
                self.move_to_element_click((By.XPATH,self.saved_filter_type+'[@filtertype="11"]'))
            elif is_senior == '高级':
                self.move_to_element_click((By.XPATH,self.saved_filter_type+'[@filtertype="12"]'))
        self.cover_is_display()
        time.sleep(0.2)
        eles_text = self.get_eles_text((By.XPATH,self.saved_filter_template+'/td[2]'))
        i = 1
        for text in eles_text:
            time.sleep(0.5)
            if temName in text:
                self.move_to_element_click((By.XPATH,self.saved_filter_template+'['+str(i)+']/td[1]'))
                break
            i = i+1
        self.download_selected_btn_click()
        return 'success'

    download_source = '//*[@id="treeSearchType"]'
    def change_source_download(self,source,is_senior):
        if is_senior == '高级':
            download_source = self.download_source +'/li'
            self.ele_show('$("#selectCustom div")')
            texts = self.get_eles_text((By.XPATH,download_source))
            i = 1
            for text in texts:
                if source == text:
                    self.move_to_element_click((By.XPATH,download_source+'['+str(i)+']'))
                    break
                i = i+1
        elif is_senior == '普通':
            self.select_by_text((By.XPATH,self.download_source),source)

    #判断高级版输入框是否有内容
    sqlLabel = (By.ID,'sqlLabel')
    def get_senior_content(self):
        return self.get_eles_text(self.sqlLabel)


    cover = (By.XPATH,'//body/div[@class="zMsg_cover cover_body"]')
    def cover_is_display(self):
        i = 0 
        while self.is_display(self.cover) == True and i < 30 :
            i = i + 1 
            time.sleep(3)
        


















