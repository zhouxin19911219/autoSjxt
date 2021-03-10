# /usr/bin/python
# coding = utf-8

from selenium.webdriver.common.by import By
from pages.basePage import Page
import datetime  
import time
import os

class AnalyPage(Page):


    #获取数据源id
    label_source = (By.ID,'cptList')
    def get_label_source(self):
        return self.find_element_value(self.label_source)

    #切换数据源
    def label_source_select(self,text):
        self.select_by_text(self.label_source,text)
    #==========================================已传已存==========================================================
    #切换已存已传
    label_group = (By.ID,'dataSource')
    def label_group_select(self,text):
        self.select_by_text(self.label_group,text)
        self.cover_is_display()

    #选择已传数据群
    uploaded_users_ele_str = '//div[@id="dialog_groupUsers"]/div/div/table/tbody[@id="groupUserTab"]/tr'

    #勾选关联和剔除查询
    uploaded_users_ele = (By.XPATH,uploaded_users_ele_str)
    def uploaded_users_click(self,texts):
        upload_users = self.find_elements(self.uploaded_users_ele)
        l = len(upload_users)
        inner = True
        tichu = True
        for i in range(0,l):
            ele = (By.XPATH,self.uploaded_users_ele_str+'['+str(i+1)+']')
            for text in texts:
                if (self.text_is_exist_no_wait(ele,text) == True ) and (inner == True or tichu == True):
                    if '关联查询' == self.get_text((By.XPATH,self.uploaded_users_ele_str+'['+str(i+1)+']/td[5]')) and inner == True:
                        inner = False
                        ele1 = (By.XPATH,self.uploaded_users_ele_str+'['+str(i+1)+']/td[1]/input')
                        if False == self.ele_is_selected(ele1):
                            self.click(ele1)

                    elif '剔除查询' == self.get_text((By.XPATH,self.uploaded_users_ele_str+'['+str(i+1)+']/td[5]')) and tichu == True:
                        tichu = False
                        ele1 = (By.XPATH,self.uploaded_users_ele_str+'['+str(i+1)+']/td[1]/input')
                        if False == self.ele_is_selected(ele1):
                            self.click(ele1)

                elif inner != True and tichu != True:
                    break
        return 'success'

    #弹框确定按钮
    uploaded_users_btn = (By.ID,'selectGroupBtn')
    def uploaded_user_btn_click(self):
        self.move_to_element_click(self.uploaded_users_btn)

    
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
    #点击已存用户确定按钮
    saved_user_btn_ele = (By.ID,'selectSaveGroupBtn')
    def saved_user_btn_click(self):
        self.move_to_element_click(self.saved_user_btn_ele)

    #==========================================已传==========================================================


    #=======================================账期===========================================
    acctMonth_selected = (By.XPATH,'//div[@class="swiper-wrapper"]/b')
    def get_acctMonth_selected(self):
        if self.is_exist_no_wait(self.acctMonth_selected) :
            result = self.get_eles_text(self.acctMonth_selected)
            return result[0]
        else:
            return ''


    def cancel_acct_month(self,*acctMonth):
        elements = self.find_elements(self.acctMonth_selected)
         #没传账期过来
        if acctMonth == ():
            for i in range(1,len(elements)+1):
                self.move_to_element_click((By.XPATH,'//div[@class="swiper-wrapper"]/b['+str(i)+']/small'))
        else:
            for i in range(1,len(elements)+1):
                if acctMonth in elements[i-1].text():
                   self.move_to_element_click((By.XPATH,'//div[@class="swiper-wrapper"]/b['+str(i)+']/small'))



    acctMonth_select = (By.XPATH,'//span[@class="swiper-notification"]')
    def select_acctMonth(self,acctMonth):
        time.sleep(0.5)
        self.move_to_element_click(self.acctMonth_select)
        label_formate = 'YYYYMM'
        if len(acctMonth) == 8:
            label_formate = 'YYYYMMDD'
        self.time_input(label_formate,acctMonth)

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

    #========================================账期==========================================
    #-----------弹框提示----------
    alert = (By.CLASS_NAME,'zMsg_alert_new')
    sub = (By.XPATH,'//div[@class="zMsg_alert_new"]/table/tfoot/tr/td/button')

    def alert_is_exist(self):
        return self.is_exist(self.alert)

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
    #====================================================

  
        
    #枚举值作为维度点击
    def enum_dimdic_click(self):
        self.as_dimdic_click('作为维度')
        self.cover_is_display()
        self.dimdic_alert_btn_click()
    #枚举值作为指标-计数点击
    def enum_dimdicCount_click(self):
        self.as_dimdic_click('作为指标-计数')
        self.cover_is_display()
        self.dimdic_alert_btn_click()
    page_count = (By.XPATH,'//div[@id="dimdicTree"]/li/a')
    select_input_search = (By.ID,'dimdicSelectInput')
    search_input_btn = (By.ID,'dimdicSearchBtn')
    #判断是否分页，并进行点击
    def page_label_click(self,labelValue,page_count):
        #超过一页进行查询后再点击
        if int(page_count) > 1:         
            for label in labelValue:
                self.send_keys(self.select_input_search,label)
                self.move_to_element_click(self.search_input_btn)
                
                time.sleep(0.5)
                self.label_value_check_click(label)     
                self.clear(self.select_input_search)
                self.move_to_element_click(self.search_input_btn)
        else:
            for label in labelValue:
                self.label_value_check_click(label) 

    def label_value_check_click(self,labelValue):
        value_id_a = self.find_element_attr((By.LINK_TEXT,labelValue),'id')[0]
        value_id_check = value_id_a.replace('_a','_check')
        self.move_to_element_click((By.ID,value_id_check))

    #枚举值作为条件点击
    def enum_condition_click(self,labelValue):
        self.as_dimdic_click('作为条件')
        self.cover_is_display()
        title = self.find_element_attr(self.page_count,'title')
        page_count = title[0].split('共')[1].replace(' ','')[0:-1]
        self.page_label_click(labelValue,page_count)
        self.dimdic_alert_btn_click()   
    #枚举值作为维度编组点击
    def enum_dimdicGroup_click(self,labelGroup,labelValue,labelDel):
        self.as_dimdic_click('作为维度-编组')
        self.cover_is_display()
        title = self.find_element_attr(self.page_count,'title')
        page_count = title[0].split('共')[1].replace(' ','')[0:-1]
        i = 0
        for labels in labelValue:
            #点击每组标签值
            self.page_label_click(labels,page_count)
            i = i+1       
            self.label_group_click()
            self.label_group_hover(i-1)
            self.label_groupName_sendkeys(i,labelGroup[i-1])
            if labelDel in labels:
                self.label_delete_click(i,labelDel)
            self.label_groupName_click(i)

        self.dimdic_alert_btn_click()
    #sql查询跳转自助报表:枚举值作为维度编组点击
    def enum_dimdicGroup_sqlSearch_click(self,labelGroup,labelValue,labelDel):
        self.as_dimdic_click('作为维度-编组')
        self.cover_is_display()
        i = 0
        for labels in labelValue:
            #点击每组标签值
            self.page_label_click(labels,'1')
            i = i+1       
            self.label_group_click()
            self.label_group_hover(i-1)
            self.label_groupName_sendkeys(i,labelGroup[i-1])
            if labelDel in labels:
                self.label_delete_click(i,labelDel)
            self.label_groupName_click(i)

        self.dimdic_alert_btn_click()

    #数值作为指标
    def num_quotaCalculate_click(self,labelCal):
        self.as_quota_click('作为指标')
        for quota in labelCal:
            self.quota_calculate_click(quota)
        self.quota_alert_btn_click()

    #数值作为维度/步长分组
    def num_quotaStep_click(self,quotaStep):
        self.as_quota_click('作为维度','步长分组')
        self.quota_group_step_sendkeys(quotaStep)
        
    #数值作为维度/选点分组
    def num_quotaPoint_click(self,quotaPoint):
        self.as_quota_click('作为维度','选点分组')
        self.quota_group_point_sendkeys(quotaPoint)

    #数据作为条件
    def num_quotaCondition_click(self,labelValue):
        self.as_quota_click('作为条件')
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
        



    def time_quotaYM_click(self,text):
        self.as_time_quota_click('按年/月分组')
        self.quota_group_YM_click(text)


    # #时间类型查询
    # def date_quotaCondition_click(self,labelValue):
    #     if labelValue[0] !='' :
    #         self.input_time_start_info(labelValue[0])
    #     if len(labelValue)>1 and labelValue[1] !='':
    #         self.input_time_end_info(labelValue[1])

    #=========================================================

    #标签名称搜索
    def label_search(self,labelName):
        self.label_search_clear()
        self.label_search_click(labelName)


    search_ele = (By.XPATH,'//input[@placeholder="搜索"]')
    def label_search_clear(self):
        self.clear(self.search_ele)
        #clear清除后没有返回所有结果，下方又重新输入一个字节a，再模拟键盘删除，结果返回
        self.send_keys(self.search_ele,'a')
        self.keys_clear(self.search_ele)

    def label_search_click(self,value):
        time.sleep(0.5)
        self.move_to_element_click(self.search_ele)
        self.send_keys(self.search_ele,value)
        time.sleep(0.5)

    #点击标签上级目录
          
    def file_click(self,labelFile):
        self.label_search_clear()
        time.sleep(0.5)
        for f in labelFile:
            self.label_file_click(f)
        time.sleep(1)

    def label_file_click(self,labelfile):
        #判断文件夹是否打开
        ele = (By.LINK_TEXT,labelfile)
        ids = self.find_element_attr(ele,'id')
        ele_span = (By.XPATH,'//*[@id="'+ ids[0] +'"]/span[1]')
        classes = self.find_element_attr(ele_span,'class')
        if 'ico_open' not in classes[0]:
            self.click((By.LINK_TEXT,labelfile))

    #维度弹框，作为维度/作为维度分组/作为条件/作为指标 按钮点击    
    def as_dimdic_click(self,text):
        i = 0
        if '作为维度' == text:
            i = 1
        elif '作为维度-编组' == text:
            i = 2
        elif '作为条件' == text:
            i = 3
        elif '作为指标-计数' == text:
            i = 4
        as_dimdic = (By.XPATH,'//div[@id="dialog_dimdic"]/div/div/div/span['+str(i)+']')
        if self.find_element_attr(as_dimdic,'class') != 'active' :
            self.move_to_element_click(as_dimdic)
    
    #弹框确定按钮
    dimdic_alert = (By.ID,'saveDimCodeBtn')
    def dimdic_alert_btn_click(self):
        self.move_to_element_click(self.dimdic_alert)
        self.cover_is_display()

    #点击标签
    def label_value_click(self,value):
        label = (By.LINK_TEXT,value)
        self.move_to_element_click(label)
        if self.cover_is_display() == True:
            result = True
        else:
            result = False
        return result


    #点击编组按钮
    label_group_btn = (By.ID,'addDicGroupBtn')
    def label_group_click(self):
        self.click(self.label_group_btn)

    #编组命名
    def label_group_hover(self,i):
        # group = (By.XPATH,'//div[@class="group_list"]/div['+str(i)+']')
        group = '$(".group_list>div>div.group_detail").eq('+str(i)+')'
        self.ele_show(group)

    def label_groupName_sendkeys(self,i,text):
        group = (By.XPATH,'//div[@class="group_list"]/div['+str(i)+']/div/div[@class="detail_form"]/input')
        self.send_keys(group,text)

    def label_groupName_click(self,i):
        group_btn = (By.XPATH,'//div[@class="group_list"]/div['+str(i)+']/div/div[@class="detail_form"]/button')
        self.click(group_btn)

    #删除组内元素
    def label_delete_click(self,i,del_text):
        group_dels = (By.XPATH,'//div[@class="group_list"]/div['+str(i)+']/div/div[@class="group_items"]/b')
        # self.add_ele_display('$(".group_detail")['+str(i-1)+']','block')
        self.ele_show('$(".group_detail").eq('+str(i-1)+')')
        j = 0
        for ele in self.get_eles_text(group_dels):
            j = j+1
            if del_text == ele :
                group_del = (By.XPATH,'//div[@class="group_list"]/div['+str(i)+']/div/div[@class="group_items"]/b['+str(j)+']/small')
                self.click(group_del)
    
    #提交查询
    search_btn = (By.ID,'submitBtn')
    def search_btn_click(self):
        time.sleep(0.5)
        self.move_to_element_click(self.search_btn)
        self.cover_is_display()

    #切换作为指标/维度/作为条件，group是选择维度时，传递步长/选点分组
    def as_quota_click(self,text,*group):
        i = 0
        if "作为指标" == text:
            i = 1
        elif "作为维度" == text:
            i = 2
        elif "作为条件" == text:
            i = 3
        ele = (By.XPATH,'//div[@id="dialog_quota"]/div/div[@class="panel_body"]/div/span['+str(i)+']')
        self.click(ele)
        if len(group) > 0:
            ele_group = '$(".tag_tab>ul")[0]'
            # self.add_ele_display(ele_group,'block')
            self.ele_show('$(".tag_tab>ul")')
            if "步长分组" == group[0]:
                ele = (By.XPATH,'//div[@class="panel_body"]/div/ul/li[1]')
                self.click(ele)
            elif "选点分组" == group[0]:
                ele = (By.XPATH,'//div[@class="panel_body"]/div/ul/li[2]')
                self.click(ele)
            # self.add_ele_display(ele_group,'none')
            self.ele_hide('$(".tag_tab>ul")')

        

    #指标取和/平均值/最大数点击   
    def quota_calculate_click(self,text):
        ele = 'sum'
        if "求和" in text:
            ele = "sum"
        elif "平均数" in text:
            ele = "average"
        elif "最大值" in text:
            ele = "max"
        elif "最小值" in text:
            ele = "min"
        elif "中位数" in text:  
            ele = "median"
        quota_calculate = (By.XPATH,'//div[@class="panel_body"]/div/div/div/label[@for="'+ele+'"]/input')
        if False == self.ele_is_selected(quota_calculate):
            self.click(quota_calculate)


    #指标弹框按钮
    quota_alert_btn = (By.XPATH,'//div[@id="dialog_quota"]/div/div[@class="my_btns"]/input')
    def quota_alert_btn_click(self):
        self.click(self.quota_alert_btn)
        self.cover_is_display()



    #步长分组
    quota_group_step = (By.XPATH,'//div[@class="panel_body"]/div/ul/li/input')
    quota_group_step_result = (By.XPATH,'//div[@class="panel_body"]/div[@class="filter_form step_len_form"]/ul/li/b')
    def quota_group_step_sendkeys(self,step):
        self.send_keys(self.quota_group_step,step)
        #等待分组结果
        self.text_is_exist(self.quota_group_step_result,'...')
        # self.get_text(self.quota_group_step_result)
    
    
    #忽略空值
    quota_stepNULL =  (By.XPATH,'//div[@class="panel_body"]/div[@class="filter_form step_len_form"]/ul/li/label/input')
    def quota_stepNULL_click(self):
        self.click(self.quota_stepNULL)    

    #选点分组
    quota_add_point = (By.CLASS_NAME,'add_point')
    quota_group_point_result = (By.XPATH,'//div[@class="panel_body"]/div[@class="filter_form check_point_form"]/ul/li/b')
    def quota_group_point_sendkeys(self,point):
        i = 0
        for p in point:
            i = i + 1
            quota_group_point = (By.XPATH,'//div[@class="point_list"]/small['+str(i)+']/input')
            self.send_keys(quota_group_point,p)
            self.text_is_exist(self.quota_group_point_result,'∞')
            self.click(self.quota_add_point)
        
            
    #忽略空值
    quota_pointNULL =  (By.XPATH,'//div[@class="panel_body"]/div[@class="filter_form check_point_form"]/ul/li/label/input')
    def quota_pointNULL_click(self):
        self.click(self.quota_pointNULL)


    #数据类型输入
    start_ele = (By.ID,'startVal')
    end_ele = (By.ID,'endVal')
    middle_flag_ele = (By.ID,'middleFlag')
    end_Sign_ele = (By.ID,'endSign')
    start_Sign_ele = (By.ID,'startSign')
    def input_Tmonth_start_info(self,startVal):
        self.send_keys(self.start_ele,startVal)
    def middle_flag_select(self,middle_flag):
        self.select_by_value(self.middle_flag_ele,middle_flag)
    def end_sign_select(self,end_sign):
        self.select_by_value(self.end_Sign_ele,end_sign)
    def start_sign_select(self,startSign):
        self.select_by_value(self.start_Sign_ele,startSign)
    def input_Tmonth_end_info(self,endVal):
        self.send_keys(self.end_ele,endVal)


    #按年月分组
    def quota_group_YM_click(self,text):

        if text in '按年':
            ele = (By.ID,'year')
            self.click(ele)
        elif text in '按月':
            ele = (By.ID,'month')
            self.click(ele)

    #切换按年月分组/选点分组/作为条件
    def as_time_quota_click(self,text):
        i = 0
        if text in "按年/月分组":
            i = 1
        elif "选点分组" == text:
            i = 2
        elif "作为条件" == text:
            i = 3
        ele = (By.XPATH,'//div[@id="dialog_date"]/div/div[@class="panel_body"]/div/span['+str(i)+']')
        self.click(ele)
        time.sleep(0.5)
    #时间指标弹框按钮
    quota_time_alert_btn = (By.XPATH,'//div[@id="dialog_date"]/div/div[@class="my_btns"]/input')
    def quota_time_alert_btn_click(self):
        self.click(self.quota_time_alert_btn)
        self.cover_is_display()

    #时间选点分组
    quota_time_add_point = (By.XPATH,'//*[@id="dialog_date"]/div/div/div[@class="filter_form time_group_form"]/ul/li[1]/i')
    quota_time_group_point_result = (By.XPATH,'//*[@id="dialog_date"]/div/div/div[@class="filter_form time_group_form"]/ul/li/b')
    def quota_group_time_point_sendkeys(self,time_format,point):        
        for p in point:
            self.click(self.quota_time_add_point)
            self.time_input(time_format,p)
            self.text_is_exist(self.quota_time_group_point_result,'∞')


    #忽略空值
    ignore_Null = (By.XPATH,'//div[@class="panel_body"]/div[@class="filter_form time_group_form"]/ul/li/label/input')
    def quota_time_ignore_null(self):
        self.click(self.ignore_Null)

    #=========================时间选择框点击==========================
    
    def time_click(self,dateFormate,values):
        if values[0]!='':
            self.input_time_start_info(dateFormate,values[0])
        if len(values) == 2 and values[1]!='':
            self.input_time_end_info(dateFormate,values[1])


    #时间类型输入
    time_start_ele = (By.ID,'timeConditionStart')
    time_end_ele = (By.ID,'timeConditionEnd')
    def input_time_start_info(self,label_formate,startTime):
        self.click(self.time_start_ele)
        self.time_input(label_formate,startTime)
    def input_time_end_info(self,label_formate,endTime):
        self.click(self.time_end_ele)
        self.time_input(label_formate,endTime)


    #==================获取结果表格表头===============================
    table_title = (By.XPATH,'//div[@id="results"]/table/tbody/tr[@class="table-title"]/td')
    table_head = (By.XPATH,'//div[@id="results"]/table/thead/tr[@class="table-title"]/td')
    def get_table_title(self):
        if self.is_exist_no_wait(self.table_title):
            return self.get_eles_text(self.table_title)
        else:
            return self.get_eles_text(self.table_head)

    table_tr = '//div[@id="results"]/table/tbody/tr'
    def get_table_content(self,length):
        if self.is_exist_no_wait((By.XPATH,self.table_tr+'[1]')):
            for i in range(0,length):
                elements = self.find_elements((By.XPATH,self.table_tr))
                for j in range(1,len(elements)):
                    if self.is_exist_no_wait((By.XPATH,self.table_tr+'['+str(j)+'][@class="table-title"]')) == False:
                        table_td = self.table_tr+'['+str(j)+']/td[1]/a'
                        if self.is_exist_no_wait((By.XPATH,table_td)):
                            self.move_to_element_click((By.XPATH,table_td))
                            self.cover_is_display()
                            break
                        else:
                            self.return_first_level()
                            self.cover_is_display()
                            break                        
                    

    breadcrumb_li = (By.XPATH,'//ol[@id="breadcrumb"]/li')
    def return_before_level(self):
        eles = self.find_elements(self.breadcrumb_li)
        before_level = (By.XPATH,'//ol[@id="breadcrumb"]/li['+str(len(eles)-1)+']/a')
        self.move_to_element_click(before_level)

    def return_first_level(self):
        before_level = (By.XPATH,'//ol[@id="breadcrumb"]/li[1]/a')
        self.click(before_level)

    breadcrumb = (By.ID,'breadcrumb')
    def breadcrumb_is_show(self):
        return self.is_display(self.breadcrumb)
            
        
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



    #====================保存模板================================
    template_save = (By.ID,'templateSaveBtn')
    def template_save_btn_click(self):
        self.move_to_element_click(self.template_save)

    filter_name = (By.ID,'rcptName')
    filter_remark = (By.ID,'rcptDesc')
    filter_type= '//*[@id="dialog_saveRcpt"]/div/div[1]/div[2]/div/div'
    filter_staff_search = (By.ID,'staffDialogSearchInput')
    filter_staff_search_click = (By.ID,'staffDialogSearchBtn')
    filter_staff = '//*[@id="staffTable"]/tbody/tr'

    def save_filter_info(self,name,type,remark,*staffs):
        self.send_keys(self.filter_name,name+datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        self.send_keys(self.filter_remark,remark+datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        if '我的' == type :
            # ele = (By.XPATH,self.filter_type+'/label[@for="filterType04"]/input[@value="04"]')
            ele = (By.ID,'filterType04')
            self.move_to_element_click(ele)
        elif '公共' == type :
            # ele = (By.XPATH,self.filter_type+'/label[@for="filterType05"]/input[@value="05"]')
            ele = (By.ID,'filterType05')
            self.move_to_element_click(ele)
        elif '分享' == type :
            # ele = (By.XPATH,self.filter_type+'/label[@for="filterType06"]/input[@value="06"]')
            ele = (By.ID,'filterType06')
            self.move_to_element_click(ele)
            self.cover_is_display()
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


    filter_btn_ele = (By.ID,'saveRcptBtn')
    def filter_btn_click(self):
        self.move_to_element_click(self.filter_btn_ele)
        self.cover_is_display()

#===========================================下载=================================================================

    charts = (By.XPATH,'//div[@class="right_box"]/div[2]/div[@class="section-title"]/div[@class="charts-check"]/span')
    download = (By.XPATH,'//div[@class="right_box"]/div[2]/div[@class="section-title"]/div[@class="charts-check"]/div/dl/dt/a')
    def download_data(self):
        self.move_to_element_and_click_element(self.charts,self.download)
        self.cover_is_display()

#===========================================模板===================================================================

    filter = (By.XPATH,'//div[@class="collapse-panel"]/ul/li[2]/h3/span')
    def filter_user_click(self):
        
        cover = (By.XPATH,'//div[@class="collapse-panel"]/ul/li[2]/div')
        self.move_to_element_click(self.filter)
        if self.is_display(cover) == False:
            time.sleep(2)
        # self.cover_is_display()

    self_search = (By.XPATH,'//div[@class="collapse-panel"]/ul/li[1]/h3/span')
    def self_search_click(self):
        cover = (By.XPATH,'//div[@class="collapse-panel"]/ul/li[1]/div')
        if self.is_display(cover) == True:
            time.sleep(2)
        self.move_to_element_click(self.self_search)
        self.cover_is_display()
    
    filter_type = '//div[@class="collapse-panel"]/ul/li[2]/div/div/div[@id="labelFilterTab"]/button'
    def filter_type_click(self,filter_type):
        ele = self.filter_type
        if filter_type == '我的':
            ele = ele + '[@value="04"]'
        elif filter_type == '分享':
            ele = ele + '[@value="06"]'
        elif filter_type == '公共':
            ele = ele + '[@value="05"]'
        ele_click = (By.XPATH,ele)
        self.click(ele_click)
        self.cover_is_display()

    self_module = (By.XPATH,'//div[@class="list-panel self-module"]')
    def filter_click(self,filter_type,name):
        if self.is_display_no_wait(self.self_module) == False:
            time.sleep(2)
        self.filter_type_click(filter_type)
        time.sleep(0.5)
        ele_str = '//dl[@id="rcptList"]/dd'
        sourceId = ''
        if self.is_exist_no_wait((By.XPATH,ele_str))==True:   
            texts = self.get_eles_text((By.XPATH,ele_str))
            l = len(texts)
            i = 0
            while i < l :
                if (name[0] in texts[i]) :
                    self.move_to_element_click((By.XPATH,ele_str+'['+str(i+1)+']/span'))
                    sourceId = self.find_element_attr((By.XPATH,ele_str+'['+str(i+1)+']/span'),'labsource')[0]
                    self.cover_is_display()
                    break
                i = i + 1
        return sourceId

    def delete_filter(self,filter_type,names):
        self.filter_type_click(filter_type)
        time.sleep(0.5)

        ele = '//dl[@id="rcptList"]/dd'
        if self.is_exist_no_wait((By.XPATH,ele))==True:   
            texts = self.get_eles_text((By.XPATH,ele))
            l = len(texts)
            i = 0
            j = 0
            while j < l :
                for name in names:
                    if (name in texts[j]) :
                        self.move_to_element_click((By.XPATH,ele+'['+str(i+1)+']/span'))
                        self.cover_is_display()
                        text = self.get_text((By.XPATH,ele+'['+str(i+1)+']'))
                        if ('×' in text) :
                            ele_colse = (By.XPATH,ele+'['+str(i+1)+']/i')
                            self.move_to_element_click(ele_colse)
                            time.sleep(0.5)
                            self.alert_sure_btn_click('确 定')
                            self.cover_is_display()
                            self.alert_sure_btn_click('确 定')
                            l = l-1
                        else:
                            i = i+1
                    else:     
                        i = i+1
                j = j + 1

        return True

#==================================层级===============================================

    
    def label_drag_drop(self,labelName):
        drag = (By.LINK_TEXT,labelName)
        drop = (By.XPATH,'//div[@id="drillDims"]')
        self.drag_drop(drag,drop)


    #-----------点击关闭05标签的下钻图层---------------
    type5 = (By.XPATH,'//div[@class="type5tree-wrap"]')
    type5_close = (By.XPATH,'//div[@class="type5tree-wrap"]/i')
    def close_type5(self):
        if True == self.is_display_no_wait(self.type5):
            self.move_to_element_click(self.type5_close)

#===============================条件===================================

    #having条件数据类型输入
    start_having_ele = (By.XPATH,'//*[@id="dialog_having"]/div/div[1]/div/input[@id="startVal"]')
    end_having_ele = (By.XPATH,'//*[@id="dialog_having"]/div/div[1]/div/input[@id="endVal"]')
    middle_flag_having_ele = (By.XPATH,'//*[@id="dialog_having"]/div/div[1]/div/select[@id="middleFlag"]')
    end_Sign_having_ele = (By.XPATH,'//*[@id="dialog_having"]/div/div[1]/div/select[@id="endSign"]')
    start_Sign_having_ele = (By.XPATH,'//*[@id="dialog_having"]/div/div[1]/div/select[@id="startSign"]')
    def input_Tmonth_start_info_having(self,startVal):
        self.send_keys(self.start_having_ele,startVal)

    def middle_flag_having_select(self,middle_flag):
        self.select_by_value(self.middle_flag_having_ele,middle_flag)

    def end_sign_having_select(self,end_sign):
        self.select_by_value(self.end_Sign_having_ele,end_sign)

    def start_sign_having_select(self,startSign):
        self.select_by_value(self.start_Sign_having_ele,startSign)

    def input_Tmonth_end_info_having(self,endVal):
        self.send_keys(self.end_having_ele,endVal)
   
    addHaving = (By.ID,'addHaving')
    havingSelect = (By.ID,'havingSelect')
    dialog_having_cover = (By.ID,'dialog_having')
    #点击条件进行筛选
    def condition_filter_click(self,labelName,labelValue):
        self.move_to_element_click(self.addHaving)
        if self.is_display(self.dialog_having_cover) == False:
            time.sleep(2)
        havings = self.get_eles_text(self.havingSelect)[0].split('\n')
        for having in havings:
            if labelName in having:
                self.select_by_value(self.havingSelect,having)
        time.sleep(1)
        
        if labelValue[0] == '' :
            self.start_sign_having_select('>')
        else :
            self.start_sign_having_select(labelValue[0])

        if len(labelValue) > 1:
            self.input_Tmonth_start_info_having(labelValue[1])
        if len(labelValue) > 2:
            self.middle_flag_having_select(labelValue[2])
        if len(labelValue) > 3:
            self.end_sign_having_select(labelValue[3])
        if len(labelValue) > 4:
            self.input_Tmonth_end_info_having(labelValue[4])
        time.sleep(1)

    dialogHavingBtn = (By.ID,'dialogHavingBtn')
    def quota_having_btn_click(self):
        self.move_to_element_click(self.dialogHavingBtn)
        if self.is_display(self.dialog_having_cover) == True:
            time.sleep(2)



#================================sql查询跳转到自助报表================================================
    dialog_dimdic = (By.ID,'dialog_dimdic')
    changeTypeBtn4Dim = (By.ID,'changeTypeBtn4Dim')
    dialog_quota = (By.ID,'dialog_quota')
    changeTypeBtn4Quota = (By.ID,'changeTypeBtn4Quota')
    dialog_date = (By.ID,'dialog_date')
    changeTypeBtn4Time = (By.ID,'changeTypeBtn4Time')
    def to_dimdic(self):
        if self.is_display(self.dialog_dimdic) == False:
            if self.is_display(self.dialog_quota) == True:
                self.move_to_element_click(self.changeTypeBtn4Quota)
                self.select_label_type((By.ID,'columnTypeDim'))
            elif self.is_display(self.dialog_date) == True:
                self.move_to_element_click(self.changeTypeBtn4Time)
                self.select_label_type((By.ID,'columnTypeDim'))
    def to_quota(self):
        if self.is_display(self.dialog_quota) == False:
            if self.is_display(self.dialog_dimdic) == True:
                self.move_to_element_click(self.changeTypeBtn4Dim)
                self.select_label_type((By.ID,'columnTypeQuota'))
            elif self.is_display(self.dialog_date) == True:
                self.move_to_element_click(self.changeTypeBtn4Time)
                self.select_label_type((By.ID,'columnTypeQuota'))

    def to_time(self):
        if self.is_display(self.dialog_date) == False:
            if self.is_display(self.dialog_dimdic) == True:
                self.move_to_element_click(self.changeTypeBtn4Dim)
                self.select_label_type((By.ID,'columnTypeTime'))
            elif self.is_display(self.dialog_quota) == True:
                self.move_to_element_click(self.changeTypeBtn4Quota)
                self.select_label_type((By.ID,'columnTypeTime'))

    switchTypeSubmitBtn = (By.ID,'switchTypeSubmitBtn')
    def select_label_type(self,loc):
        self.move_to_element_click(loc)
        self.move_to_element_click(self.switchTypeSubmitBtn)



    cover = (By.XPATH,'//body/div[@class="zMsg_cover cover_body"]')
    def cover_is_display(self):
        i = 0 
        while self.is_display(self.cover) == True and i < 30 :
            i = i + 1 
            time.sleep(2)
        return True
        









