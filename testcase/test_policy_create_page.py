# /usr/bin/python
# coding=utf-8
import sys
sys.path.append('.')
import allure
import pytest
from common import param
from pages.policyCreatePage import PolicyCreatePage
from pages.labelPage import LabelPage
import time

@allure.feature('策略创建')
class Test_policyCreate_Page():

    def label_search(self,label_Page,sourceType,label,source_id,l):
        if 'labelFile' in label and label['labelFile']!='':
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
    
    @allure.story('策略创建')
    @pytest.mark.run(order=1)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize('dic',param.policy_create_data)
    def test_policy_create(self,policy_create,to_parent_frame,dic):
        
        policyCreatePage = PolicyCreatePage(policy_create)
        labelPage = LabelPage(policy_create)
        policyCreatePage.cover_is_display()

        
        for scene_select in dic['scene_select']:
            #点击场景
            with allure.step('勾选场景：{}'.format(scene_select['sceneName'])):
                policyCreatePage.policy_click(scene_select['sceneName'])
            #设置场景口径
            with allure.step('设置场景口径：{}'.format(scene_select['sceneName'])):
                scene_id = policyCreatePage.policy_label_click(scene_select['sceneName'])
                scene_select['sceneId'] = scene_id
                #删除已有口径
                with allure.step('删除已有口径'):
                    policyCreatePage.delete_label_caliber()

                #选择标签
                l = len(scene_select['sceneCaliber'])
                source_id = policyCreatePage.get_source_id()
                for label in scene_select['sceneCaliber']:
                    with allure.step('点击口径标签信息：{}'.format(label)):
                        self.label_search(labelPage,'month',label,source_id,l)
                        l = l-1
                
                policyCreatePage.save_caliber()

            #设置最大值
            with allure.step('设置 {} 场景最大值：{}'.format(scene_select['sceneName'],scene_select['maxVal'])):
                policyCreatePage.input_max_val(scene_select['sceneName'],scene_select['maxVal'])

        with allure.step('点击场景匹配'):
            policyCreatePage.scene_adjust()

        for scene_select in dic['scene_select']:
            if 'marketNum' in scene_select or 'adjustNum' in scene_select:
                sceneId = scene_select['sceneId']
                if 'marketNum' not in scene_select:
                    scene_select['marketNum']=0
                if 'adjustNum' not in scene_select:
                    scene_select['adjustNum']=0   
                with allure.step('设置 {} 场景营销人数'.format(scene_select['sceneName'])): 
                    policyCreatePage.set_num(sceneId,scene_select['marketNum'],scene_select['adjustNum'],scene_select['maxVal'])
                
                policyCreatePage.change_strategy_cnt(sceneId)
                #删除已有营销
                policyCreatePage.delete_strategy()
                policyCreatePage.add_strategy()
                #选择标签
                l = len(scene_select['strategyCaliber'])
                for strategy in scene_select['strategyCaliber']:

                    for label in strategy['labelInfo']:
                        with allure.step('点击策略调整标签信息：{}'.format(label)):
                            self.label_search(labelPage,'month',label,source_id,l)
                            l = l-1

                with allure.step('选择产品大类：{}，产品信息：{}'.format(strategy['product_type'],strategy['product'])):
                    policyCreatePage.product_type_click(strategy['product_type'])
                    policyCreatePage.product_click(strategy['product'])

                policyCreatePage.save_strategy()
                policyCreatePage.check_strategy()
                #收入预测
                policyCreatePage.preview()
                policyCreatePage.preview_calculate()
                policyCreatePage.save_person()



                result = policyCreatePage.get_result(scene_select['sceneName'])
                with allure.step('{} 场景生成清单结果：{}'.format(scene_select['sceneName'],result)):
                    assert '已生成清单' in result

                with allure.step('点击用户选择'):
                    policyCreatePage.person_select()

                is_success = policyCreatePage.select_group_name('场景用户',scene_select['sceneName'])
                with allure.step('用户选择中{}场景是否存在：{}'.format(scene_select['sceneName'],is_success)):
                    assert is_success == True





    @allure.story('清理场景')
    @pytest.mark.run(order=2)
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize('dic',param.policy_scene_clean)
    def test_scene_clean(self,policy_create,to_parent_frame,dic):
        policyCreatePage = PolicyCreatePage(policy_create)

        #点击手动场景
        with allure.step('点击用户选择'):
            policyCreatePage.manual_scene_click()
            with allure.step('删除{}，场景：{}'.format(dic['groupType'],dic['groupName'])):
                policyCreatePage.select_user_group(dic['groupType'])
                policyCreatePage.delete_group_name(dic['groupType'],dic['groupName'])




    @allure.story('触点选择')
    @pytest.mark.run(order=3)
    @pytest.mark.skip(reason='用户分配无法选择')
    @pytest.mark.flaky(reruns=1,reruns_delay=1)
    @pytest.mark.parametrize('dic',param.policy_scene_flow)
    def test_scene_flow(self,policy_create,to_parent_frame,dic):
        policyCreatePage = PolicyCreatePage(policy_create)

        #点击手动场景
        with allure.step('点击手动场景'):
            policyCreatePage.manual_scene_click()
            with allure.step('选择用户群{}，用户名：{}'.format(dic['groupType'],dic['groupName'])):
                policyCreatePage.select_user_group(dic['groupType'])
                policyCreatePage.select_group_name(dic['groupType'],dic['groupName'])
        #点击用户分配
        with allure.step('点击产品分配'):
            policyCreatePage.product_assignment()



 

if __name__ == "__main__":
    pytest.main(['-s',"testcase/test_poliy_create_page.py::Test_poliyCreate_Page::test_policy_create"])



