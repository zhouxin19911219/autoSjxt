# #! /usr/bin/python
# # coding=utf-8
# import allure
# import pytest
# import sys
# sys.path.append('.')
# from pages.listBuildPage import ListBuildPage
# from common import param
# import time
# import datetime
# # from db.cont_mysql_db import get_staff_info

# @allure.feature('清单发布')
# class Test_listBuild_Page():

#     #清单发布不审批不拆分
#     @allure.story('清单发布')
#     @pytest.mark.flaky(reruns=2,reruns_delay=1)
#     @pytest.mark.parametrize('dic',param.list_data)
#     def test_listBuild(self,list_build,to_parent_frame,dic):
#         listBuild_Page = ListBuildPage(list_build)

#         # 切换数据清单
#         if dic['listType'] == '数据':
#             listBuild_Page.datalist_click()

#         #输入清单名称
#         listBuild_Page.list_name_sendKeys(dic['listname']+datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
#         #账期
#         listBuild_Page.list_acctdate_sendKeys(dic['acctDate'])


#         if dic['listType'] == '文件':
#             #上传清单文件
#             listBuild_Page.list_file_upload(dic['listFile'])
#             while listBuild_Page.list_file_tips() !='上传成功':
#                 time.sleep(1)
#         elif dic['listType'] == '数据':
#             #是否周期
#             listBuild_Page.control_click(dic['cycle'])
#             #输入数据清单sql
#             listBuild_Page.split_sql_sendkeys(dic['spilt_sql'])

#         #上传说明文件
#         if dic['listMarkFile'] != '':
#             listBuild_Page.list_file_remark_upload(dic['listMarkFile'])
#             while listBuild_Page.list_file_remark_tips() !='上传成功':
#                 time.sleep(1)
        
#         if dic['listApprove'] == '是':
#             #选择人员审批
#             listBuild_Page.require_approve_click()
#             time.sleep(1)
#             listBuild_Page.require_approve_staff()
#             time.sleep(1)
#             listBuild_Page.approve_staff_search(dic['ApproveStaff'])
#             time.sleep(1)
#             listBuild_Page.approve_staff_search_click()
#             time.sleep(1)
#             listBuild_Page.approve_staff_select_click(dic['ApproveStaff'])
#             listBuild_Page.approve_staff_select_btn_click()


#         #失效时间
#         listBuild_Page.invalid_time_click()
#         if dic['invalidTime']=='' or 'invalidTime' not in dic:
#             listBuild_Page.invalid_time_date_click(datetime.datetime.now().strftime('%Y%m%d'))
#         elif len(dic['invalidTime']) != 8  :
#             listBuild_Page.invalid_time_value_click(dic['invalidTime'])
#         else :
#             listBuild_Page.invalid_time_date_click(dic['invalidTime'])



#         if dic['listSplit'] == '是':            
#             #选择拆分
#             listBuild_Page.split_click()
#             if 'spilt_sql' in dic:
#                 if '${month' in dic['spilt_sql'] or '${day' in dic['spilt_sql']:
#                     res = listBuild_Page.replace_acctmonth(dic['replaceType'],dic['replaceTime'])
#                     if 'success' in res:
#                         listBuild_Page.replace_acctmonth_sure_click()

#             time.sleep(1)
#             #选择拆分的字段
#             listBuild_Page.split_field_click(dic['splitField'])
#             time.sleep(1)
#             listBuild_Page.search_staff()
#             time.sleep(1)
#             # listBuild_Page.staff_drag()
#             #增加用户
#             for staff in dic['splitStaff']:
#                 staffinfo = get_staff_info(staff)
#                 listBuild_Page.staff_add(staffinfo)
#                 time.sleep(1)
#         else:
#             listBuild_Page.split_not_click()
#             if 'spilt_sql' in dic:
#                 if '${month' in dic['spilt_sql'] or '${day' in dic['spilt_sql']:
#                     res = listBuild_Page.replace_acctmonth(dic['replaceType'],dic['replaceTime'])
#                     if 'success' in res:
#                         listBuild_Page.replace_acctmonth_sure_click()

#             listBuild_Page.search_staff()
#             time.sleep(1)
#             # listBuild_Page.staff_drag()
#             #增加用户
#             for staff in dic['splitStaff']:
#                 staffinfo = get_staff_info(staff)
#                 listBuild_Page.staff_add(staffinfo)
#                 time.sleep(1)
#         #点击提交
#         listBuild_Page.submit_click()
#         time.sleep(2)
#         #判断是否提交成功
#         suc = listBuild_Page.alert_tip()
#         assert '清单发布成功' in  suc
#         time.sleep(1)
#         listBuild_Page.alert_btn_click()


# # if __name__ == "__main__":
# #     pytest.main(['-s','test_listBuild_page.py'])
