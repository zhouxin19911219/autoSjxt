from pages.basePage import Page
from selenium.webdriver.common.by import By
import datetime
import time

class SqlSearchPage(Page):
    
    #选择筛选或模板
    select_group_str = '//div[@class="section-body"]/div[@class="tabs"]/div[@class="btn-group"]/button'
    def select_group(self,id):
        self.move_to_element_click((By.XPATH,self.select_group_str+'['+str(id)+']'))

    #选择我的/分享/公共
    select_type_str = '//div[@class="modules-tab"]/dl/dd'
    def select_type(self,group):
        group_names = self.get_eles_text((By.XPATH,self.select_type_str))
        i = 0
        for name in group_names:
            i = i + 1
            if group == name :
                self.move_to_element_click((By.XPATH,self.select_type_str+'['+str(i)+']'))
                break
        

    schema_name = (By.ID,'schema_name')
    def select_source(self,source):
        self.select_by_value(self.schema_name,source)

    treeNodesSearchInput = (By.ID,'treeNodesSearchInput')
    ztreeSearchBtn = (By.ID,'ztreeSearchBtn')
    def search_table(self,table):
        self.send_keys(self.treeNodesSearchInput,table)
        self.move_to_element_click(self.ztreeSearchBtn)

    sqlText = (By.ID,'sqlText')
    def input_sql(self,sql):
        self.clear(self.sqlText)
        self.send_keys(self.sqlText,sql)


    runSQL = (By.ID,'runSQL')
    formatSQL = (By.ID,'formatSQL')
    clearSQL = (By.ID,'clearSQL')
    saveSQL = (By.ID,'saveSQL')
    saveUserGroup = (By.ID,'saveUserGroup')
    analysisSQL = (By.ID,'analysisSQL')
    showPushIOPBtn = (By.ID,'showPushIOPBtn')

    filterName = (By.ID,'filterName')
    filterType_str = '//input[@name="filterType"]'
    ifPushIop_str = '//span/input[@name="ifPushIop"]'
    isCreateTask_str = '//span/input[@name="isCreateTask"]'
    taskType_str = '//span/input[@name="taskType"]'
    executionTime_0 = (By.ID,'executionTime_0')
    startTime = (By.ID,'startTime')
    endTime = (By.ID,'endTime')
    executionTime_1 = (By.ID,'executionTime_1')
    remark = (By.ID,'remark')
    filter_staff_search = (By.ID,'input_staff')
    filter_staff_search_click = (By.ID,'searchBtn')
    filter_staff = '//tbody[@id="table_body"]/tr'
    saveLabelFilterBtn = (By.ID,'saveLabelFilterBtn')
    filterFileName_str = '//tbody[@id="folder_template_table_body"]'

    def runSQL_click(self):
        self.move_to_element_click(self.runSQL)
        self.cover_is_display()
        print('加载完成')

    def formatSQL_click(self):
        self.move_to_element_click(self.formatSQL)

    def clearSQL_click(self):
        self.move_to_element_click(self.clearSQL)

    def saveSQL_click(self,filter):
        self.move_to_element_click(self.saveSQL)
        is_push = self.find_element_attr(self.showPushIOPBtn,'value')
        print('查询sql查询菜单权限是否iop推送：'+is_push[0])
        self.save_filter_info(filter,is_push[0])

    def saveUserGroup_click(self):
        self.move_to_element_click(self.saveUserGroup)    
        self.cover_is_display()

    def analysisSQL_click(self):
        self.move_to_element_click(self.analysisSQL)      

    taskSQL = (By.ID,'taskSQL')
    def taskSQL_click(self):
        self.move_to_element_click(self.taskSQL)

    sqlTaskTab_str = '//tbody[@id="sqlTaskTab"]'
    def taskSQL_clear(self,name):
        taskNames = self.get_eles_text((By.XPATH,self.sqlTaskTab_str+'/tr/td[1]'))
        i = 0 
        for taskName in taskNames:
            i = i + 1
            if name in taskName:
                self.move_to_element_click((By.XPATH,self.sqlTaskTab_str+'/tr['+str(i)+']/td[7]/input[@class="my_btn delBtn"]'))

                if self.alert_is_exist() == False:
                    time.sleep(2)
                if '移除' in self.alert_tip():
                    self.alert_btn_sure_click()
                    i = i - 1
                    self.cover_is_display()
                    self.alert_btn_sure_click()

            

        

    def save_filter_info(self,filterInfo,is_push):
        #名称
        name = filterInfo['filterName']
        self.send_keys(self.filterName,name)
        
        #备注
        if 'remark' in filterInfo:
            remark = filterInfo['remark']
            self.send_keys(self.remark,remark)

        #是否创建任务
        if 'isCreateTask' in filterInfo and filterInfo['isCreateTask'] == True:
            self.click((By.XPATH,self.isCreateTask_str+'[@value="1"]'))
            #周期
            if 'taskType' in filterInfo and filterInfo['taskType']=='周期':
                self.click((By.XPATH,self.taskType_str+'[@value="1"]'))
                if ('startTime' in filterInfo and len(filterInfo['startTime']) == 8) and ('endTime' in filterInfo and len(filterInfo['endTime']) == 8):
                    self.move_to_element_click(self.startTime)
                    time.sleep(0.2)
                    self.time_input('YYYYMMDD',filterInfo['startTime']) 

                    self.move_to_element_click(self.endTime)
                    time.sleep(0.2)
                    self.time_input('YYYYMMDD',filterInfo['endTime'])

                    self.move_to_element_click(self.executionTime_1)
                    time.sleep(0.2)
                    self.time_input('HH',filterInfo['executionTime'])

                else:
                    now = datetime.datetime.now().strftime('%Y%m%d')
                    self.move_to_element_click(self.startTime)
                    time.sleep(0.2)
                    self.time_input('YYYYMMDD',now) 

                    self.move_to_element_click(self.endTime)
                    time.sleep(0.2)
                    self.time_input('YYYYMMDD',(datetime.datetime.strptime(now,'%Y%m%d')+datetime.timedelta(days=2)).strftime('%Y%m%d'))

                    self.move_to_element_click(self.executionTime_1)
                    time.sleep(0.2)
                    self.time_input('hh','00')


            #单次
            else:
                self.click((By.XPATH,self.taskType_str+'[@value="0"]'))
                self.move_to_element_click(self.executionTime_0)
                time.sleep(0.2)
                if 'executionTime' in filterInfo and len(filterInfo['executionTime'])==10:
                    self.time_input('YYYYMMDDhh',filterInfo['executionTime'])
                else:
                    now = datetime.datetime.now().strftime('%Y%m%d%H')
                    self.time_input('YYYYMMDDhh',now)

        else:
            self.click((By.XPATH,self.isCreateTask_str+'[@value="0"]'))

        time.sleep(1)
        #是否推送iop
        if is_push.lower() == 'true':
            if 'ifPushIop' in filterInfo and filterInfo['ifPushIop'] == '是':
                self.click((By.XPATH,self.ifPushIop_str+'[@value="1"]'))
            else:
                self.click((By.XPATH,self.ifPushIop_str+'[@value="0"]'))
        
        self.add_attr('#panel_save_sql > div > div.panel_body',0,'style','height: 100%;max-height: 500px;overflow:auto;')


        type_filter = filterInfo['filterType']
        if '我的' == type_filter :
            ele = (By.XPATH,self.filterType_str+'[@value="02"]')
            self.move_to_element_click(ele)

            if 'filterFileName' in filterInfo and filterInfo['filterFileName'] !='我的模板':
                fileNames = self.get_eles_text((By.XPATH,self.filterFileName_str+'/tr'))
                i = 0 
                for fileName in fileNames:
                    i = i + 1
                    if fileName == filterInfo['filterFileName']:
                        self.click((By.XPATH,self.filterFileName_str+'/tr['+str(i)+']/td[1]'))
                        break

        elif '公共' == type_filter :
            ele = (By.XPATH,self.filterType_str+'[@value="01"]')
            self.move_to_element_click(ele)


            if 'filterFileName' in filterInfo and filterInfo['filterFileName'] !='公共模板':
                fileNames = self.get_eles_text(self.filterFileName_str+'/tr')
                i = 0 
                for fileName in fileNames:
                    i = i + 1
                    if fileName == filterInfo['filterFileName']:
                        self.click((self.filterFileName_str+'/tr['+str(i)+']/td[1]'))
                        break

        elif '分享' == type_filter :
            ele = (By.XPATH,self.filterType_str+'[@value="03"]')
            self.move_to_element_click(ele)
            staffs = filterInfo['staffs']
            self.cover_is_display()
            if self.is_display(self.filter_staff_search):
                for staff in staffs:
                    self.clear(self.filter_staff_search)
                    self.send_keys(self.filter_staff_search,staff)
                    self.move_to_element_click(self.filter_staff_search_click)
                    self.cover_is_display()
                    filter_list = self.find_elements((By.XPATH,self.filter_staff))
                    
                    if  len(filter_list) > 0:
                        for i in range(1,len(filter_list)+1):
                            staff_name = self.get_text((By.XPATH,self.filter_staff+'['+str(i)+']/td[2]'))
                            if staff_name == staff:
                                self.scroll('#table_body > tr',str(i-1))
                                self.move_to_element_click((By.XPATH,self.filter_staff+'['+str(i)+']/td[1]'))
                                break
        
        self.move_to_element_click(self.saveLabelFilterBtn)
        self.cover_is_display()
        return 'success'

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

    #=====================点击模板查询============================

    filter_my_str = '//ul[@id="myLabels"]'
    panel_my = (By.XPATH,'//*[@class="dimension_panel tag_panel"]')
    def filter_select_my(self,filterName):
        if self.is_display(self.panel_my) == False:
            time.sleep(2)
        result = False
        # filterFiles = self.find_elements((By.XPATH,self.filter_my_str+'/li/ul/li'))
        # i = 0
        # for filterFile in filterFiles:
        #     i = i + 1
        #     my_class = self.find_element_attr((By.XPATH,self.filter_my_str+'/li/ul/li['+str(i)+']/span'),'class')[0]
        #     if 'center_close' in my_class:
        #         self.move_to_element_click((By.XPATH,self.filter_my_str+'/li/ul/li['+str(i)+']/span'))

        #         if self.is_exist((By.XPATH,self.filter_my_str+'/li/ul/li['+str(i)+']/ul/li/a'))==True:
        #             filter_eles = self.find_elements((By.XPATH,self.filter_my_str+'/li/ul/li['+str(i)+']/ul/li/a'))
        #             for filter_ele in filter_eles:
        #                 title = filter_ele.get_attribute('title')
        #                 if filterName in title:
        #                     filter_ele.click()
        #                     result = True
        #                     break
        #     else:
        #         filter_eles = self.find_elements((By.XPATH,self.filter_my_str+'/li/ul/li['+str(i)+']/a'))
        #         for filter_ele in filter_eles:
        #             title = filter_ele.get_attribute('title')
        #             if filterName in title:
        #                 filter_ele.click()
        #                 result = True
        #                 break
        id = self.get_filter_id(filterName[0],self.filter_my_str,True)
        if id != []:
            self.move_to_element_click((By.ID,id))
            result=True

        return result

    def get_filter_id(self,name,filter_str,is_radio):
        result_id = []
        filterFiles = self.find_elements((By.XPATH,filter_str+'/li/ul/li'))
        i = 0
        for filterFile in filterFiles:
            i = i + 1
            my_class = self.find_element_attr((By.XPATH,filter_str+'/li/ul/li['+str(i)+']/span'),'class')[0]
            if 'center_close' in my_class or 'bottom_close' in my_class:
                self.move_to_element_click((By.XPATH,filter_str+'/li/ul/li['+str(i)+']/span'))

                if self.is_exist((By.XPATH,filter_str+'/li/ul/li['+str(i)+']/ul/li/a'))==True:
                    filter_eles = self.find_elements((By.XPATH,filter_str+'/li/ul/li['+str(i)+']/ul/li/a'))
                    for filter_ele in filter_eles:
                        title = filter_ele.get_attribute('title')
                        if name in title:
                            # filter_ele.click()
                            result_id.append(filter_ele.get_attribute('id'))
                            if is_radio == True:
                                break
                            
            else:
                filter_eles = self.find_elements((By.XPATH,filter_str+'/li/ul/li['+str(i)+']/a'))
                for filter_ele in filter_eles:
                    title = filter_ele.get_attribute('title')
                    if name in title:
                        # filter_ele.click()
                        result_id.append(filter_ele.get_attribute('id'))
                        if is_radio == True:
                            break
        return result_id


    filter_share_str = '//ul[@id="shareLabels"]'
    panel_share = (By.XPATH,'//*[@class="share_panel tag_panel"]')
    def filter_select_share(self,filterName):
        if self.is_display(self.panel_share) == False:
            time.sleep(2)
        result = False
        filter_eles = self.find_elements((By.XPATH,self.filter_share_str+'/li/ul/li/a'))
        for filter_ele in filter_eles:
            title = filter_ele.get_attribute('title')
            if filterName in title:
                filter_ele.click()
                result = True
                break
        # filterNames = self.get_eles_text((By.XPATH,self.filter_share_str+'/li/span'))
        # i = 0 
        # result = False
        # for filter in filterNames:
        #     i = i + 1
        #     if filter == filterName:
        #         self.move_to_element_click((By.XPATH,self.filter_share_str+'/li['+str(i)+']/span'))
        #         result = True
        #         break    
        return result
    
    filter_sys_str = '//ul[@id="sysLabels"]'
    panel_sys = (By.XPATH,'//*[@class="target_panel tag_panel"]')
    def filter_select_sys(self,filterName):
        if self.is_display(self.panel_sys) == False:
            time.sleep(2)
        result = False
        # filterFiles = self.find_elements((By.XPATH,self.filter_sys_str+'/li/ul/li'))
        # i = 0
        # for filterFile in filterFiles:
        #     i = i + 1
        #     my_class = self.find_element_attr((By.XPATH,self.filter_sys_str+'/li/ul/li['+str(i)+']/span'),'class')[0]
        #     if '_close' in my_class:
        #         self.move_to_element_click((By.XPATH,self.filter_sys_str+'/li/ul/li['+str(i)+']/span'))

        #         if self.is_exist((By.XPATH,self.filter_sys_str+'/li/ul/li['+str(i)+']/ul/li/a'))==True:
        #             filter_eles = self.find_elements((By.XPATH,self.filter_sys_str+'/li/ul/li['+str(i)+']/ul/li/a'))
        #             for filter_ele in filter_eles:
        #                 title = filter_ele.get_attribute('title')
        #                 if filterName in title:
        #                     filter_ele.click()
        #                     result = True
        #                     break
        #     else:
        #         filter_eles = self.find_elements((By.XPATH,self.filter_sys_str+'/li/ul/li['+str(i)+']/a'))
        #         for filter_ele in filter_eles:
        #             title = filter_ele.get_attribute('title')
        #             if filterName in title:
        #                 filter_ele.click()
        #                 result = True
        #                 break
        id = self.get_filter_id(filterName,self.filter_sys_str,True)
        if id != []:
            self.move_to_element_click((By.ID,id))
            result=True
  
        return result
    #=====================模板清理============================

    def delete_filter(self,filterType,filterName):
        i = 0
        filter_str = ''
        if filterType=='我的':
            if self.is_display(self.panel_my) == False:
                time.sleep(2)
            filter_str = self.filter_my_str
        elif filterType=='分享':
            if self.is_display(self.panel_share) == False:
                time.sleep(2)
            filter_str = self.filter_share_str
        elif filterType=='公共':
            if self.is_display(self.panel_sys) == False:
                time.sleep(2)
            filter_str = self.filter_sys_str
        context = self.get_eles_text((By.XPATH,filter_str))
        contexts = context[0].split('\n')
        if len(contexts) != 1:
            ids = self.get_filter_id(filterName[0],filter_str,False)
            for id in ids:
                self.move_to_element_click((By.XPATH,'//a[@id="'+id+'"]/i'))
                if self.alert_is_exist()==False:
                    time.sleep(2)
                if '移除' in self.alert_tip():
                    self.alert_btn_sure_click()
                    self.cover_is_display()

            # filterNames = self.get_eles_text((By.XPATH,filter_str+'/li/ul/li'))
            # i = 0 
            # for filter in filterNames:
            #     i = i + 1
            #     if '×' in filter:
            #         for filterN in filterName:
            #             if filterN in filter:
            #                 self.move_to_element_click((By.XPATH,filter_str+'/li['+str(i)+']/i'))
            #                 if self.alert_is_exist() == False:
            #                     time.sleep(2)
            #                 if '移除' in self.alert_tip():
            #                     self.alert_btn_sure_click()
            #                     i = i - 1
            #                 self.cover_is_display()
    #=============================保存已存===========================
    #保存客户群名称
    save_user_name_ele = (By.ID,'groupName')
    save_user_remark_ele = (By.ID,'groupRemark')
    def save_user_name_sendkeys(self,usersName):
        self.send_keys(self.save_user_name_ele,usersName)

    save_user_expiration_time_ele = (By.ID,'addExpirationTime')
    def save_user_expiration_time(self,timeVal):
        self.click(self.save_user_expiration_time_ele)
        time.sleep(0.5)
        self.time_input('YYYYMMDD',timeVal)

    def save_user_remark_sendkeys(self,usersRemark):
        self.send_keys(self.save_user_remark_ele,usersRemark)

    saveGroupBtn = (By.ID,'saveGroupBtn')
    def save_group_click(self):
        self.move_to_element_click(self.saveGroupBtn)
        self.cover_is_display()


    #=========================时间选择框点击==========================

    #根据时间格式进行选择
    def time_input(self,label_formate,time):
        if label_formate == 'hh':
            if time != '': 
                self.change_HH(time)
        elif label_formate == 'YYYYMM':
            if time != '': 
                self.change_YYYYMM(time)
        elif label_formate == 'YYYYMMDD': 
            if time != '': 
                self.change_YYYYMMDD(time)
        elif label_formate == 'YYYYMMDDhh':
            if time != '': 
                self.change_YYYYMMDDHH(time)
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

    #------------------年月日时格式选日期--------------------
    def change_YYYYMMDDHH(self,time):
        #字符串转日期格式
        time = datetime.datetime.strptime(time,'%Y%m%d%H')
        yy = time.strftime('%Y')
        mm = time.strftime('%m')
        self.change_year(yy)
        self.change_month(mm)  
        hh = time.strftime('%H')
        self.change_hms((By.XPATH,'//div[@class="jedatehmscon jedateprophours"]/p['+str(int(hh)+1)+']'))
        #转字符串格式，并将01变成1
        time = time.strftime('%Y-%m-%d').replace('-0','-')
        ele = (By.XPATH,'//div[@id="jedatebox"]/ul/li[@data-ymd="'+time+'"]')
        self.click(ele)
    #---------------------时格式选日期----------------------
    
    def change_HH(self,time):
        #字符串转日期格式
        time = datetime.datetime.strptime(time,'%H')
        hh = time.strftime('%H')
        self.change_hms((By.XPATH,'//div[@class="jedatehmscon jedateprophours"]/p['+str(int(hh)+1)+']'))
        self.click((By.CLASS_NAME,'jedateok'))
        


    cover = (By.XPATH,'//body/div[@class="zMsg_cover cover_body"]')
    def cover_is_display(self):
        i = 0 
        while self.is_display(self.cover) == True and i < 30 :
            i = i + 1 
            time.sleep(3)

    
        
    def switch_to_frame(self,frameName):
        #切换frame
        self.switch_to_parent_frame()
        frame = (By.XPATH,'//div[@title="'+frameName+'"]/iframe')
        self.switch_frame(frame)



        
    
