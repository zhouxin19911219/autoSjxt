# /usr/bin/python
# coding=utf-8

import sys
sys.path.append('.')
from pages.zfCalculatePage import ZfCalculatePage
from pages.labelPage import LabelPage
import time
# from db import cont_mysql_db
import pytest
from common import param
import allure


@allure.feature('资费测算')
class Test_zfCalculate_Page():

    def label_search(self,label_Page,sourceType,label,source_id,l):
        if label['labelFile']!='':
            #点击上级目录
            label_Page.file_click(sourceType,label['labelFile'])
        else:      
            #点击搜索框搜索  
            label_Page.label_search(sourceType,label['labelsearch'],label['searchlabel'])
            
        time.sleep(0.2)
        if True == label_Page.label_exist(label['labelName']):
            if '枚举' == label['labelType']:
                label_Page.enum_click(label['labelName'],label['labelValue'])
            
            elif '数值' == label['labelType']:
                label_Page.num_click(label['labelName'],label['labelValue'])                

            elif '时间' in label['labelType']:
                label_Page.label_btn_click(label['labelName'])
                label_format = label_Page.get_format(label['labelValue'])
                label_Page.time_click(label['labelName'],label_format,label['labelValue'])


            elif '大枚举' in label['labelType']:
                label_Page.bigCode_click(label['labelName'],label['labelValue'],label['inverse'])


            elif '大数量枚举' in label['labelType']:
                if 'labelValue' not in label:
                    label['labelValue']=''
                if 'searchlabel' not in label:
                    label['searchlabel']=''
                labels,id = label_Page.enum_bigCode_click(label['labelName'],label['labelValue'],label['inverse'],label['searchlabel'])
            #关闭type=5的下钻图层,标签库弹框没有05下钻
            # label_Page.close_type5()


    @allure.story('资费测算')
    @pytest.mark.run(order=1)   
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize('dic',param.zf_calculate_data)
    def test_zf_calculate(self,zf_calculate,to_parent_frame,dic):
        '''
            资费测算执行
        '''
        zfCalculatePage = ZfCalculatePage(zf_calculate)
        labelPage = LabelPage(zf_calculate)
        zfCalculatePage.cover_is_display()
        source_id = zfCalculatePage.get_source_id()


        if dic['sourceType'] == '已存':
            with allure.step('选择已存用户：{}'.format(dic['source'])):
                zfCalculatePage.saved_user_click(dic['source'])
        elif dic['sourceType'] == '已传':
            with allure.step('选择已传用户：{}'.format(dic['source'])):
                zfCalculatePage.uploaded_user_click(dic['source'])

        with allure.step('点击添加规则'):
            zfCalculatePage.add_rule_click()


        # source = cont_mysql_db.get_zf_source()

        l = len(dic['labelInfo'])
        for label in dic['labelInfo']:
            with allure.step('点击查询标签信息：{}'.format(label)):
                self.label_search(labelPage,'month',label,source_id,l)
                l = l-1

        with allure.step('选择产品大类：{}，产品信息：{}'.format(dic['product_type'],dic['product'])):
            zfCalculatePage.product_type_click(dic['product_type'])
            zfCalculatePage.product_click(dic['product'])


        zfCalculatePage.label_sure_click()

        zfCalculatePage.calculate_click()

        tip = zfCalculatePage.alert_tip()
        if tip != '':
            assert tip == ''
            print('资费测算结果预测：'+tip)

        result = zfCalculatePage.get_calculate_result()
        with allure.step('资费测算结果：{}'.format(result)):        
            if '执行成功' in result:
                zfCalculatePage.calculate_result_click()
                
            if '无匹配人数' in result:
                assert '无匹配人数' in result
            else:
                assert '执行成功' in result








