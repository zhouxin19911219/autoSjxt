#! /usr/bin/python
# coding=utf-8


from pages.basePage import Page
from selenium.webdriver.common.by import By
import datetime
import time
import sys
sys.path.append('.')
from common import param 
import os 



class ListPage(Page):
    # staff_name = param.staff_name
    # staff_id = str(param.staff_id)
    #员工id和姓名
    staff_no = param.staff_no

    
    # 清单切换数据清单
    datalist = (By.XPATH, '//button[@data-type="table"]')
    def datalist_click(self):
        self.move_to_element_click(self.datalist)


    #清单名称
    list_name_ele = (By.ID,'listName')
    def list_name_sendKeys(self,name):
       
        self.send_keys(self.list_name_ele,name)

    #账期
    acct_date_ele = (By.ID,'acctDate')
    def list_acctdate_sendKeys(self,acct_date):
        self.send_keys(self.acct_date_ele,acct_date)
    
    # 周期
    control = (By.ID, 'whetherCycle')
    def control_click(self,value):
        self.select_by_value(self.control, value)

    # 拆分SQL
    spilt_sql = (By.ID, 'tableName')
    def split_sql_sendkeys(self, sql):
        self.send_keys(self.spilt_sql, sql)


    #上传文件
    split_file_ele = (By.XPATH,'//*[@id="listFilePick"]/div/input')
    split_file_tips_ele = (By.XPATH,'//*[@id="listFilePick"]/div/small')


    split_file_remark_ele = (By.XPATH,'//div[@id="remarkListFilePick"]/div/input')
    split_file_remark_tips_ele = (By.XPATH,'//div[@id="remarkListFilePick"]/div/small')
    def list_file_upload(self,listFile):
        self.send_keys(self.split_file_ele,os.path.abspath('.')+listFile)

    def list_file_tips(self):
        return self.get_text(self.split_file_tips_ele)
    
    def list_file_remark_upload(self,listFile):
        self.send_keys(self.split_file_remark_ele,os.path.abspath('.')+listFile)
    
    def list_file_remark_tips(self):
        return self.get_text(self.split_file_remark_tips_ele)

    #审批
    require_approve_ele = (By.ID,"whetherApprove")
    approve_staff_ele = (By.XPATH,'//i[@class="icon-approve-person"]')
    approve_staff_search_ele = (By.ID,'staffDialogSearchInput')
    approve_staff_search_btn_ele = (By.ID,'staffDialogSearchBtn')
    approve_staff_select_ele = '//div[@id="dialog_authorize_staff"]/table/tbody/tr/td/input[@data-staffname="'
    approve_staff_select_btn_ele = (By.ID,'staffDialogSubmitBtn')
    

    def require_approve_click(self):
        self.select_by_value(self.require_approve_ele,'1')
    
    def require_approve_staff(self):
        self.move_to_element_click(self.approve_staff_ele)
        self.cover_is_display()

    def approve_staff_search(self,staff_name):
        self.send_keys(self.approve_staff_search_ele,staff_name)
    
    def approve_staff_search_click(self):
        self.move_to_element_click(self.approve_staff_search_btn_ele)
        self.cover_is_display()

    staffTable = (By.XPATH,'//table[@id="staffTable"]/tbody/tr/td[2]')
    def approve_staff_select_click(self,staff_name):
        # ele = (By.XPATH,self.approve_staff_select_ele + staff_name + '"]')#员工姓名
        staffs = self.get_eles_text(self.staffTable)
        i = 0
        for staff in staffs:
            i = i + 1
            if staff_name == staff:
                break
        ele = (By.XPATH,'//table[@id="staffTable"]/tbody/tr['+str(i)+']/td[1]/input')         
        self.move_to_element_click(ele)

    def approve_staff_select_btn_click(self):
        self.move_to_element_click(self.approve_staff_select_btn_ele)
    

    

    #失效时间
    invalid_time_ele = (By.ID,'invalidTime')
    def invalid_time_click(self):
        self.move_to_element_click(self.invalid_time_ele)

    invalid_time_ele_1 = '//li[@value="'
    def invalid_time_value_click(self,value):
        ele = (By.XPATH,self.invalid_time_ele_1 + value + '"]')
        self.move_to_element_click(ele)

    invalid_time_ele_date = (By.XPATH,'//li[@class="date_picker"]')
    def invalid_time_date_click(self,value):       
        self.move_to_element_click(self.invalid_time_ele_date)
        self.change_YYYYMMDD(value)

    
    #----------------年月日格式选日期---------------
    def change_year(self,yy):
        #切换年份
        ele_year = (By.XPATH,'//em[@class="jedateyear"]')
        ele_yy = (By.XPATH,'//li[@yy="'+yy+'"]')
        self.click(ele_year)
        self.click(ele_yy)
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
    #----------------年月日格式选日期---------------


    #是否拆分
    not_split_ele = (By.XPATH,'//input[@value="0"]')
    split_ele = (By.XPATH,'//input[@value="1"]')
    split_field_ele = '//label[@class="radio-inline"]/input[@value="'

    def split_not_click(self):
        self.click(self.not_split_ele)
        self.cover_is_display()
    
    def split_click(self):
        self.click(self.split_ele)
        self.cover_is_display()
    
    def split_field_click(self,value):
        ele = (By.XPATH,self.split_field_ele + value + '"]')
        self.click(ele)
        self.cover_is_display()
    
    #查询用户，并拖拽
    split_module_tile = (By.XPATH,'//table/thead/tr[@class="table_title"]/td[@class="split-module-title"]')
    split_way_str = '//table/tbody/tr/td/span[@class="capsule capsule-red"]'
    depart_trees_str = '//div[@id="staffTree"]/li'
    def staff_drag(self,splitWay,staff_no,is_split):
        
        id = ''
        departs = self.find_elements((By.XPATH,self.depart_trees_str))
        for i in range(1,len(departs)+1):
            if self.is_display_no_wait((By.XPATH,self.depart_trees_str+'['+str(i)+']')) == True:
                staff_trees_str = self.depart_trees_str+'['+str(i)+']/ul/li'
                staffs = self.find_elements((By.XPATH,staff_trees_str))
                for j in range(1,len(staffs)+1):
                    if self.is_display_no_wait((By.XPATH,staff_trees_str+'['+str(j)+']')) == True:
                        if staff_no == self.get_text((By.XPATH,staff_trees_str+'['+str(j)+']/a/span[2]')):
                            id = self.find_element_attr((By.XPATH,staff_trees_str+'['+str(j)+']/a/span[2]'),'id')[0]
                            break
        split_all = self.get_eles_text((By.XPATH,self.split_way_str))
        if is_split == '是': 
            if id != '':
                i = 0
                for split in split_all:
                    i = i + 1
                    if splitWay in split and '全部' in split:
                        self.drag_drop((By.ID,id),self.split_module_tile)
                    elif split == splitWay:
                        time.sleep(0.2)
                        self.drag_drop((By.ID,id),(By.XPATH,'//table/tbody/tr['+str(i)+']/td[2]'))
                        time.sleep(0.2)
        else:
            if id != '':
                i = 0
                for split in split_all:
                    i = i + 1
                    if splitWay in split and '不拆分' in split:
                        self.drag_drop((By.ID,id),self.split_module_tile)
                    
                    
                    
    #员工查询
    staff_search_ele = (By.XPATH,'//input[@class="search_input"]')
    def search_staff(self,*staff):
        self.clear(self.staff_search_ele)
        if staff is None:
            self.send_keys(self.staff_search_ele,self.staff_no)
        else:
            self.send_keys(self.staff_search_ele,staff)
    
    
    #添加查看清单人员
    staff_name_ele = '.split-module-td'
    def staff_add(self,staff_add):
        staff_name_add_ele = "<span class='capsule capsule-green' data-staffid='"+ str(staff_add[0][0]) +"' data-staffname='"+ staff_add[0][2] +"'>"+ staff_add[0][2] +"<i>×</i></span>"
        staff_name_add_ele = ' '.join(staff_name_add_ele.split('\xa0'))
        self.add_child_ele(self.staff_name_ele,staff_name_add_ele)


    list_name_str = '//table[@id="result_table"]/tbody/tr'
    list_name_search_id = 'listName'
    search_id = 'queryFormSubmit'
    def get_list_names(self,lists):
        list_result = []
        
        for li in lists:
            self.clear((By.ID,self.list_name_search_id))
            self.send_keys((By.ID,self.list_name_search_id),li)
            self.move_to_element_click((By.ID,self.search_id))
            self.cover_is_display()
            list_ele = (By.XPATH,self.list_name_str+'/td[1]')
            if self.ele_is_exist(list_ele):
                listnames = self.get_eles_text(list_ele)
                i = 0 
                for listname in listnames:
                    if listname == li:
                        split_result = self.get_eles_text((By.XPATH,self.list_name_str+'/td[5]'))
                        is_cycle = self.get_eles_text((By.XPATH,self.list_name_str+'/td[4]'))
                        j = 0
                        while split_result == '拆分处理中' and j < 30:
                            j = j + 1
                            time.sleep(5)
                        list_result.append({'listName':listname,'listCycle':is_cycle[i],'listResult':split_result[i]})
                    i = i + 1
        return list_result



    def get_list_names_download(self,lists):
        list_result = []
        for li in lists:
            self.clear((By.ID,self.list_name_search_id))
            self.send_keys((By.ID,self.list_name_search_id),li)
            self.move_to_element_click((By.ID,self.search_id))
            self.cover_is_display()
            list_ele = (By.XPATH,self.list_name_str+'/td[1]')
            if self.ele_is_exist(list_ele):
                listnames = self.get_eles_text(list_ele)
                i = 0 
                for listname in listnames:
                    if listname == li:
                        expires_time = self.get_eles_text((By.XPATH,self.list_name_str+'/td[8]'))
                        now_time = datetime.datetime.now().strftime('%Y%m%d')
                        result = False
                        if datetime.datetime.strptime(expires_time[0],'%Y-%m-%d').strftime('%Y%m%d') >= now_time: 
                            result = True
                            self.move_to_element_click((By.XPATH,self.list_name_str+'['+str(i+1)+']/td[10]/div/a'))
                            time.sleep(3)
                        list_result.append({'listName':listname,'result':result})
                    i = i + 1
        return list_result


                

    submit_btn_ele = (By.ID,'listSubmit')
    def submit_click(self):
        self.move_to_element_click(self.submit_btn_ele)
        self.cover_is_display()

    alert = (By.CLASS_NAME,'zMsg_alert_new')
    sub = (By.XPATH,'//div[@class="zMsg_alert_new"]/table/tfoot/tr/td/button')
    def alert_btn_click(self):
        if True == self.is_exist(self.alert):
            self.move_to_element_click(self.sub)
            self.cover_is_display()
    
    tip = (By.XPATH,'//td[@class="tip"]')
    def alert_tip(self):
        if True == self.is_exist(self.alert):
            return self.get_text(self.tip)


    replace_type = '//*[@name="replaceType"]'
    replace_result = '//*[@id="replaceResult"]'
    def replace_acctmonth(self,replaceType,*replaceTime):
        eles = self.find_elements((By.XPATH,self.replace_type))
        if replaceType=='all':
            eles[0].click()
        elif replaceType=='reality':
            eles[1].click()
        elif replaceType=='Manual':
            eles[2].click()
            replace_times = '//div[@id="manualResult"]/input'
            eles_time = self.find_elements((By.XPATH,replace_times))
            l = len(eles_time)
            i,j = 2,0
            for i in range(2,l+1):
                replace_time = replace_times+'['+str(i)+']'
                self.send_keys((By.XPATH,replace_time),replaceTime[j])
                i = i+2
                j = j+1

        while '${' in self.find_element_value((By.XPATH,self.replace_result)):
            time.sleep(1)

        return 'success'

    replace_click = (By.ID,'sqlVariableDialogSubmitBtn')
    def replace_acctmonth_sure_click(self):
        self.move_to_element_click(self.replace_click)


    cover = (By.XPATH,'//body/div[@class="zMsg_cover cover_body"]')
    def cover_is_display(self):
        i = 0 
        while self.is_display(self.cover) == True and i < 30 :
            i = i + 1 
            time.sleep(3)





    


    



    

