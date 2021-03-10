#! /usr/bin/python
# coding=utf-8
import os
import sys
sys.path.append('.')
import datetime
import yaml

#打开配置文件
file_db = open('file/params/config.yaml','r',encoding='utf-8')
file_parmas = file_db.read()
file_db.close()
config = yaml.load(file_parmas,Loader=yaml.SafeLoader)['config']
report_design_datasource = yaml.load(file_parmas,Loader=yaml.SafeLoader)['report_design']

url = config['url']
usr = config['usr_suc']
pwd = config['pwd_suc']

# usr_err = config['usr_err']
# pwd_err = config['pwd_err']

bas_path = os.path.abspath('.')

#获取用户id，用户name
# staff_name = get_staff_info(usr_suc)[0][2]
# staff_id = get_staff_info(usr_suc)[0][0]
# staff_grade = get_staff_info(usr_suc)[0][3]
staff_no = usr

om_datasource = report_design_datasource['om']
sys_datasource = report_design_datasource['sys']
gp_datasource = report_design_datasource['gp']


def get_param(path):
    file_db = open(path,'r',encoding='utf-8')
    file_parmas = file_db.read()
    file_db.close()
    return yaml.load(file_parmas,Loader=yaml.SafeLoader)

#================================菜单==================================
menu = get_param(bas_path+'/file/params/menu.yaml')
if 'label_lib' in menu:
    label_lib = menu['label_lib']
if 'auto_analy' in menu:
    auto_analy = menu['auto_analy']
if 'list_build' in menu:
    list_build = menu['list_build']
if 'list_search' in menu:
    list_search = menu['list_search']
if 'list_download' in menu:
    list_download = menu['list_download']
if 'zf_calculate' in menu:
    zf_calculate = menu['zf_calculate']
if 'sql_search' in menu:
    sql_search = menu['sql_search']
if 'report_design' in menu:
    report_design = menu['report_design']
    report_design_menu = report_design['menu']
if 'policy_create' in menu:
    policy_create = menu['policy_create']
#=================================清单============================
# list_data= param_list.list_data
list_v2= get_param(bas_path+'/file/params/list.yaml')
if 'list_data' in list_v2:
    list_data = list_v2['list_data']

# if 'list_download' in list_v2:
#     list_download = list_v2['list_download']

# if 'list_search' in list_v2:
#     list_search = list_v2['list_search']

#====================================标签库高级版============================================
param_label_senior = get_param(bas_path+'/file/params/label_senior.yaml')

if 'labellib_senior_data' in param_label_senior:
    labellib_senior_data = param_label_senior['labellib_senior_data']

if 'data_upload_senior' in param_label_senior:
    data_upload_senior = param_label_senior['data_upload_senior']

if 'data_uploaded_senior' in param_label_senior:
    data_uploaded_senior = param_label_senior['data_uploaded_senior']

if 'save_label_filter_data_senior' in param_label_senior:
    save_label_filter_data_senior = param_label_senior['save_label_filter_data_senior']

if 'filter_user_senior' in param_label_senior:
    filter_user_senior = param_label_senior['filter_user_senior']

if 'data_download_senior' in param_label_senior:
    data_download_senior = param_label_senior['data_download_senior']

if 'data_analy_senior' in param_label_senior:
    data_analy_senior = param_label_senior['data_analy_senior']

if 'data_clean_senior' in param_label_senior:
    data_clean_senior = param_label_senior['data_clean_senior']

#====================================标签库============================================
param_label = get_param(bas_path+'/file/params/label.yaml')

# labellib_enum_data = param_label['labellib_enum_data']

# labellib_num_data = param_label['labellib_num_data']

# labellib_time_data = param_label['labellib_time_data']

# data_bigcode = param_label['data_bigcode']

# data_inverse = param_label['data_inverse']

if 'data_upload' in param_label:
    data_upload = param_label['data_upload']

if 'data_uploaded' in param_label:
    data_uploaded = param_label['data_uploaded']

if 'labellib_data' in param_label:
    labellib_data = param_label['labellib_data']

if 'save_label_filter_data' in param_label:
    save_label_filter_data = param_label['save_label_filter_data']

if 'filter_user' in param_label:
    filter_user = param_label['filter_user']

if 'data_download' in param_label:
    data_download = param_label['data_download']

if 'data_analy' in param_label:
    data_analy = param_label['data_analy']

if 'data_clean' in param_label:
    data_clean = param_label['data_clean']

#====================================自助报表============================================
param_analy = get_param(bas_path+'/file/params/analy.yaml')

if 'analy_data' in param_analy:
    analy_data = param_analy['analy_data']

if 'filter_Info' in param_analy:
    filter_Info = param_analy['filter_Info']

if 'save_template' in param_analy:
    save_template = param_analy['save_template']

if 'download_data' in param_analy:
    download_data = param_analy['download_data']

if 'data_clean_analy' in param_analy:
    data_clean_analy = param_analy['data_clean_analy']


#======================================资费测算=================================================

zf_calcul = get_param(bas_path+'/file/params/zf_calculate.yaml')

if 'zf_calculate' in zf_calcul:
    zf_calculate_data = zf_calcul['zf_calculate']

#=====================================sql查询=========================================

sql_sear = get_param(bas_path+'/file/params/sql_search.yaml')

if 'sql_search' in sql_sear:
    sql_search_data = sql_sear['sql_search']

if 'data_clean' in sql_sear:
    data_clean_sql = sql_sear['data_clean']


#====================================策略创建====================================================

policy_cre = get_param(bas_path+'/file/params/policy_create.yaml')

if 'policy_create' in policy_cre:
    policy_create_data = policy_cre['policy_create']

if 'policy_scene_clean' in policy_cre:
    policy_scene_clean = policy_cre['policy_scene_clean']

if 'policy_scene_flow' in policy_cre:
    policy_scene_flow = policy_cre['policy_scene_flow']