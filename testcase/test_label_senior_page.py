#! /usr/bin/python
# coding=utf-8

import allure
import sys 
sys.path.append('.')
from pages.labelPage import LabelPage
from pages.reportDesignPage import ReportDesignPage
import time
from common import param
import pytest
# from db import cont_mysql_db
# from db.cont_gp_db import get_label_result
import datetime




@allure.feature('标签库高级版')
class Test_labelSenior_Page():
    global staff 
    
    def label_group_select(self,label_Page,reportDesignPage,group,groupName,sql,inner_sql):
        if group =='已传':
            label_Page.uploaded_user_click()
            tables = label_Page.uploaded_users_click(groupName)
            label_Page.uploaded_user_btn_click()
            if 'inner' in tables:
                sql_inner = "select user_flag from label_into_user_group where INTO_ID='"+tables['inner_id']+"'"
                datasource = param.om_datasource
                result = reportDesignPage.sql_search_pubulic(datasource,sql_inner)
                tables['inner_type'] = 'user_id'
                if result[0] == '1':
                    tables['inner_type'] = 'user_id'
                elif result[0] == '2':
                    tables['inner_type'] = 'user_number'
                    
                sql = sql +' ( select '+ tables['inner_type']+' from anrpt.'+tables['inner']+' ) as  labellibaliast0 ,'     
            else:
                sql_tichu = "select user_flag from label_into_user_group where INTO_ID='"+tables['tichu_id']+"'"
                datasource = param.om_datasource
                result = reportDesignPage.sql_search_pubulic(datasource,sql_tichu)
                if result[0] == '1':
                    tables['tichu_type'] = 'user_id'
                elif result[0] == '2':
                    tables['tichu_type'] = 'user_number'
                sql = sql +' ( select '+ tables['tichu_type']+' from anrpt.'+tables['tichu']+' )  as  labellibaliast0 ,'
            inner_sql = inner_sql + ' labellibaliast0'+'.user_id = labellibaliast1'+'.user_id and '
        elif group =='已存':
            label_Page.saved_user_click()  
            if type(groupName) is list:
                groupName=groupName[0]
            saved_sql = label_Page.saved_users_click(groupName)
            label_Page.saved_user_btn_click()
            sql = sql +' (select labellibaliasu.user_id_t from ( '+saved_sql+' ) labellibaliasu ) as  labellibaliast0,'
            inner_sql = inner_sql + ' labellibaliast0'+'.user_id_t = labellibaliast1'+'.user_id_t and '
        return sql,inner_sql


    def label_source_select(self,label_Page,reportDesignPage,sourceInfo,tabel_sql,inner_sql,source_i,source_l,is_split_sql):
        label_Page.label_data_type(sourceInfo['sourceType'])
        label_Page.label_source_select(sourceInfo['sourceType'],sourceInfo['source'])
        source_id = label_Page.get_label_source(sourceInfo['sourceType'])
        dataFormat = 'YYYYMM'
        if sourceInfo['sourceType'] == '日':
            dataFormat = 'YYYYMMDD'

        label_Page.select_acct_month(sourceInfo['sourceType'],dataFormat,sourceInfo['acct_month'])
        time.sleep(0.2)
        label_Page.add_acct_month_click(sourceInfo['sourceType'])

        # source = cont_mysql_db.get_label_source_tabel(source_id)
        if is_split_sql == True:
            sql = "select source_id,source_table from dvpomdb01.label_source_def where SOURCE_ID = '"+source_id+"' "
            datasource = param.om_datasource
            source = reportDesignPage.sql_search_pubulic(datasource,sql)

            table = source[1].replace('${date}',sourceInfo['acct_month'])
            tabel_as_name = 'labellibaliast' + str(source_i) 
            tabel_sql = tabel_sql + table +' '+' as '+tabel_as_name

            if source_i != source_l:
                tabel_sql = tabel_sql + ' , '

            if source_i != source_l:
                inner_sql = inner_sql + ' labellibaliast'+str(source_i)+'.user_id_t = labellibaliast'+str(source_i+1)+'.user_id_t and '

            staff_grade = Test_labelSenior_Page.staff[1]
            if staff_grade!='21':
                inner_sql = inner_sql + 'labellibaliast'+str(source_i)+'.city_code = \''+ staff_grade +'\' and ' #增加地市过滤

        return tabel_sql,inner_sql,source_id


    def label_senior_search(self,label_Page,reportDesignPage,labelInfo,tabels,condition_sql,tabel_name,is_split_sql):
        for label in labelInfo:
            if 'symbol' in label:
                if label['symbol'] == '输入框' and 'value' in label:
                    with allure.step('输入框内容：{}'.format(label['value'])):
                        label_Page.label_symbol_click(label['symbol'])
                        label_Page.set_input_value(label['value'])
                        condition_sql = condition_sql + label['value'] +' '
                else:
                    if label_Page.get_senior_content()[0]!='':
                        with allure.step('符号：{}'.format(label['symbol'])):
                            label_Page.label_symbol_click(label['symbol'])
                            condition_sql = condition_sql + label['symbol'] +' '    
            else:
                if len(tabels) == 3 and 'source' not in label:
                    tabel_as_name = tabels[tabel_name]
                    source_id = tabels[tabel_name+"_sourceId"]
                    label['sourceType'] = tabels[tabel_name+"_sourceType"]
                    label['acct_month'] = tabel_name.split('(')[1].split(')')[0]
                else:
                    tabel_as_name = tabels[label['source']+'('+label['acct_month']+')']
                    source_id = tabels[label['source']+'('+label['acct_month']+')'+'_sourceId']
                
                if 'labelFile' in label and label['labelFile']!='' :
                    #点击上级目录test_label_senior_page.py
                    with allure.step('点击上级目录{}'.format(label['labelFile'])):
                        label_Page.file_click(label['sourceType'],label['labelFile'])
                elif 'labelsearch' not in label:
                    if 'searchlabel' not in label:
                        with allure.step('点击标签名查询{}'.format(label['labelName'])):
                            label_Page.label_search(label['sourceType'],'标签名',label['labelName'])
                    else:
                        with allure.step('点击标签名查询{}'.format(label['labelName'])):
                            label_Page.label_search(label['sourceType'],'标签名',label['searchlabel'])   
                else:      
                    #点击搜索框搜索
                    with allure.step('点击{}搜索{}'.format(label['labelsearch'],label['labelName'])):  
                        label_Page.label_search(label['sourceType'],label['labelsearch'],label['searchlabel'])
                       
                time.sleep(0.2)
                if True == label_Page.label_exist(label['labelName']):
                    label['labelValue_log']= []
                    if 'labelValue' not in label:
                        if 'labelSelect' in label:
                            for select in label['labelSelect']:
                                label['labelValue_log'].append(select['labelValue'])
                        else:
                            label['labelValue_log']=''
                    else:
                        label['labelValue_log'] = label['labelValue']
                    with allure.step('点击枚举值{}'.format(label['labelValue_log'])):
                        # label_Page.label_symbol_click('(')
                        if '枚举' == label['labelType']:
                            # labelCode = label_Page.get_label_code(label['labelName'])  
                            if is_split_sql == True:
                                sql = "SELECT label_code from dvpomdb01.label_config_def where label_name='"+label['labelName']+"' and LAB_SOURCE='"+source_id+"' "
                                datasource = param.om_datasource
                                labelCode = reportDesignPage.sql_search_pubulic(datasource,sql)[0]
                                if 'labelValue' in label:
                                    label_Page.enum_click(label['labelName'],label['labelValue'],label['acct_month'])
                                    condition_sql = condition_sql +' ( '+ tabel_as_name +'.' + labelCode +' in ('+ str(label['labelValue']).replace(']','').replace('[','') +') ) '
                                else:
                                    label_Page.label_btn_click(label['labelName'])
                                    label_Page.click_label_code_save()
                                    condition_sql = condition_sql + tabel_as_name +'.' + labelCode +' '
                            else:
                                if 'labelValue' in label:
                                    label_Page.enum_click(label['labelName'],label['labelValue'],label['acct_month'])
                                else:
                                    label_Page.label_btn_click(label['labelName'])
                                    label_Page.click_label_code_save()
                    
                        elif '数值' == label['labelType']:
                            if is_split_sql == True:
                                sql = "SELECT label_code from dvpomdb01.label_config_def where label_name='"+label['labelName']+"' and LAB_SOURCE='"+source_id+"' "
                                datasource = param.om_datasource
                                labelCode = reportDesignPage.sql_search_pubulic(datasource,sql)[0]
                                if 'labelValue' in label:
                                    label_Page.num_click(label['labelName'],label['labelValue'],label['acct_month'])
                                    condition_sql = condition_sql +' ( '+ tabel_as_name +'.' + labelCode +' '+str(label['labelValue']).replace(']','').replace('[','').replace(',',' ').replace('\'','').replace('and' , 'and '+ tabel_as_name +'.'+labelCode)+' ) '
                                else:
                                    label_Page.label_btn_click(label['labelName'])
                                    label_Page.click_labelData_save()
                                    condition_sql = condition_sql + tabel_as_name +'.' + labelCode +' '
                            else:
                                if 'labelValue' in label:
                                    label_Page.num_click(label['labelName'],label['labelValue'],label['acct_month'])
                                else:
                                    label_Page.label_btn_click(label['labelName'])
                                    label_Page.click_labelData_save()
                                
                    
                        elif '时间' in label['labelType']:
                            label_format = label_Page.get_format(label['labelValue'])
                            if is_split_sql == True:
                                sql = "SELECT label_code from dvpomdb01.label_config_def where label_name='"+label['labelName']+"' and LAB_SOURCE='"+source_id+"' "
                                datasource = param.om_datasource
                                labelCode = reportDesignPage.sql_search_pubulic(datasource,sql)[0]
                            
                                if 'labelValue' in label:
                                    label_Page.time_click(label['labelName'],label_format,label['labelValue'],label['acct_month'])
                                    if (len(label['labelValue']) == 1) or ( len(label['labelValue']) == 2 and label['labelValue'][1] == ''):
                                        condition_sql = condition_sql  +' ( '+ tabel_as_name+'.' + labelCode +' >= \''+str(label['labelValue'][0])+'\' ) '
                                    elif len(label['labelValue']) == 2 and label['labelValue'][0] == '':
                                        condition_sql = condition_sql  +' ( '+ tabel_as_name+'.' + labelCode +' <= \''+str(label['labelValue'][1])+'\' ) '
                                    else:
                                        condition_sql = condition_sql +' ( '+ tabel_as_name+'.' + labelCode +' between '+str(label['labelValue']).replace(']','').replace('[','').replace(',',' and ')+' ) '
                                else:
                                    label_Page.label_btn_click(label['labelName'])
                                    label_Page.click_labelTime_save()
                                    condition_sql = condition_sql + tabel_as_name +'.' + labelCode +' '
                            else:
                                if 'labelValue' in label:
                                    label_Page.time_click(label['labelName'],label_format,label['labelValue'],label['acct_month'])
                                else:
                                    label_Page.label_btn_click(label['labelName'])
                                    label_Page.click_labelTime_save()
                    
                        elif '大枚举' in label['labelType']:
                            if is_split_sql == True:
                                sql = "SELECT label_code from dvpomdb01.label_config_def where label_name='"+label['labelName']+"' and LAB_SOURCE='"+source_id+"' "
                                datasource = param.om_datasource
                                labelCode = reportDesignPage.sql_search_pubulic(datasource,sql)[0]
                                if 'labelValue' in label:
                                    label_Page.bigCode_click(label['labelName'],label['labelValue'],label['inverse'],label['acct_month'])
                                    time.sleep(0.5)
                                    condition_sql = condition_sql + tabel_as_name+'.' +  labelCode 
                                    if '是' == label['inverse'] :
                                        condition_sql = condition_sql +' not '
                                    condition_sql = condition_sql +' in ('+ label_Page.file_content(label['labelValue']) +') '
                                else:
                                    label_Page.label_btn_click(label['labelName'])
                                    label_Page.click_label_code_save()
                                    condition_sql = condition_sql + tabel_as_name +'.' + labelCode +' '
                            else:
                                if 'labelValue' in label:
                                    label_Page.bigCode_click(label['labelName'],label['labelValue'],label['inverse'],label['acct_month'])
                                    time.sleep(0.5)
                                else:
                                    label_Page.label_btn_click(label['labelName'])
                                    label_Page.click_label_code_save()
                    
                        elif '大数量枚举' in label['labelType']:
                            if is_split_sql == True:
                                sql = "SELECT label_code from dvpomdb01.label_config_def where label_name='"+label['labelName']+"' and LAB_SOURCE='"+source_id+"' "
                                datasource = param.om_datasource
                                labelCode = reportDesignPage.sql_search_pubulic(datasource,sql)[0]
                                if 'labelValue' not in label:
                                    label['labelValue']=''
                                if 'labelSelect' not in label:
                                    label['labelSelect']=''
                                if 'labelValue' in label or 'labelSelect' in label:
                                    labels,id = label_Page.enum_bigCode_click(label['labelName'],label['labelValue'],label['inverse'],label['labelSelect'],label['acct_month'])
                                    condition_sql = condition_sql + tabel_as_name+'.' +  labelCode
                                    if '是' == label['inverse'] :
                                        condition_sql = condition_sql +' not '
                                    condition_sql = condition_sql + ' in ('   
                                    if label['labelValue']!='':
                                        condition_sql = condition_sql + label_Page.file_content(label['labelValue'])+ ','
                                    condition_sql = condition_sql + ','.join("'"+str(i)+"'" for i in labels) +') '    
                                else: 
                                    label_Page.label_btn_click(label['labelName'])
                                    label_Page.click_label_code_save()
                                    condition_sql = condition_sql + tabel_as_name +'.' + labelCode +' '
                            else:
                                if 'labelValue' not in label:
                                    label['labelValue']=''
                                if 'labelSelect' not in label:
                                    label['labelSelect']=''

                                if 'labelValue' in label or 'labelSelect' in label:
                                    labels,id = label_Page.enum_bigCode_click(label['labelName'],label['labelValue'],label['inverse'],label['labelSelect'],label['acct_month']) 
                                else: 
                                    label_Page.label_btn_click(label['labelName'])
                                    label_Page.click_label_code_save()

                
                if 'labelSymbol' not in label:
                    label['labelSymbol']=''
                time.sleep(0.5)
                label_Page.label_symbol_click(label['labelSymbol'])
                if is_split_sql == True:
                    condition_sql = condition_sql + ' ' + label['labelSymbol']+ ' '
                #关闭type=5的下钻图层
                label_Page.close_type5()
        return condition_sql





    @allure.story('查询用户信息')
    @pytest.mark.run(order=1)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    def test_get_staff_info(self,report_design,to_parent_frame):
        reportDesignPage = ReportDesignPage(report_design)
        sql = "select staff_no,grade_value from sys_staff staff,sys_staff_grade_rel rel where rel.STAFF_ID = staff.STAFF_ID and staff.STAFF_NO='"+ param.staff_no +"' "
        with allure.step('执行sql查询用户信息：{}'.format(sql)):
            datasource = param.sys_datasource
            Test_labelSenior_Page.staff = reportDesignPage.sql_search_pubulic(datasource,sql)

    @allure.story('高级上传用户')
    @pytest.mark.run(order=2)
    # @pytest.mark.skip(reason = 'ss')
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize("dic",param.data_upload_senior)
    def test_upload_user_senior(self,label_lib,to_parent_frame,dic):
        '''
        ==============上传用户==================
        '''
        if dic is not None:
            #上传用户
            label_Page = LabelPage(label_lib)
            time.sleep(0.5)
            with allure.step('点击高级版按钮'):
                label_Page.senior_button_click()

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
                if '创建成功' in alert:
                    label_Page.alert_btn_click()
                assert '创建成功' in alert



    @allure.story('选择高级全量/已传/已存再已存')
    @pytest.mark.run(order=3)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize("dic",param.data_uploaded_senior)
    def test_uploadedUser_search_senior(self,label_lib,to_parent_frame,dic):
        '''
        ==============选择全量/已传/已存再已存==================
        '''   
        label_Page =  LabelPage(label_lib)
        reportDesignPage = ReportDesignPage(label_lib)
        is_split_sql = False
        time.sleep(0.5)
        with allure.step('点击高级版按钮'):
            label_Page.senior_button_click()
        sql = 'select to_char(COUNT (1) , \'999,999,999,999,999,999\') from '

        tabel_sql,join_sql,inner_sql,condition_sql = ' ',' ',' ',' '
        if 'group' in dic and dic['group']!='全量':
            time.sleep(0.5)
            with allure.step('选择{}数据：{}'.format(dic['group'],dic['groupName'])):
                join_sql,inner_sql = self.label_group_select(label_Page,reportDesignPage,dic['group'],dic['groupName'],join_sql,inner_sql)

        i = 0
        l = len(dic['sourceInfo'])
        tables = {}
        tabel_name = ''
        for sourceInfo in dic['sourceInfo']:
            i = i + 1
            with allure.step('数据源选择：{}{}'.format(sourceInfo['source'],sourceInfo['acct_month'])):
                tabel_sql,inner_sql,source_id = self.label_source_select(label_Page,reportDesignPage,sourceInfo,tabel_sql,inner_sql,i,l,is_split_sql)
                tabel_name = sourceInfo['source']+'('+sourceInfo['acct_month']+')'
                tables[tabel_name] = 'labellibaliast'+str(i)
                tables[tabel_name+"_sourceId"] = source_id
                tables[tabel_name+"_sourceType"] = sourceInfo['sourceType']

        if i == 1:
            condition_sql = self.label_senior_search(label_Page,reportDesignPage,dic['labelInfo'],tables,condition_sql,tabel_name,is_split_sql)
        else:
            condition_sql = self.label_senior_search(label_Page,reportDesignPage,dic['labelInfo'],tables,condition_sql,'',is_split_sql)
           
        #点击查询按钮
        with allure.step('点击查询'):
            label_Page.query_data_btn_click()
            label_Page.alert_btn_click()

        with allure.step('点击保存结果'): 
            label_Page.save_user_click()
            label_Page.save_user_name_sendkeys(dic['savedName']+datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            label_Page.save_user_expiration_time(dic['savedExpirationTime'])
            label_Page.save_user_remark_sendkeys(dic['savedName']+datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

            label_Page.save_user_submit_click()
            
        with allure.step('结果验证'):
            alert = label_Page.alert_tip()
            if '保存成功' in alert:
                label_Page.alert_btn_click()
            assert '保存成功' in alert


    @allure.story('高级版查询')
    @pytest.mark.run(order=4)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize('dic',param.labellib_senior_data)
    def test_label_senior_search(self,label_lib,to_parent_frame,dic):
        '''
        ==============高级版查询==================
        ''' 
        if dic is not None:
            label_Page = LabelPage(label_lib)
            reportDesignPage = ReportDesignPage(label_lib)
            is_split_sql = True
            time.sleep(0.5)
            with allure.step('点击高级版按钮'):
                label_Page.senior_button_click()

            sql = 'select to_char(COUNT (1) , \'999,999,999,999,999,999\') from '

            tabel_sql,join_sql,inner_sql,condition_sql = ' ',' ',' ',' '
            if 'group' in dic and dic['group']!='全量':
                time.sleep(0.5)
                with allure.step('选择{}数据：{}'.format(dic['group'],dic['groupName'])):
                    join_sql,inner_sql = self.label_group_select(label_Page,reportDesignPage,dic['group'],dic['groupName'],join_sql,inner_sql)

            if 'sourceInfo' in dic:
                i = 0
                l = len(dic['sourceInfo'])
                tables = {}
                tabel_name = ''
                for sourceInfo in dic['sourceInfo']:
                    i = i + 1
                    with allure.step('数据源选择：{}{}'.format(sourceInfo['source'],sourceInfo['acct_month'])):
                        tabel_sql,inner_sql,source_id = self.label_source_select(label_Page,reportDesignPage,sourceInfo,tabel_sql,inner_sql,i,l,is_split_sql)
                        tabel_name = sourceInfo['source']+'('+sourceInfo['acct_month']+')'
                        tables[tabel_name] = 'labellibaliast'+str(i)
                        tables[tabel_name+"_sourceId"] = source_id
                        tables[tabel_name+"_sourceType"] = sourceInfo['sourceType']
                #相同数据源账期，取最后一个
                if len(tables) == 3:
                    condition_sql = self.label_senior_search(label_Page,reportDesignPage,dic['labelInfo'],tables,condition_sql,tabel_name,is_split_sql)
                else:
                    condition_sql = self.label_senior_search(label_Page,reportDesignPage,dic['labelInfo'],tables,condition_sql,'',is_split_sql)
            
            #点击查询按钮
            with allure.step('点击查询'):
                label_Page.query_data_btn_click()
                label_Page.alert_btn_click()

            sql = sql + join_sql + tabel_sql + ' where 1=1 and ' + inner_sql + '('+ condition_sql+')'
            datasource = param.gp_datasource
            with allure.step('拼接sql查询:{}'.format(sql)):
                result_sql = reportDesignPage.sql_search_pubulic(datasource,sql)
                result = label_Page.get_return_count_table_info()

                for sourceInfo in dic['sourceInfo']:
                    assert sourceInfo['source']+'('+sourceInfo['acct_month']+')' in result[0]
                with allure.step('sql查询结果：{},页面查询结果：{}'.format(str(result_sql[0]).replace(' ',''),result)):
                    assert str(result_sql[0]).replace(' ','') == result[1]   



    @allure.story('保存筛选')
    @pytest.mark.run(order=5)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize("dic",param.save_label_filter_data_senior)
    def test_save_label_filter_senior(self,label_lib,to_parent_frame,dic):
        '''
        ==============保存筛选==================
        '''
        if dic is not None:
            label_Page = LabelPage(label_lib)
            reportDesignPage = ReportDesignPage(label_lib)
            is_split_sql = False
            time.sleep(0.5)
            with allure.step('点击高级版按钮'):
                label_Page.senior_button_click()

            sql = 'select to_char(COUNT (1) , \'999,999,999,999,999,999\') from '

            tabel_sql,join_sql,inner_sql,condition_sql = ' ',' ',' ',' '
            if 'group' in dic and dic['group']!='全量':
                time.sleep(0.5)
                with allure.step('选择{}数据：{}'.format(dic['group'],dic['groupName'])):
                    join_sql,inner_sql = self.label_group_select(label_Page,reportDesignPage,dic['group'],dic['groupName'],join_sql,inner_sql)

            i = 0
            l = len(dic['sourceInfo'])
            tables = {}
            tabel_name = ''
            for sourceInfo in dic['sourceInfo']:
                i = i + 1
                with allure.step('数据源选择：{}{}'.format(sourceInfo['source'],sourceInfo['acct_month'])):
                    tabel_sql,inner_sql,source_id = self.label_source_select(label_Page,reportDesignPage,sourceInfo,tabel_sql,inner_sql,i,l,is_split_sql)
                    tabel_name = sourceInfo['source']+'('+sourceInfo['acct_month']+')'
                    tables[tabel_name] = 'labellibaliast'+str(i)
                    tables[tabel_name+"_sourceId"] = source_id
                    tables[tabel_name+"_sourceType"] = sourceInfo['sourceType']

            if i == 1:
                condition_sql = self.label_senior_search(label_Page,reportDesignPage,dic['labelInfo'],tables,condition_sql,tabel_name,is_split_sql)
            else:
                condition_sql = self.label_senior_search(label_Page,reportDesignPage,dic['labelInfo'],tables,condition_sql,'',is_split_sql)
            
            #点击查询按钮
            with allure.step('点击查询'):
                label_Page.query_data_btn_click()
                label_Page.alert_btn_click()
            #统计分析
            if 'data_analy' in dic:
                with allure.step('点击统计分析'):
                    label_Page.count_analy_btn_click()
                    time.sleep(0.5)
                for data_analy in dic['data_analy']:
                    
                    label_Page.select_analy_source_senior(data_analy['analySource'])
                    if 'dimension' in data_analy and data_analy['dimension'] != '' and data_analy['dimension'] != ['']:
                        label_Page.dimension_panel_click()
                        for d in data_analy['dimension']:
                            with allure.step('点击维度：{}'.format(d)):
                                label_Page.dim_input_click(d)
                        time.sleep(0.5)
                        
                    if 'target' in data_analy and data_analy['target'] != '' and data_analy['target'] != ['']:
                        label_Page.target_panel_click()
                        for t in data_analy['target']:
                            with allure.step('点击指标：{}'.format(t)):
                                label_Page.quota_input_click(t)
                        time.sleep(0.5)
                label_Page.count_data_btn_click()
                if label_Page.get_count_result()==False:
                    #等待统计分析结果
                    time.sleep(4)


            time.sleep(1)

            #点击保存筛选按钮
            with allure.step('点击保存筛选按钮'):
                label_Page.save_filter_click()
                if 'filterStaff' not in dic['filter'][0] :
                    staff_list = []
                    staff_list.append(param.staff_no)
                    dic['filter'][0]['filterStaff'] = staff_list
                if param.staff_no not in dic['filter'][0]['filterStaff']:
                    dic['filter'][0]['filterStaff'].append(param.staff_no)  
            
            with allure.step('结果验证'):
                result = label_Page.save_filter_info(dic['filter'][0]['filterName']+datetime.datetime.now().strftime('%Y%m%d%H%M%S'),dic['filter'][0]['filterType'],dic['filter'][0]['remark'],True,dic['filter'][0]['filterStaff'])
                if 'success' == result:
                    label_Page.filter_staff_btn_click()

                    alert = label_Page.alert_tip()
                    if '保存成功' in alert:
                        label_Page.alert_btn_click()
                    assert '保存成功' in alert
        

    @allure.story('点击模板查询')
    @pytest.mark.run(order=6)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize("dic",param.filter_user_senior)
    def test_filter_user_search(self,label_lib,to_parent_frame,dic):
        '''
        ==============点击模板查询==================
        '''
        if dic is not None:
            label_Page = LabelPage(label_lib)
            reportDesignPage = ReportDesignPage(label_lib)
            is_split_sql = False
            time.sleep(0.5)
            with allure.step('点击高级版按钮'):
                label_Page.senior_button_click()
  

            #选择模板
            with allure.step('选择模板'):
                label_Page.filter_user_click()
                label_Page.select_filter(dic['type'],dic['name'])
                label_Page.filter_user_click()
                #点击自助筛选tab，让日期active
                # label_Page.select_search()
                # time.sleep(0.5)

            sql = 'select to_char(COUNT (1) , \'999,999,999,999,999,999\') from '

            tabel_sql,join_sql,inner_sql,condition_sql = ' ',' ',' ',' '
            if 'group' in dic and dic['group']!='全量':
                time.sleep(0.5)
                with allure.step('选择{}数据：{}'.format(dic['group'],dic['groupName'])):
                    join_sql,inner_sql = self.label_group_select(label_Page,reportDesignPage,dic['group'],dic['groupName'],join_sql,inner_sql)

            if 'sourceInfo' in dic :
                i = 0
                l = len(dic['sourceInfo'])
                tables = {}
                tabel_name = ''
                for sourceInfo in dic['sourceInfo']:
                    i = i + 1
                    with allure.step('数据源选择：{}{}'.format(sourceInfo['source'],sourceInfo['acct_month'])):
                        tabel_sql,inner_sql,source_id = self.label_source_select(label_Page,reportDesignPage,sourceInfo,tabel_sql,inner_sql,i,l,is_split_sql)
                        tabel_name = sourceInfo['source']+'('+sourceInfo['acct_month']+')'
                        tables[tabel_name] = 'labellibaliast'+str(i)
                        tables[tabel_name+"_sourceId"] = source_id
                        tables[tabel_name+"_sourceType"] = sourceInfo['sourceType']

                if i == 1:
                    condition_sql = self.label_senior_search(label_Page,reportDesignPage,dic['labelInfo'],tables,condition_sql,tabel_name,is_split_sql)
                else:
                    condition_sql = self.label_senior_search(label_Page,reportDesignPage,dic['labelInfo'],tables,condition_sql,'',is_split_sql)

            
            #点击查询按钮
            with allure.step('点击查询'):
                label_Page.query_data_btn_click()
                label_Page.alert_btn_click()

            with allure.step('结果验证'):
                result = label_Page.get_return_count_table_info()
                if 'sourceInfo' in dic:
                    for sourceInfo in dic['sourceInfo']:
                        assert sourceInfo['source']+'('+sourceInfo['acct_month']+')' in result[0]
                if 'group' in dic:
                    for groupName in dic['groupName']:
                        assert groupName in result[0]





    @allure.story('下载数据')
    @pytest.mark.run(order=7)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize("dic",param.data_download_senior)
    def test_download_data(self,label_lib,to_parent_frame,dic):
        '''
        ==============下载数据==================
        '''
        if dic is not None:
            label_Page = LabelPage(label_lib)
            reportDesignPage = ReportDesignPage(label_lib)
            is_split_sql = False
            time.sleep(0.5)

            with allure.step('点击高级版按钮'):
                label_Page.senior_button_click()

            sql = 'select to_char(COUNT (1) , \'999,999,999,999,999,999\') from '

            tabel_sql,join_sql,inner_sql,condition_sql = ' ',' ',' ',' '
            if 'group' in dic and dic['group']!='全量':
                time.sleep(0.5)
                with allure.step('选择{}数据：{}'.format(dic['group'],dic['groupName'])):
                    join_sql,inner_sql = self.label_group_select(label_Page,reportDesignPage,dic['group'],dic['groupName'],join_sql,inner_sql)

            if 'sourceInfo' in dic:
                i = 0
                l = len(dic['sourceInfo'])
                tables = {}
                tabel_name = ''
                for sourceInfo in dic['sourceInfo']:
                    i = i + 1
                    with allure.step('数据源选择：{}{}'.format(sourceInfo['source'],sourceInfo['acct_month'])):
                        tabel_sql,inner_sql,source_id = self.label_source_select(label_Page,reportDesignPage,sourceInfo,tabel_sql,inner_sql,i,l,is_split_sql)
                        tabel_name = sourceInfo['source']+'('+sourceInfo['acct_month']+')'
                        tables[tabel_name] = 'labellibaliast'+str(i)
                        tables[tabel_name+"_sourceId"] = source_id
                        tables[tabel_name+"_sourceType"] = sourceInfo['sourceType']

                if i == 1:
                    condition_sql = self.label_senior_search(label_Page,reportDesignPage,dic['labelInfo'],tables,condition_sql,tabel_name,is_split_sql)
                else:
                    condition_sql = self.label_senior_search(label_Page,reportDesignPage,dic['labelInfo'],tables,condition_sql,'',is_split_sql)
            
            #点击查询按钮
            with allure.step('点击查询'):
                label_Page.query_data_btn_click()
                label_Page.alert_btn_click()
            
            with allure.step('点击下载'):
                label_Page.get_data_btn_click()
                if 'download_data' in dic:
                    for download in dic['download_data']:
                        label_Page.change_source_download(download['source'],'高级')   
                        time.sleep(0.5)
                        for label in download['download']:
                            label_Page.label_btn_click(label)
                        label_Page.add_user_click()

            if 'addTemplate' in dic:
                temTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                if 'templateSub' not in dic['addTemplate'] :
                    dic['addTemplate']['templateSub']=temTime
                if 'staffs' not in dic['addTemplate'] :
                    dic['addTemplate']['staffs']=''
                with allure.step('添加下载{}模板：{}'.format(dic['addTemplate']['templateType'],dic['addTemplate']['templateName'])):
                    result = label_Page.add_template(dic['addTemplate']['templateName']+temTime,dic['addTemplate']['templateType'],dic['addTemplate']['templateSub'],'高级',dic['addTemplate']['staffs'])
                    if result == 'success':
                        label_Page.download_filter_staff_btn_click()
                        alert = label_Page.alert_tip()
                        if '保存成功' in alert:
                            label_Page.alert_btn_click()
                        assert '保存成功' in alert 

            time.sleep(1) 
            if 'selectTemplate' in dic:
                with allure.step('选择{}模板：{}'.format(dic['selectTemplate']['templateType'],dic['selectTemplate']['templateName'])):
                    label_Page.select_template(dic['selectTemplate']['templateType'],dic['selectTemplate']['templateName'],'高级')

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
    @pytest.mark.parametrize("dic",param.data_analy_senior)
    def test_count_analy(self,label_lib,to_parent_frame,dic):
        '''
        ==============统计分析==================
        '''
        #统计分析
        if dic is not None:
            label_Page = LabelPage(label_lib)
            reportDesignPage = ReportDesignPage(label_lib)
            is_split_sql = False
            time.sleep(0.5)
            with allure.step('点击高级版按钮'):
                label_Page.senior_button_click()

            sql = 'select to_char(COUNT (1) , \'999,999,999,999,999,999\') from '

            tabel_sql,join_sql,inner_sql,condition_sql = ' ',' ',' ',' '
            if 'group' in dic and dic['group']!='全量':
                time.sleep(0.5)
                with allure.step('选择{}数据：{}'.format(dic['group'],dic['groupName'])):
                    join_sql,inner_sql = self.label_group_select(label_Page,reportDesignPage,dic['group'],dic['groupName'],join_sql,inner_sql)

            i = 0
            l = len(dic['sourceInfo'])
            tables = {}
            tabel_name = ''
            for sourceInfo in dic['sourceInfo']:
                i = i + 1
                with allure.step('数据源选择：{}{}'.format(sourceInfo['source'],sourceInfo['acct_month'])):
                    tabel_sql,inner_sql,source_id = self.label_source_select(label_Page,reportDesignPage,sourceInfo,tabel_sql,inner_sql,i,l,is_split_sql)
                    tabel_name = sourceInfo['source']+'('+sourceInfo['acct_month']+')'
                    tables[tabel_name] = 'labellibaliast'+str(i)
                    tables[tabel_name+"_sourceId"] = source_id
                    tables[tabel_name+"_sourceType"] = sourceInfo['sourceType']

            if i == 1:
                condition_sql = self.label_senior_search(label_Page,reportDesignPage,dic['labelInfo'],tables,condition_sql,tabel_name,is_split_sql)
            else:
                condition_sql = self.label_senior_search(label_Page,reportDesignPage,dic['labelInfo'],tables,condition_sql,'',is_split_sql)
            
            #点击查询按钮
            with allure.step('点击查询'):
                label_Page.query_data_btn_click()
                label_Page.alert_btn_click()


            #统计分析
            if 'data_analy' in dic:
                with allure.step('点击统计分析'):
                    label_Page.count_analy_btn_click()
                    time.sleep(0.5)
                for data_analy in dic['data_analy']:
                    label_Page.select_analy_source_senior(data_analy['analySource'])
                    if 'dimension' in data_analy and data_analy['dimension'] != '' and data_analy['dimension'] != ['']:
                        label_Page.dimension_panel_click()
                        for d in data_analy['dimension']:
                            with allure.step('点击维度：{}'.format(d)):
                                label_Page.dim_input_click(d)
                                time.sleep(0.5)
                        
                    if 'target' in data_analy and data_analy['target'] != '' and data_analy['target'] != ['']:
                        label_Page.target_panel_click()
                        for t in data_analy['target']:
                            with allure.step('点击指标：{}'.format(t)):
                                label_Page.quota_input_click(t)
                                time.sleep(0.5)
                label_Page.count_data_btn_click()
            time.sleep(1)

            with allure.step('结果验证'):
                analy_result = label_Page.analy_result() 
                analy_result = ','.join(analy_result)
                if 'data_analy' in dic:
                    for data_analy in dic['data_analy']:
                        if 'target' in data_analy and data_analy['target'] != '' and data_analy['target'] != ['']:
                            for target in data_analy['target']:
                                with allure.step('统计分析结果：{}'.format(target)) :
                                    assert target in analy_result
                        if 'dimension' in data_analy and data_analy['dimension'] != '' and data_analy['dimension'] != ['']:
                            for dimension in data_analy['dimension']:
                                with allure.step('统计分析结果：{}'.format(dimension)) :
                                    assert dimension in analy_result   
                    
 


    @allure.story('清理已存/已传/保存筛选')
    @pytest.mark.run(order=9)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    # @pytest.mark.skip(reason= 'periodic cleaning')
    @pytest.mark.parametrize("dic",param.data_clean_senior)
    def test_data_clean(self,label_lib,to_parent_frame,dic):
        '''
        ==============清理已存/已传/保存筛选==================
        '''
        if dic is not None:
            label_Page =  LabelPage(label_lib)
            time.sleep(0.5)
            with allure.step('点击高级版按钮'):
                label_Page.senior_button_click()
  

            #删除模板
            label_Page.filter_user_click()
            for filter in dic['filter_name']:
                with allure.step('清理模板：{}'.format(filter)):
                    label_Page.delete_filter(filter['type'],filter['name'])
            time.sleep(0.5)   

            #删除已存用户
            label_Page.saved_user_click()  
            for name in dic['saved_name']:
                with allure.step('清理已存数据：{}'.format(name)):
                    label_Page.saved_users_click(name)
                    result = label_Page.delete_saved_users_click(name)
            label_Page.saved_close_btn_click()
            time.sleep(0.5)

            #删除已传用户
            label_Page.uploaded_user_click()
            for name in dic['uploaded_name']:
                with allure.step('清理已传数据：{}'.format(name)):
                    label_Page.uploaded_users_click(name)
            result = label_Page.delete_uploaded_users_click(dic['uploaded_name'])
            label_Page.uploaded_close_btn_click()
            time.sleep(0.5)


           
