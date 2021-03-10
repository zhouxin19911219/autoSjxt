#! /usr/bin/python
#coding:utf-8

import sys
sys.path.append('.')
import pytest
from pages.loginPage import LoginPage
from pages.indexPage import IndexPage
from pages.labelPage import LabelPage
from pages.reportDesignPage import ReportDesignPage
from common import param
import time
from selenium import webdriver
import datetime
import os

import allure


@allure.feature('标签库查询')
class Test_Label_Page():
    # global staff

    def label_source_select(self,label_Page,reportDesignPage,group,sql,*groupNames):
        if len(groupNames) != 0:
            groupName = groupNames[0]
        if group =='已传':
            label_Page.uploaded_user_click()
            tables = label_Page.uploaded_users_click(groupName)
            label_Page.uploaded_user_btn_click()
            if 'inner' in tables:
                sql_inner = "select user_flag from label_into_user_group where INTO_ID='"+tables['inner_id']+"'"
                datasource = param.om_datasource
                result = reportDesignPage.sql_search_pubulic(datasource,sql_inner)
                if result[0] == '1':
                    tables['inner_type'] = 'user_id'
                elif result[0] == '2':
                    tables['inner_type'] = 'user_number'
                sql = sql + ' '+ tables['inner_type']+' in ( select user_id from anrpt.'+tables['inner']+' ) and '
            if 'tichu' in tables:
                sql_tichu = "select user_flag from label_into_user_group where INTO_ID='"+tables['tichu_id']+"'"
                datasource = param.om_datasource
                result = reportDesignPage.sql_search_pubulic(datasource,sql_tichu)
                if result[0] == '1':
                    tables['tichu_type'] = 'user_id'
                elif result[0] == '2':
                    tables['tichu_type'] = 'user_number'
                sql = sql + ' '+ tables['tichu_type']+' not in ( select user_id from anrpt.'+tables['tichu']+' ) and '
        
        elif group =='已存':
            label_Page.saved_user_click()  
            if type(groupName) is list:
                groupName=groupName[0]
            time.sleep(0.5)
            saved_sql = label_Page.saved_users_click(groupName)
            if saved_sql is None:
                print('已存数据没有找到：'+groupName)
            else:
                sql = sql + ' user_id_t in (select labellibaliasu.user_id_t from ( '+saved_sql+' ) labellibaliasu ) and '
                label_Page.saved_user_btn_click()

        elif group == '全量':
            label_Page.all_user_click()

        time.sleep(1)
        return sql


    def label_search(self,label_Page,reportDesignPage,sourceInfo,tabel_sql,condition_sql,i,length,is_split_sql):
        
        with allure.step('选择数据源：{}{}'.format(sourceInfo['source'],sourceInfo['acct_month'])):
            label_Page.label_data_type(sourceInfo['sourceType'])
            label_Page.label_source_select(sourceInfo['sourceType'],sourceInfo['source'])
            source_id = label_Page.get_label_source(sourceInfo['sourceType'])
        # source = cont_mysql_db.get_label_source_tabel(source_id)
        dataFormat = ''
        if is_split_sql == True:
            sql = "select source_id,source_table from dvpomdb01.label_source_def where SOURCE_ID = "+source_id+" "
            datasource = param.om_datasource
            source = reportDesignPage.sql_search_pubulic(datasource,sql)

            tabel_sql = tabel_sql + source[1].replace('${date}',sourceInfo['acct_month']) +' as '
            table_as_name = ''
            if sourceInfo['sourceType'] == '日':
                dataFormat = 'YYYYMMDD'
                table_as_name = 'labellibaliasd'
            elif sourceInfo['sourceType'] == '月':
                dataFormat = 'YYYYMM'
                table_as_name = 'labellibaliasm'
            tabel_sql = tabel_sql + table_as_name 
            if i != length:
                tabel_sql = tabel_sql +  ' , '
            elif i == length and length == 1:
                tabel_sql = tabel_sql +' where 1=1 and '
            elif i == length and length != 1:
                tabel_sql = tabel_sql +' where labellibaliasm.user_id_t = labellibaliasd.user_id_t and '

            staff_grade = Test_Label_Page.staff[1]
            if staff_grade!='21':
                condition_sql = condition_sql + ' labellibaliasm.city_code = \''+ staff_grade +'\' and ' #增加地市过滤
            condition_sql = condition_sql+'(' #条件增加括号

        else:
            if sourceInfo['sourceType'] == '日':
                dataFormat = 'YYYYMMDD'
            elif sourceInfo['sourceType'] == '月':
                dataFormat = 'YYYYMM'

        time.sleep(0.5)
        label_Page.select_acct_month(sourceInfo['sourceType'],dataFormat,sourceInfo['acct_month'])

        
        if 'labelInfo' in sourceInfo and len(sourceInfo['labelInfo']) !=0:
            l = len(sourceInfo['labelInfo'])
            for label in sourceInfo['labelInfo']:
                l = l -1
                if 'labelFile' in label and label['labelFile']!='':
                    #点击上级目录
                    with allure.step('点击上级目录{}'.format(label['labelFile'])):
                        label_Page.file_click(sourceInfo['sourceType'],label['labelFile'])
                    
                elif 'labelsearch' not in label:
                    if 'searchlabel' not in label:
                        with allure.step('点击标签名查询{}'.format(label['labelName'])):
                            label_Page.label_search(sourceInfo['sourceType'],'标签名',label['labelName'])
                    else:
                        with allure.step('点击标签名查询{}'.format(label['labelName'])):
                            label_Page.label_search(sourceInfo['sourceType'],'标签名',label['searchlabel'])   
                else:      
                    #点击搜索框搜索
                    with allure.step('点击{}搜索{}'.format(label['labelsearch'],label['labelName'])):  
                        label_Page.label_search(sourceInfo['sourceType'],label['labelsearch'],label['searchlabel'])
                    
                time.sleep(0.2)
                if True == label_Page.label_exist(label['labelName']):
                    label['labelValue_log']= []
                    if 'labelValue' not in label:
                        for select in label['labelSelect']:
                            label['labelValue_log'].append(select['labelValue'])
                    else:
                        label['labelValue_log'] = label['labelValue']
                    with allure.step('点击枚举值{}'.format(label['labelValue_log'])):
                        if '枚举' == label['labelType']:
                            label_Page.enum_click(label['labelName'],label['labelValue'])

                            # labelCode = cont_mysql_db.get_label_code(label['labelName'],source_id)

                            if is_split_sql == True:
                                sql = "SELECT label_code from dvpomdb01.label_config_def where label_name='"+label['labelName']+"' and LAB_SOURCE='"+source_id+"' "
                                datasource = param.om_datasource
                                labelCode = reportDesignPage.sql_search_pubulic(datasource,sql)[0]
                                condition_sql = condition_sql +' ( '+  table_as_name+'.'+labelCode +' in ('+ str(label['labelValue']).replace(']','').replace('[','') +') ) '
                                if l != 0 :
                                    condition_sql = condition_sql + 'and'
                        
                        elif '数值' == label['labelType']:
                            label_Page.num_click(label['labelName'],label['labelValue'])                
                            if is_split_sql == True:
                                sql = "SELECT label_code from dvpomdb01.label_config_def where label_name='"+label['labelName']+"' and LAB_SOURCE='"+source_id+"' "
                                datasource = param.om_datasource
                                labelCode = reportDesignPage.sql_search_pubulic(datasource,sql)[0]
                                condition_sql = condition_sql +' ( '+ table_as_name+'.'+labelCode +' '+str(label['labelValue']).replace(']','').replace('[','').replace(',',' ').replace('\'','').replace('and' , 'and '+table_as_name+'.'+labelCode)+' ) '
                                if l != 0 :
                                    condition_sql = condition_sql + 'and'


                        elif '时间' in label['labelType']:
                            label_Page.label_btn_click(label['labelName'])
                            label_format = label_Page.get_format(label['labelValue'])
                            label_Page.time_click(label['labelName'],label_format,label['labelValue'])
                            if is_split_sql == True:
                                sql = "SELECT label_code from dvpomdb01.label_config_def where label_name='"+label['labelName']+"' and LAB_SOURCE='"+source_id+"' "
                                datasource = param.om_datasource
                                labelCode = reportDesignPage.sql_search_pubulic(datasource,sql)[0]

                                if (len(label['labelValue']) == 1) or ( len(label['labelValue']) == 2 and label['labelValue'][1] == ''):
                                    condition_sql = condition_sql  +' ( '+ table_as_name+'.'+labelCode +' >= '+str(label['labelValue'][0])+' ) '
                                elif len(label['labelValue']) == 2 and label['labelValue'][0] == '':
                                    condition_sql = condition_sql  +' ( '+ table_as_name+'.'+labelCode +' <= '+str(label['labelValue'][1])+' ) '
                                else:
                                    condition_sql = condition_sql +' ( '+ table_as_name+'.'+labelCode +' between '+str(label['labelValue']).replace(']','').replace('[','').replace(',',' and ')+' ) '
                                if l != 0 :
                                    condition_sql = condition_sql + 'and'


                        elif '大枚举' in label['labelType']:
                            label_Page.bigCode_click(label['labelName'],label['labelValue'],label['inverse'])

                            if is_split_sql == True:
                                sql = "SELECT label_code from dvpomdb01.label_config_def where label_name='"+label['labelName']+"' and LAB_SOURCE='"+source_id+"' "
                                datasource = param.om_datasource
                                labelCode = reportDesignPage.sql_search_pubulic(datasource,sql)[0]
                                condition_sql = condition_sql +' '+  table_as_name+'.'+labelCode
                                if '是' == label['inverse'] :
                                    condition_sql = condition_sql +' not '
                                label_Page.file_content(label['labelValue'])
                                condition_sql = condition_sql +' in ('+ label_Page.file_content(label['labelValue']) +') '
                                if l != 0 :
                                    condition_sql = condition_sql + 'and'


                        elif '大数量枚举' in label['labelType']:
                            if 'labelValue' not in label:
                                label['labelValue']=''
                            if 'labelSelect' not in label:
                                label['labelSelect']=''
                            labels,id = label_Page.enum_bigCode_click(label['labelName'],label['labelValue'],label['inverse'],label['labelSelect'])

                            if is_split_sql == True:
                                sql = "SELECT label_code from dvpomdb01.label_config_def where label_name='"+label['labelName']+"' and LAB_SOURCE='"+source_id+"' "
                                datasource = param.om_datasource
                                labelCode = reportDesignPage.sql_search_pubulic(datasource,sql)[0]
                                condition_sql = condition_sql +' '+  table_as_name+'.'+labelCode 
                                if '是' == label['inverse'] :
                                    condition_sql = condition_sql +' not '
                                condition_sql = condition_sql + ' in ('   
                                if label['labelValue']!='':
                                    condition_sql = condition_sql + label_Page.file_content(label['labelValue'])+ ','
                                condition_sql = condition_sql + ','.join("'"+str(i)+"'" for i in labels) +') '
                                if l != 0 :
                                    condition_sql = condition_sql + 'and'
                        #关闭type=5的下钻图层
                        label_Page.close_type5()
                        label_Page.search_label_clear(sourceInfo['sourceType'])
                        label_Page.search_label_btn(sourceInfo['sourceType'])
        if is_split_sql == True:                    
            condition_sql = condition_sql +") "
            if i != length:
                condition_sql = condition_sql +" and "
        return tabel_sql,condition_sql



    @allure.story('查询用户信息')
    @pytest.mark.run(order=1)
    def test_get_staff_info(self,report_design,to_parent_frame):
        reportDesignPage = ReportDesignPage(report_design)
        sql = "select staff_no,grade_value from sys_staff staff,sys_staff_grade_rel rel where rel.STAFF_ID = staff.STAFF_ID and staff.STAFF_NO='"+ param.staff_no +"' "
        with allure.step('执行sql查询用户信息：{}'.format(sql)):
            datasource = param.sys_datasource
            Test_Label_Page.staff = reportDesignPage.sql_search_pubulic(datasource,sql)
        with allure.step('用户{}所属地市：{}'.format(Test_Label_Page.staff[1],Test_Label_Page.staff[1])):
            pass
     

    @allure.story('上传用户')
    @pytest.mark.run(order=2)
    # @pytest.mark.skip(reason='')
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize("dic",param.data_upload)
    def test_upload_user(self,label_lib,to_parent_frame,dic):
        '''
        ==============上传用户==================
        '''
        #上传用户
        if dic is not None:
            label_Page = LabelPage(label_lib)
            time.sleep(1)
            with allure.step('点击上传按钮'):
                label_Page.upload_user_click()
            
            with allure.step('选择上传类型：{}'.format(dic['dataType'])):
                label_Page.upload_dataType_click(dic['dataType'])
            label_Page.upload_user_sendkeys(dic['uploadname']+datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            if dic['is_joint'] == 0 :
                label_Page.upload_user_notinner_click()

            label_Page.upload_user_file(dic['uploadfile'])
            label_Page.upload_user_btn()
            time.sleep(1)
            label_Page.wait_alert()
            result = label_Page.alert_tip()
            with allure.step('上传文件结果：{}'.format(result)):
                if '上传成功' in result:
                    print('文件上传成功')
                    label_Page.alert_btn_click()
                else:
                    print('文件上传失败')
                    label_Page.alert_btn_click()

            label_Page.upload_user_remark(dic['uploadremark'])
            time.sleep(2)
            label_Page.upload_user_submit_click()
            alert = label_Page.alert_tip()
            with allure.step('保存上传结果：{}'.format(alert)):
                if '保存成功' in alert:
                    label_Page.alert_btn_click()
                assert '保存成功' in alert





    @allure.story('选择全量/已传/已存再已存')
    @pytest.mark.run(order=3)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize("dic",param.data_uploaded)
    def test_uploadedUser_search(self,label_lib,to_parent_frame,dic):
        '''
        ==============选择全量/已传/已存再已存==================
        '''  
        if dic is not None: 
            label_Page =  LabelPage(label_lib)
            reportDesignPage = ReportDesignPage(label_lib)
            is_split_sql = False
            time.sleep(1)       
            sql = 'select to_char(COUNT (1) , \'999,999,999,999,999,999\') from '
            tabel_sql,condition_sql='',''
            i = 0
            l = len(dic['sourceInfo'])
            for sourceInfo in dic['sourceInfo']:
                i = i + 1
                with allure.step('数据源选择：{}{}'.format(sourceInfo['source'],sourceInfo['acct_month'])):
                    tabel_sql,condition_sql = self.label_search(label_Page,reportDesignPage,sourceInfo,tabel_sql,condition_sql,i,l,is_split_sql)
            join_sql = ''
            if 'group' in dic and dic['group']!='全量':
                with allure.step('选择{}数据：{}'.format(dic['group'],dic['groupName'])):
                    join_sql= self.label_source_select(label_Page,reportDesignPage,dic['group'],join_sql,dic['groupName'])
            else:
                with allure.step('选择全量数据'):
                    join_sql = self.label_source_select(label_Page,reportDesignPage,'全量',join_sql)
            #点击查询
            with allure.step('点击查询'):
                label_Page.query_data_btn_click()
                label_Page.alert_btn_click()

            with allure.step('点击保存结果'):   
                label_Page.save_user_click()
                label_Page.save_user_name_sendkeys(dic['savedName']+datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
                label_Page.save_user_expiration_time(dic['savedExpirationTime'])
                label_Page.save_user_remark_sendkeys(dic['savedName']+datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

                label_Page.save_user_submit_click()
                alert = label_Page.alert_tip()
                if '保存成功' in alert:
                    label_Page.alert_btn_click()
                assert '保存成功' in alert
            

   
    @allure.story('标签库混合查询')
    @pytest.mark.run(order=4)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize('dic',param.labellib_data)
    def test_label_search(self,label_lib,to_parent_frame,dic):
        '''
        ==============标签库混合查询==================
        '''
        if dic is not None:
            label_Page = LabelPage(label_lib)
            reportDesignPage = ReportDesignPage(label_lib)
            is_split_sql = True
            time.sleep(1)
            sql = 'select to_char(COUNT (1) , \'999,999,999,999,999,999\') from '
            tabel_sql,condition_sql='',''
            i = 0
            l = len(dic['sourceInfo'])
            for sourceInfo in dic['sourceInfo']:
                i = i + 1
                with allure.step('数据源选择：{}{}'.format(sourceInfo['source'],sourceInfo['acct_month'])):
                    tabel_sql,condition_sql = self.label_search(label_Page,reportDesignPage,sourceInfo,tabel_sql,condition_sql,i,l,is_split_sql)

            join_sql = ''
            if 'group' in dic and dic['group']!='全量':
                with allure.step('选择{}数据：{}'.format(dic['group'],dic['groupName'])):
                    join_sql= self.label_source_select(label_Page,reportDesignPage,dic['group'],join_sql,dic['groupName'])
            else:
                with allure.step('选择全量数据'):
                    join_sql = self.label_source_select(label_Page,reportDesignPage,'全量',join_sql)

            #点击查询按钮
            with allure.step('点击查询'):
                label_Page.query_data_btn_click()
                label_Page.alert_btn_click()


            sql = sql + tabel_sql + join_sql + condition_sql
            datasource = param.gp_datasource
            with allure.step('拼接sql查询:{}'.format(sql)):
                res = reportDesignPage.sql_search_pubulic(datasource,sql)
                # res = cont_gp_db.get_label_result(sql)
                result = label_Page.get_return_count_table_info()
            
            for sourceInfo in dic['sourceInfo']:
                assert sourceInfo['acct_month']+'('+sourceInfo['sourceType']+')' in result[1]
            with allure.step('sql查询结果：{},页面查询结果：{}'.format(str(res[0]).replace(' ',''),result)):
                assert str(res[0]).replace(' ','') in result   




    @allure.story('保存筛选')
    @pytest.mark.run(order=5)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize("dic",param.save_label_filter_data)
    def test_save_label_filter(self,label_lib,to_parent_frame,dic):
        '''
        ==============保存筛选==================
        '''
        if dic is not None:
            label_Page = LabelPage(label_lib)
            reportDesignPage = ReportDesignPage(label_lib)
            is_split_sql = False
            time.sleep(1)
            sql = 'select to_char(COUNT (1) , \'999,999,999,999,999,999\') from '

            tabel_sql,condition_sql='',''
            i = 0
            l = len(dic['sourceInfo'])
            for sourceInfo in dic['sourceInfo']:
                i = i + 1
                with allure.step('数据源选择：{}{}'.format(sourceInfo['source'],sourceInfo['acct_month'])):
                    tabel_sql,condition_sql = self.label_search(label_Page,reportDesignPage,sourceInfo,tabel_sql,condition_sql,i,l,is_split_sql)
            join_sql = ''
            if 'group' in dic and dic['group']!='全量':
                with allure.step('选择{}数据：{}'.format(dic['group'],dic['groupName'])):
                    join_sql= self.label_source_select(label_Page,reportDesignPage,dic['group'],join_sql,dic['groupName'])
            else:
                with allure.step('选择全量数据'):
                    join_sql = self.label_source_select(label_Page,reportDesignPage,'全量',join_sql)

            with allure.step('点击查询'):
                label_Page.query_data_btn_click()
                label_Page.alert_btn_click()
            
            #统计分析
            if 'dimension' in dic and dic['dimension'] != '':
                with allure.step('点击统计分析'):
                    label_Page.count_analy_btn_click()
                    time.sleep(0.5)
                    #切换账期
                    if 'analySource' in dic:
                        label_Page.select_analy_source(dic['analySource'])
                    #点击维度
                    for d in dic['dimension']:
                        with allure.step('点击维度：{}'.format(d)):
                            label_Page.dim_input_click(d)
                    time.sleep(0.5)
                    label_Page.target_panel_click()
                    #点击指标
                    for t in dic['target']:
                        with allure.step('点击指标：{}'.format(t)):
                            label_Page.quota_input_click(t)
                    time.sleep(0.5)
                    label_Page.count_data_btn_click()
            time.sleep(1)
            #点击保存筛选按钮
            with allure.step('点击保存筛选按钮'):
                label_Page.save_filter_click()
                if param.staff_no not in dic['filterStaff']:
                    dic['filterStaff'].append(param.staff_no)
            with allure.step('结果验证'):
                result = label_Page.save_filter_info(dic['filterName']+datetime.datetime.now().strftime('%Y%m%d%H%M%S'),dic['filterType'],dic['remark'],False,dic['filterStaff']) 
                if 'success' == result:
                    label_Page.filter_staff_btn_click()
                    
                    alert = label_Page.alert_tip()
                    with allure.step('保存筛选结果：{}'.format(alert)):
                        if '保存成功' in alert:
                            label_Page.alert_btn_click()
                        assert '保存成功' in alert


    @allure.story('点击模板查询')
    @pytest.mark.run(order=6)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize("dic",param.filter_user)
    def test_filter_user_search(self,label_lib,to_parent_frame,dic):
        
        '''
        ==============点击模板查询==================
        '''
        if dic is not None:
            label_Page = LabelPage(label_lib)
            reportDesignPage = ReportDesignPage(label_lib)
            is_split_sql = False
            time.sleep(1)
            #选择模板
            with allure.step('选择模板'):
                label_Page.filter_user_click()
                label_Page.select_filter(dic['type'],dic['name'])
                #关闭模板
                label_Page.filter_user_click()

            sql = 'select to_char(COUNT (1) , \'999,999,999,999,999,999\') from '

            tabel_sql,condition_sql='',''
            i = 0
            l = len(dic['sourceInfo'])
            for sourceInfo in dic['sourceInfo']:
                i = i + 1
                with allure.step('数据源选择：{}{}'.format(sourceInfo['source'],sourceInfo['acct_month'])):
                    tabel_sql,condition_sql = self.label_search(label_Page,reportDesignPage,sourceInfo,tabel_sql,condition_sql,i,l,is_split_sql)
            join_sql = ''
            if 'group' in dic and dic['group']!='全量':
                with allure.step('选择{}数据：{}'.format(dic['group'],dic['groupName'])):
                    join_sql= self.label_source_select(label_Page,reportDesignPage,dic['group'],join_sql,dic['groupName'])
            else:
                with allure.step('选择全量数据'):
                    join_sql = self.label_source_select(label_Page,reportDesignPage,'全量',join_sql)

            #点击查询按钮
            with allure.step('点击查询'):
                label_Page.query_data_btn_click()
                label_Page.alert_btn_click()
                result = label_Page.get_return_count_table_info()
            with allure.step('结果验证'):
                assert dic['sourceInfo'][0]['acct_month']+'('+dic['sourceInfo'][0]['sourceType']+')' in result[1]
        



    @allure.story('下载数据')
    @pytest.mark.run(order=7)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize("dic",param.data_download)
    def test_download_data(self,label_lib,to_parent_frame,dic):
        '''
        ==============下载数据==================
        '''
        if dic is not None:
            label_Page = LabelPage(label_lib)
            reportDesignPage = ReportDesignPage(label_lib)
            is_split_sql = False
            time.sleep(1)
            sql = 'select to_char(COUNT (1) , \'999,999,999,999,999,999\') from '

            tabel_sql,condition_sql='',''
            i = 0
            l = len(dic['sourceInfo'])
            for sourceInfo in dic['sourceInfo']:
                i = i + 1
                with allure.step('数据源选择：{}{}'.format(sourceInfo['source'],sourceInfo['acct_month'])):
                    tabel_sql,condition_sql = self.label_search(label_Page,reportDesignPage,sourceInfo,tabel_sql,condition_sql,i,l,is_split_sql)

            join_sql = ''
            if 'group' in dic and dic['group']!='全量':
                with allure.step('选择{}数据：{}'.format(dic['group'],dic['groupName'])):
                    join_sql= self.label_source_select(label_Page,reportDesignPage,dic['group'],join_sql,dic['groupName'])
            else:
                with allure.step('选择全量数据'):
                    join_sql = self.label_source_select(label_Page,reportDesignPage,'全量',join_sql)
            #点击查询
            with allure.step('点击查询'):
                label_Page.query_data_btn_click()
                label_Page.alert_btn_click()
                label_Page.get_data_btn_click()
            if 'download_data' in dic:   
                with allure.step('下载数据'):
                    for download_data in dic['download_data']:
                        if 'source' in download_data:
                            label_Page.change_source_download(download_data['source'],'普通')
                            time.sleep(0.5)
                        for label in download_data['download']:
                            label_Page.label_btn_click(label)   
                        label_Page.add_user_click()
            if 'addTemplate' in dic:
                with allure.step('保存模板'):
                    temTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                    if 'templateSub' not in dic['addTemplate'] :
                        dic['addTemplate']['templateSub']=temTime
                    if 'staffs' in dic['addTemplate'] :
                        dic['addTemplate']['staffs'].append(param.staff_no)
                    else:
                        dic['addTemplate']['staffs'] = []
                        dic['addTemplate']['staffs'].append(param.staff_no)
                    result = label_Page.add_template(dic['addTemplate']['templateName']+temTime,dic['addTemplate']['templateType'],dic['addTemplate']['templateSub'],'普通',dic['addTemplate']['staffs'])
                    if result == 'success':
                        label_Page.download_filter_staff_btn_click()
                        alert = label_Page.alert_tip()
                        if '保存成功' in alert:
                            label_Page.alert_btn_click()
                        assert '保存成功' in alert     
            time.sleep(1) 
            if 'selectTemplate' in dic:
                with allure.step('选择模板'):
                    label_Page.select_template(dic['selectTemplate']['templateType'],dic['selectTemplate']['templateName'],'普通')
            
            with allure.step('点击下载'):
                label_Page.export_data_btn_click()

            if label_Page.alert_is_exist() == True:
                tip = label_Page.alert_tip()
                with allure.step('弹框提示{}'.format(tip)):  
                    label_Page.alert_btn_click()
            else:
                with allure.step('进入下载路径自行查看下载结果是否正常'):  
                    print('点击下载结果没有弹框，进入下载路径自行查看下载结果是否正常')

            
            


    @allure.story('统计分析')
    @pytest.mark.run(order=8)  
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize("dic",param.data_analy)
    def test_count_analy(self,label_lib,to_parent_frame,dic):
        '''
        ==============统计分析==================
        '''
        if dic is not None:
            #统计分析
            label_Page = LabelPage(label_lib)
            reportDesignPage = ReportDesignPage(label_lib)
            is_split_sql = False 
            time.sleep(1)

            sql = 'select to_char(COUNT (1) , \'999,999,999,999,999,999\') from '

            tabel_sql,condition_sql='',''
            i = 0
            l = len(dic['sourceInfo'])
            for sourceInfo in dic['sourceInfo']:
                i = i + 1
                with allure.step('数据源选择：{}{}'.format(sourceInfo['source'],sourceInfo['acct_month'])):
                    tabel_sql,condition_sql = self.label_search(label_Page,reportDesignPage,sourceInfo,tabel_sql,condition_sql,i,l,is_split_sql)

            join_sql = ''
            if 'group' in dic and dic['group']!='全量':
                with allure.step('选择{}数据：{}'.format(dic['group'],dic['groupName'])):
                    join_sql= self.label_source_select(label_Page,reportDesignPage,dic['group'],join_sql,dic['groupName'])
            else:
                with allure.step('选择全量数据'):
                    join_sql = self.label_source_select(label_Page,reportDesignPage,'全量',join_sql)
            #点击查询
            with allure.step('点击查询'):
                label_Page.query_data_btn_click()
                label_Page.alert_btn_click()

            #点击查询
            with allure.step('点击统计分析'):
                label_Page.count_analy_btn_click()
                time.sleep(0.5)
                #切换账期
                if 'analySource' in dic:
                    label_Page.select_analy_source(dic['analySource'])
                for d in dic['dimension']:
                    with allure.step('点击维度：{}'.format(d)):
                        label_Page.dim_input_click(d)
                        time.sleep(0.5)
                label_Page.target_panel_click()

                for t in dic['target']:
                    with allure.step('点击指标：{}'.format(t)):
                        label_Page.quota_input_click(t)
                        time.sleep(0.5)
                label_Page.count_data_btn_click()
            

            analy_result = label_Page.analy_result()

            for d in dic['dimension']:
                with allure.step('统计分析结果：{}'.format(d)) :
                    assert d in analy_result
 


    @allure.story('清理已存/已传/保存筛选')
    @pytest.mark.run(order=9)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    # @pytest.mark.skip(reason= 'periodic cleaning')
    @pytest.mark.parametrize("dic",param.data_clean)
    def test_data_clean(self,label_lib,to_parent_frame,dic):
        '''
        ==============清理已存/已传/保存筛选==================
        '''
        if dic is not None:
            #模板
            label_Page =  LabelPage(label_lib)
            time.sleep(1)
            label_Page.filter_user_click()
            time.sleep(1)
            for filter in dic['filter_name']:
                with allure.step('清理模板：{}'.format(filter)):
                    label_Page.delete_filter(filter['type'],filter['name'])
            time.sleep(0.5)


            #已存用户
            label_Page.saved_user_click()  
            for name in dic['saved_name']:
                time.sleep(0.5)
                with allure.step('清理已存数据：{}'.format(name)):
                    label_Page.saved_users_click(name)
                    result = label_Page.delete_saved_users_click(name)
            label_Page.saved_close_btn_click()
            time.sleep(0.5)
                

            #已传用户删除测试数据
            label_Page.uploaded_user_click()
            for name in dic['uploaded_name']:
                with allure.step('清理已传数据：{}'.format(name)):
                    label_Page.uploaded_users_click(name)
            result = label_Page.delete_uploaded_users_click(dic['uploaded_name'])
            label_Page.uploaded_close_btn_click()
            time.sleep(0.5)





            

