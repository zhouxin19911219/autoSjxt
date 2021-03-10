#! /usr/bin/python
# coding=utf-8
import allure
import pytest
import sys
sys.path.append('.')
from pages.listPage import ListPage
from pages.reportDesignPage import ReportDesignPage
from common import param
import time
import datetime

@allure.feature('清单发布')
class Test_List_Page():
    lists = []
    
    @allure.story('查询用户信息')
    @pytest.mark.run(order=1)
    def test_get_staff_info(self,report_design,to_parent_frame):
        reportDesignPage = ReportDesignPage(report_design)
        sql = "select staff_no,staff_name,grade_value from sys_staff staff,sys_staff_grade_rel rel where rel.STAFF_ID = staff.STAFF_ID and staff.STAFF_NO='"+ param.staff_no +"' "
        with allure.step('执行sql查询用户信息：{}'.format(sql)):
            datasource = param.sys_datasource
            staff = reportDesignPage.sql_search_pubulic(datasource,sql)
            Test_List_Page.staff_name = staff[1]
            time.sleep(1)



    @allure.story('清单发布')
    @pytest.mark.run(order = 1)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize('dic',param.list_data)
    def test_list_build(self,list_build,to_parent_frame,dic):
        '''
            ==============清单发布==============
        '''        
        list_Page = ListPage(list_build)
        listName = dic['listname']+datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        Test_List_Page.lists.append(listName)
        
 
        # 切换数据清单
        if dic['listType'] == '数据':
            with allure.step('切换数据清单tab'):
                list_Page.datalist_click()

        #输入清单名称
        list_Page.list_name_sendKeys(listName)
        #账期
        list_Page.list_acctdate_sendKeys(dic['acctDate'])


        if dic['listType'] == '文件':
            #上传清单文件
            with allure.step('上传文件'):
                list_Page.list_file_upload(dic['listFile'])
                while list_Page.list_file_tips() !='上传成功':
                    time.sleep(1)
        elif dic['listType'] == '数据':
            #是否周期
            with allure.step('选择是否周期：{}'.format(dic['cycle'])):
                list_Page.control_click(dic['cycle'])
            #输入数据清单sql
            with allure.step('sql：{}'.format(dic['spilt_sql'])):
                list_Page.split_sql_sendkeys(dic['spilt_sql'])

        #上传说明文件
        if dic['listMarkFile'] != '':
            with allure.step('上传文件说明'):
                list_Page.list_file_remark_upload(dic['listMarkFile'])
                while list_Page.list_file_remark_tips() !='上传成功':
                    time.sleep(1)
        
        if dic['listApprove'] == '是':
            #选择人员审批
            with allure.step('选择审批人员：{}'.format(dic['ApproveStaff'])):
                list_Page.require_approve_click()
                time.sleep(0.5)
                list_Page.require_approve_staff()
                list_Page.approve_staff_search(dic['ApproveStaff'])
                time.sleep(0.5)
                list_Page.approve_staff_search_click()
                list_Page.approve_staff_select_click(dic['ApproveStaff'])
                list_Page.approve_staff_select_btn_click()


        #失效时间
        list_Page.invalid_time_click()
        with allure.step('选择失效时间'):
            if dic['invalidTime']=='' or 'invalidTime' not in dic:
                list_Page.invalid_time_date_click(datetime.datetime.now().strftime('%Y%m%d'))
            elif len(dic['invalidTime']) != 8  :
                list_Page.invalid_time_value_click(dic['invalidTime'])
            else :
                list_Page.invalid_time_date_click(dic['invalidTime'])



        if dic['listSplit'] == '是':            
            #选择拆分
            with allure.step('选择拆分'):
                list_Page.split_click()
            if 'spilt_sql' in dic:
                if '${month' in dic['spilt_sql'] or '${day' in dic['spilt_sql']:
                    with allure.step('sql中含有变量，选择替换方式：{}，替换值：{}'.format(dic['replaceType'],dic['replaceTime'])):
                        res = list_Page.replace_acctmonth(dic['replaceType'],dic['replaceTime'])
                        if 'success' in res:
                            list_Page.replace_acctmonth_sure_click()
            time.sleep(1)
            #选择拆分的字段
            with allure.step('选择拆分字段：{}'.format(dic['splitField'])):
                list_Page.split_field_click(dic['splitField'])
        else:
            with allure.step('选择不拆分'):
                list_Page.split_not_click()
            if 'spilt_sql' in dic:
                if '${month' in dic['spilt_sql'] or '${day' in dic['spilt_sql']:
                    with allure.step('sql中含有变量，选择替换方式：{}，替换值：{}'.format(dic['replaceType'],dic['replaceTime'])):
                        res = list_Page.replace_acctmonth(dic['replaceType'],dic['replaceTime'])
                        if 'success' in res:
                            list_Page.replace_acctmonth_sure_click()

        #增加用户
        for splitInfo in dic['splitInfo']:
            with allure.step('添加{} 拆分项：{}'.format(splitInfo['splitWay'],splitInfo['splitStaff'])):
                #增加本人下载权限
                if Test_List_Page.staff_name not in splitInfo['splitStaff']:
                    splitInfo['splitStaff'].append(Test_List_Page.staff_name)

                for staff in splitInfo['splitStaff']:
                    list_Page.search_staff(staff)
                    time.sleep(1)
                    list_Page.staff_drag(splitInfo['splitWay'],staff,dic['listSplit'])

        #点击提交
        with allure.step('提交'):
            list_Page.submit_click()
            time.sleep(0.2)
        #判断是否提交成功
        suc = list_Page.alert_tip()
        assert '清单发布成功' in  suc
        time.sleep(0.5)
        list_Page.alert_btn_click()


    @allure.story('清单查询')
    @pytest.mark.run(order = 2)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    # @pytest.mark.skip(reason='')
    # @pytest.mark.parametrize('dic',param.list_data)
    def test_list_search(self,list_search,to_parent_frame):

        list_Page = ListPage(list_search)
        
        list_results = list_Page.get_list_names(Test_List_Page.lists)

        for list_build in Test_List_Page.lists:
            for list_result in list_results:
                if list_build == list_result['listName']:
                    # is_exist = True
                    if list_result['listCycle'] == '是':
                        assert list_result['listResult'] == '审核成功'
                    elif list_result['listCycle'] == '否':
                        assert list_result['listResult'] == '拆分成功'
                    




    @allure.story('清单下载')
    @pytest.mark.run(order = 3)
    # @pytest.mark.flaky(reruns=1,reruns_delay=1)
    # @pytest.mark.skip(reason='')
    # @pytest.mark.parametrize('dic',param.list_data)
    def test_list_download(self,list_download,to_parent_frame):

        list_Page = ListPage(list_download)
        
        list_results = list_Page.get_list_names_download(Test_List_Page.lists)

        for list_build in Test_List_Page.lists:
            for list_result in list_results:
                if list_build == list_result['listName']:
                    assert list_result['result'] == True


                    

        


# if __name__ == "__main__":
#     pytest.main(['-s','test_listBuild_page.py'])
