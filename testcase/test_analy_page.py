# /usr/bin/python
# coding= utf-8
import allure
import time
import sys
# sys.path.append('.')
# print(sys.path)
from pages.analyPage import AnalyPage
from common import param
import pytest
import datetime


@allure.feature('自助报表')
class Test_analy_Page():

    def label_select(self,analy_Page,selfInfo,source_id):
        #=====================枚举类型=========================
        #维度
        if selfInfo['type'] == 'dimdic':
            analy_Page.enum_dimdic_click()
        #维度分组
        elif selfInfo['type'] == 'dimdicGroup':
            labelgroup = selfInfo["groupName"]
            labelvalue = selfInfo["groupValue"]
            if 'groupDel' in selfInfo:
                analy_Page.enum_dimdicGroup_click(labelgroup,labelvalue,selfInfo["groupDel"])
            else:
                analy_Page.enum_dimdicGroup_click(labelgroup,labelvalue,'')
        #条件
        elif selfInfo['type'] == 'dimdicCondition':
            analy_Page.enum_condition_click(selfInfo["value"])
        
        #指标计数
        elif selfInfo['type'] == 'dimdicCount':
            analy_Page.enum_dimdicCount_click()
        #=====================数值=========================
        #作为指标
        elif selfInfo['type'] == 'quota':
            analy_Page.num_quotaCalculate_click(selfInfo["value"])
        
        #作为维度 /步长分组  
        elif selfInfo['type'] == 'quota_step':
            analy_Page.num_quotaStep_click(selfInfo['value'])
            analy_Page.quota_stepNULL_click()
            analy_Page.quota_alert_btn_click()
        
        #作为维度 /选点分组  
        elif selfInfo['type'] == 'quota_point':
            analy_Page.num_quotaPoint_click(selfInfo['value'])
            #忽略空值
            analy_Page.quota_pointNULL_click()
            analy_Page.quota_alert_btn_click()
        
        #作为条件
        elif selfInfo['type'] == 'quota_condition':
            analy_Page.num_quotaCondition_click(selfInfo['value'])
            analy_Page.quota_alert_btn_click()
        #=====================时间=========================
        # 按年月分组
        elif selfInfo['type'] == 'quota_time':
            analy_Page.as_time_quota_click('按年/月分组')
            analy_Page.time_quotaYM_click(selfInfo["value"])
            time.sleep(0.5)
            analy_Page.quota_time_alert_btn_click()
        
        #选点分组
        elif selfInfo['type'] == 'quota_timePoint':
            # label_format = get_label_dateFormart(selfInfo['labelName'],source_id)
            label_format = 'YYYYMM'
            if len(selfInfo['value'][0]) == 8:
                label_format = 'YYYYMMDD'
            elif len(selfInfo['value'][0]) == 14:
                label_format = 'YYYYMMDDhhmmss'
            analy_Page.as_time_quota_click('选点分组')
            analy_Page.quota_group_time_point_sendkeys(label_format,selfInfo['value'])
            analy_Page.quota_time_ignore_null()
            analy_Page.quota_time_alert_btn_click()
        
        
        #作为查询条件
        elif selfInfo['type'] == 'quota_timeCondition':
            # label_formate = get_label_dateFormart(selfInfo['labelName'],source_id)
            label_format = 'YYYYMM'
            if len(selfInfo['value'][0]) == 8:
                label_format = 'YYYYMMDD'
            elif len(selfInfo['value'][0]) == 14:
                label_format = 'YYYYMMDDhhmmss'
            analy_Page.as_time_quota_click('作为条件')
            analy_Page.time_click(label_format,selfInfo['value'])
            analy_Page.quota_time_alert_btn_click()

        #维度
        else:
            analy_Page.enum_dimdic_click()
        #关闭type=5的下钻图层
        analy_Page.close_type5()




    def analy_search(self,analy_Page,selfInfo,source_id):

        if 'labelFile' in selfInfo and selfInfo['labelFile']!='':
            #点击上级目录
            analy_Page.file_click(selfInfo['labelFile'])
        elif 'searchlabel' not in selfInfo:
            analy_Page.label_search(selfInfo['labelName'])
        else:      
            #点击搜索框搜索  
            analy_Page.label_search(selfInfo["searchlabel"])
        #点击标签
        analy_Page.label_value_click(selfInfo['labelName'])   

        self.label_select(analy_Page,selfInfo,source_id)




    def analy_level(self,analy_Page,selfInfo,source_id):

        if 'labelFile' in selfInfo and selfInfo['labelFile']!='':
            #点击上级目录
            analy_Page.file_click(selfInfo['labelFile'])
        elif 'searchlabel' not in selfInfo:
            analy_Page.label_search(selfInfo['labelName'])
        else:      
            #点击搜索框搜索  
            analy_Page.label_search(selfInfo["searchlabel"])
        #拖拽标签层级
        analy_Page.label_drag_drop(selfInfo['labelName'])  

        self.label_select(analy_Page,selfInfo,source_id)

    #条件选择
    def condition_select(self,analy_Page,conditionInfo):
        analy_Page.condition_filter_click(conditionInfo['labelName'],conditionInfo['value'])
        analy_Page.quota_having_btn_click()




    @allure.story('自助报表查询')
    @pytest.mark.run(order=1)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize("dic",param.analy_data)
    def test_analy_search(self,auto_analy,to_parent_frame,dic):
        '''
        ==============自助报表查询==================
        '''
        analy_Page = AnalyPage(auto_analy)
        analy_Page.label_source_select(dic["source"])
        source_id = analy_Page.get_label_source()

        if dic['sourceType']=='已传':
            with allure.step('点击已传数据：{}'.format(dic['sourceTypeName'])):
                analy_Page.label_group_select('已传数据')
                analy_Page.uploaded_users_click(dic['sourceTypeName'])
                analy_Page.uploaded_user_btn_click()
        elif dic['sourceType']=='已存':
            with allure.step('点击已存数据:{}'.format(dic['sourceTypeName'][0])):
                analy_Page.label_group_select('已存数据')
                sourceTypeName = dic['sourceTypeName']
                if type(dic['sourceTypeName']) == list:
                    sourceTypeName = dic['sourceTypeName'][0]
                analy_Page.saved_users_click(sourceTypeName)
                analy_Page.saved_user_btn_click()
        
        acct_month_selected = analy_Page.get_acctMonth_selected()
        time.sleep(0.2)
        if acct_month_selected[0:-1] not in dic['acctMonth']:
            analy_Page.cancel_acct_month()
        time.sleep(0.5)
        for acct_month in dic['acctMonth']:
            if acct_month != acct_month_selected[0:-1]:
                with allure.step('点击账期：{}'.format(acct_month)):
                    analy_Page.select_acctMonth(acct_month)
        #标签选择
        for selfInfo in dic['selfInfos']:
            with allure.step('选择标签：{}'.format(selfInfo['labelName'])):
                self.analy_search(analy_Page,selfInfo,source_id)
                time.sleep(0.5)
        #层级选择
        if 'levelInfos' in dic:
            for levelInfo in dic['levelInfos']:
                with allure.step('选择层级：{}'.format(levelInfo['labelName'])):
                    self.analy_level(analy_Page,levelInfo,source_id)
                    time.sleep(1)

        #条件选择
        if 'conditionInfos' in dic:
            analy_Page.search_btn_click()
            for conditionInfo in dic['conditionInfos']:
                with allure.step('选择条件：{}'.format(conditionInfo['labelName'])):
                    self.condition_select(analy_Page,conditionInfo)

        with allure.step('点击查询'):
            analy_Page.search_btn_click()
        
        #参数：面包屑长度
        if 'levelInfos' in dic:
            with allure.step('逐层点击'):
                analy_Page.get_table_content(len(dic['levelInfos'])+1)

        # if analy_Page.breadcrumb_is_show() == True :
        #     analy_Page.cover_is_display()
        analy_Page.cover_is_display()   
        
        with allure.step('结果验证'):
            table = analy_Page.get_table_title()
            if 'selfInfos' in dic:
                assert table is not None
                for selfInfo in dic['selfInfos']:
                    if selfInfo['type'] == 'dimdic':
                        assert selfInfo['labelName'] in table
                    elif selfInfo['type'] == 'dimdicGroup' :
                        assert selfInfo['labelName']+'-分组' in table
                    elif selfInfo['type'] == 'dimdicCondition' :   
                        assert selfInfo['labelName'] in table
                    # for i in dic['quotaCalculate']:
                    #     assert dic['quota']+单位+i in table   
                    # assert dic['quota_step'] in table 单位没拼接上
                    # assert dic['quota_point'] in table
                    elif selfInfo['type'] == 'quota_timeGroup_name' :
                        assert selfInfo['labelName'] in table
                    elif selfInfo['type'] == 'quota_timePoint_name' :    
                        assert selfInfo['labelName'] in table
                    elif selfInfo['type'] == 'dimdicCount' :    
                        assert selfInfo['labelName']+'-计数' in table

    @allure.story('点击模板查询')
    @pytest.mark.run(order=2)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize("dic",param.filter_Info)
    def test_analy_filter_search(self,auto_analy,to_parent_frame,dic):
        '''
        ==============点击模板查询==================
        '''
        analy_Page = AnalyPage(auto_analy)
        analy_Page.cover_is_display()
        #模板
        with allure.step('点击{}模板：{}'.format(dic['type'],dic['name'])):
            analy_Page.filter_user_click()
            source_id = analy_Page.filter_click(dic['type'],dic['name'])
            analy_Page.self_search_click()
        #标签选择
        if 'selfInfos' in dic:
            for selfInfo in dic['selfInfos']:
                with allure.step('选择标签：{}'.format(selfInfo['labelName'])):
                    self.analy_search(analy_Page,selfInfo,source_id)
                    time.sleep(0.5)
        #层级选择
        if 'levelInfos' in dic:
            for levelInfo in dic['levelInfos']:
                with allure.step('选择层级：{}'.format(levelInfo['labelName'])):
                    self.analy_level(analy_Page,levelInfo,source_id)
                    time.sleep(1)

        #条件选择
        if 'conditionInfos' in dic:
            analy_Page.search_btn_click()
            for conditionInfo in dic['conditionInfos']:
                with allure.step('选择条件：{}'.format(conditionInfo['labelName'])):
                    self.condition_select(analy_Page,conditionInfo)

        with allure.step('保存查询'):
            analy_Page.search_btn_click()
        
        #参数：面包屑长度
        if 'levelInfos' in dic:
            with allure.step('逐层点击'):
                analy_Page.get_table_content(len(dic['levelInfos'])+1)

        if analy_Page.breadcrumb_is_show() == True :
            time.sleep(2)
        time.sleep(1)    
        table = analy_Page.get_table_title()
        with allure.step('结果验证'):
            assert table != ''
            if 'selfInfos' in dic:
                for selfInfo in dic['selfInfos']:
                    if selfInfo['type'] == 'dimdic':
                        assert selfInfo['labelName'] in table
                    elif selfInfo['type'] == 'dimdicGroup' :
                        assert selfInfo['labelName']+'-分组' in table
                    elif selfInfo['type'] == 'dimdicCondition' :   
                        assert selfInfo['labelName'] in table
                    # for i in dic['quotaCalculate']:
                    #     assert dic['quota']+单位+i in table   
                    # assert dic['quota_step'] in table 单位没拼接上
                    # assert dic['quota_point'] in table
                    elif selfInfo['type'] == 'quota_timeGroup_name' :
                        assert selfInfo['labelName'] in table
                    elif selfInfo['type'] == 'quota_timePoint_name' :    
                        assert selfInfo['labelName'] in table
                    elif selfInfo['type'] == 'dimdicCount' :    
                        assert selfInfo['labelName']+'-计数' in table
        
        

    @allure.story('自助报表保存模板')
    @pytest.mark.run(order=3)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize('dic',param.save_template)
    def test_analy_save_template(self,auto_analy,to_parent_frame,dic):
        '''
        ==============自助报表保存模板==================
        '''
        analy_Page = AnalyPage(auto_analy)
        analy_Page.label_source_select(dic["source"])
        source_id = analy_Page.get_label_source()

        if dic['sourceType']=='已传':
            with allure.step('点击已传数据'):
                analy_Page.label_group_select('已传数据')
                analy_Page.uploaded_users_click(dic['sourceTypeName'])
                analy_Page.uploaded_user_btn_click()
        elif dic['sourceType']=='已存':
            with allure.step('点击已存数据'):
                analy_Page.label_group_select('已存数据')
                sourceTypeName = dic['sourceTypeName']
                if type(dic['sourceTypeName']) == list:
                    sourceTypeName = dic['sourceTypeName'][0]
                analy_Page.saved_users_click(sourceTypeName)
                analy_Page.saved_user_btn_click()

        acct_month_selected = analy_Page.get_acctMonth_selected()
        if acct_month_selected[0:-1] not in dic['acctMonth']:
            analy_Page.cancel_acct_month()
        time.sleep(0.5)
        for acct_month in dic['acctMonth']:
            if acct_month != acct_month_selected[0:-1]:
                with allure.step('点击账期：{}'.format(acct_month)):
                    analy_Page.select_acctMonth(acct_month)

        for selfInfo in dic['selfInfos']:
            with allure.step('选择标签：{}'.format(selfInfo['labelName'])):
                self.analy_search(analy_Page,selfInfo,source_id)
                time.sleep(0.5)
        with allure.step('保存查询'):
            analy_Page.search_btn_click()

        with allure.step('保存模板'):
            analy_Page.template_save_btn_click()
            if param.staff_no not in dic['filterStaff']:
                dic['filterStaff'].append(param.staff_no)
        result = analy_Page.save_filter_info(dic['filterName'],dic['filterType'],dic['remark'],dic['filterStaff'])
        if 'success' == result:
            analy_Page.filter_btn_click()
            alert = analy_Page.alert_tip()
            if '保存成功' in alert:
                analy_Page.alert_btn_click()
            assert '保存成功' in alert


    @allure.story('自助报表导出')
    @pytest.mark.run(order=4)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize('dic',param.download_data)
    def test_analy_download_data(self,auto_analy,to_parent_frame,dic):
        '''
        ==============自助报表导出==================
        '''
        analy_Page = AnalyPage(auto_analy)
        analy_Page.label_source_select(dic["source"])
        source_id = analy_Page.get_label_source()

        if dic['sourceType']=='已传':
            with allure.step('点击已传数据'):
                analy_Page.label_group_select('已传数据')
                analy_Page.uploaded_users_click(dic['sourceTypeName'])
                analy_Page.uploaded_user_btn_click()
        elif dic['sourceType']=='已存':
            with allure.step('点击已存数据'):
                analy_Page.label_group_select('已存数据')
                sourceTypeName = dic['sourceTypeName']
                if type(dic['sourceTypeName']) == list:
                    sourceTypeName = dic['sourceTypeName'][0]
                analy_Page.saved_users_click(sourceTypeName)
                analy_Page.saved_user_btn_click()

        acct_month_selected = analy_Page.get_acctMonth_selected()
        if acct_month_selected[0:-1] not in dic['acctMonth']:
            analy_Page.cancel_acct_month()
        time.sleep(0.5)
        for acct_month in dic['acctMonth']:
            if acct_month != acct_month_selected[0:-1]:
                with allure.step('点击账期：{}'.format(acct_month)):
                    analy_Page.select_acctMonth(acct_month)

        for selfInfo in dic['selfInfos']:
            with allure.step('选择标签：{}'.format(selfInfo['labelName'])):
                self.analy_search(analy_Page,selfInfo,source_id)
                time.sleep(0.5)
        with allure.step('保存查询'):    
            analy_Page.search_btn_click()
        with allure.step('点击下载'):
            analy_Page.download_data()
        
        if analy_Page.alert_is_exist() == True:
            tip = analy_Page.alert_tip()
            assert tip == ''
            with allure.step('弹框提示{}'.format(tip)):  
                analy_Page.alert_btn_click()
        else:
            with allure.step('进入下载路径自行查看下载结果是否正常'):  
                print('点击下载结果没有弹框，进入下载路径自行查看下载结果是否正常')




    @allure.story('清理模板')
    @pytest.mark.run(order=5)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize("dic",param.data_clean_analy)
    def test_data_clean_analy(self,auto_analy,to_parent_frame,dic):
        '''
        ==============清理模板==================
        '''
        analy_Page = AnalyPage(auto_analy)
        analy_Page.cover_is_display()
        # analy_Page.label_source_select(dic["source"])
        # source_id = analy_Page.get_label_source()
        
        #模板
        analy_Page.filter_user_click()
        time.sleep(0.5)
        for filter in dic['filter_name']:
            with allure.step('清理{}模板{}'.format(filter['type'],filter['name'])):
                result = analy_Page.delete_filter(filter['type'],filter['name'])
                assert result == True
        time.sleep(0.5)
