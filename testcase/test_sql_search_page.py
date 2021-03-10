import pytest
import sys
sys.path.append('.')
from pages.sqlSearchPage import SqlSearchPage
from pages.analyPage import AnalyPage
from common import param
import allure
import time
import datetime

@allure.feature('SQL查询')
class Test_sqlSearch_Page():



    def exec_operate(self,sqlSearchPage,analy_Page,oper):
        sqlSearchPage.cover_is_display()
        if oper['operate'] == '执行':
            sqlSearchPage.runSQL_click()
        elif '格式化' in oper['operate']:
            sqlSearchPage.formatSQL_click()
        elif oper['operate'] == '清空':
            sqlSearchPage.clearSQL_click()
        elif oper['operate'] == '保存模板':
            oper['filter'][0]['filterName'] = oper['filter'][0]['filterName']+datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            sqlSearchPage.saveSQL_click(oper['filter'][0])

            assert sqlSearchPage.alert_tip() == '保存成功！'
            if sqlSearchPage.alert_tip() == '保存成功！':
                sqlSearchPage.alert_btn_click()
            
        elif oper['operate'] == '保存客群':
            sqlSearchPage.saveUserGroup_click()
            saved = oper['saved'][0]
            sqlSearchPage.save_user_name_sendkeys(saved['savedName']+datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            sqlSearchPage.save_user_expiration_time(saved['savedExpirationTime'])
            sqlSearchPage.save_user_remark_sendkeys(saved['remark'])
            sqlSearchPage.save_group_click()
            assert sqlSearchPage.alert_tip() == '保存成功！'
            if sqlSearchPage.alert_tip() == '保存成功！':
                sqlSearchPage.alert_btn_click()

        elif oper['operate'] == '统计分析':

            sqlSearchPage.analysisSQL_click()
            sqlSearchPage.cover_is_display()
            sqlSearchPage.switch_to_frame('自助报表')
            #点击标签
            selfInfos = oper['selfInfos']
            for selfInfo in selfInfos:
                with allure.step('选择标签：{}'.format(selfInfo['labelName'])):
                    if analy_Page.label_value_click(selfInfo['labelName']) == True:
                        self.label_select(analy_Page,selfInfo) 

            analy_Page.search_btn_click()
        
        




    def label_select(self,analy_Page,selfInfo):
        #=====================枚举类型=========================
        #维度
        if selfInfo['type'] == 'dimdic':
            analy_Page.to_dimdic()
            analy_Page.enum_dimdic_click()
        #维度分组
        elif selfInfo['type'] == 'dimdicGroup':
            analy_Page.to_dimdic()
            labelgroup = selfInfo["groupName"]
            labelvalue = selfInfo["groupValue"]
            if 'groupDel' in selfInfo:
                analy_Page.enum_dimdicGroup_sqlSearch_click(labelgroup,labelvalue,selfInfo["groupDel"])
            else:
                analy_Page.enum_dimdicGroup_sqlSearch_click(labelgroup,labelvalue,'')
        #条件
        elif selfInfo['type'] == 'dimdicCondition':
            analy_Page.to_dimdic()
            analy_Page.enum_condition_click(selfInfo["value"])
        
        #指标计数
        elif selfInfo['type'] == 'dimdicCount':
            analy_Page.to_dimdic()
            analy_Page.enum_dimdicCount_click()
        #=====================数值=========================
        #作为指标
        elif selfInfo['type'] == 'quota':
            analy_Page.to_quota()
            analy_Page.num_quotaCalculate_click(selfInfo["value"])
        
        #作为维度 /步长分组  
        elif selfInfo['type'] == 'quota_step':
            analy_Page.to_quota()
            analy_Page.num_quotaStep_click(selfInfo['value'])
            analy_Page.quota_stepNULL_click()
            analy_Page.quota_alert_btn_click()
        
        #作为维度 /选点分组  
        elif selfInfo['type'] == 'quota_point':
            analy_Page.to_quota()
            analy_Page.num_quotaPoint_click(selfInfo['value'])
            #忽略空值
            analy_Page.quota_pointNULL_click()
            analy_Page.quota_alert_btn_click()
        
        #作为条件
        elif selfInfo['type'] == 'quota_condition':
            analy_Page.to_quota()
            analy_Page.num_quotaCondition_click(selfInfo['value'])
            analy_Page.quota_alert_btn_click()
        #=====================时间=========================
        # 按年月分组
        elif selfInfo['type'] == 'quota_time':
            analy_Page.to_time()
            analy_Page.as_time_quota_click('按年/月分组')
            analy_Page.time_quotaYM_click(selfInfo["value"])
            time.sleep(0.5)
            analy_Page.quota_time_alert_btn_click()
        
        #选点分组
        elif selfInfo['type'] == 'quota_timePoint':
            analy_Page.to_time()
            label_format = analy_Page.get_format(selfInfo['value'])
            analy_Page.as_time_quota_click('选点分组')
            analy_Page.quota_group_time_point_sendkeys(label_format,selfInfo['value'])
            analy_Page.quota_time_ignore_null()
            analy_Page.quota_time_alert_btn_click()
        
        
        #作为查询条件
        elif selfInfo['type'] == 'quota_timeCondition':
            analy_Page.to_time()
            label_format = analy_Page.get_format(selfInfo['value'])
            analy_Page.as_time_quota_click('作为条件')
            analy_Page.time_click(label_format,selfInfo['value'])
            analy_Page.quota_time_alert_btn_click()

        #维度
        else:
            analy_Page.to_dimdic()
            analy_Page.enum_dimdic_click()





    @allure.story('SQL查询')
    @pytest.mark.run(order=1)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize('dic',param.sql_search_data)
    def test_sql_search(self,sql_search,to_parent_frame,dic):
        '''
            sql查询
        '''
        sqlSearchPage = SqlSearchPage(sql_search)
        sqlSearchPage.cover_is_display()
        analy_Page = AnalyPage(sql_search)
        #点击筛选/模板
        if 'type' in dic:
            with allure.step('点击{}模板查询:{}'.format(dic['type'],dic['filterName'])):
                sqlSearchPage.select_group(2)
                sqlSearchPage.select_type(dic['type'])
                if dic['type']=='我的':
                    result = sqlSearchPage.filter_select_my(dic['filterName'])
                elif dic['type']=='分享':
                    result = sqlSearchPage.filter_select_share(dic['filterName'])
                elif dic['type']=='公共':
                    result = sqlSearchPage.filter_select_sys(dic['filterName'])
                with allure.step('点击模板结果：{}'.format(result)):
                    assert result == True

            if 'sql' in dic:
                with allure.step('输入sql：{}'.format(dic['sql'])):
                    sqlSearchPage.input_sql(dic['sql'])

        else:
            sqlSearchPage.select_group(1)
            #选择数据源
            with allure.step('选择数据源：{}'.format(dic['source'])):
                sqlSearchPage.select_source(dic['source'])

            if 'table' in dic:
                with allure.step('选择查询的表：{}'.format(dic['table'])):
                    sqlSearchPage.search_table(dic['table'])

            with allure.step('输入sql：{}'.format(dic['sql'])):    
                sqlSearchPage.input_sql(dic['sql'])

        #操作
        for oper in dic['operateInfo']:
            with allure.step('操作：{}'.format(oper)):
                self.exec_operate(sqlSearchPage,analy_Page,oper)



    @allure.story('SQL查询模板清理')
    @pytest.mark.run(order=2)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize('dic',param.data_clean_sql)
    def test_data_clean(self,sql_search,to_parent_frame,dic):
        '''
            sql查询模板清理
        '''
        sqlSearchPage = SqlSearchPage(sql_search)
        sqlSearchPage.cover_is_display()
        time.sleep(1)
        #点击模板
        if 'filter_name' in dic:
            #选择模板
            sqlSearchPage.select_group(2)
            for filter in dic['filter_name']:
                with allure.step('清理{}模板:{}'.format(filter['type'],filter['name'])):                
                    sqlSearchPage.select_type(filter['type'])
                    sqlSearchPage.delete_filter(filter['type'],filter['name'])
        
        if 'operateInfo' in dic:
            for oper in dic['operateInfo']:
                if oper['operate'] == '任务管理':
                    sqlSearchPage.taskSQL_click()
                    sqlSearchPage.cover_is_display()
                    sqlSearchPage.taskSQL_clear(oper['name'])





        

# if __name__ == "__main__":
    
#     pytest.main('-s','testcase/test_sql_search_page.py::Test_sqlSearch_Page::test_sql_search')
        

        








