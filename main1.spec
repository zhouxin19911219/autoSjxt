# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

SETUP_DIR = 'D:\\doc\\pd_code\\AutoTest\\shujia\\'


a = Analysis(['main.py',
'testcase\\test_analy_page.py',
'testcase\\test_label_page.py',
'testcase\\test_label_senior_page.py',
'testcase\\test_listBuild_page.py',
'testcase\\test_zf_calculate_page.py',
'testcase\\test_sql_search_page.py',
'pages\\analyPage.py',
'pages\\basePage.py',
'pages\\indexPage.py',
'pages\\labelPage.py',
'pages\\listBuildPage.py',
'pages\\loginPage.py',
'pages\\zfCalculatePage.py',
'pages\\sqlSearchPage.py',
'db\\cont_gp_db.py',
'db\\cont_mysql_db.py',
'common\\param.py'
],
             pathex=['D:\\doc\\pd_code\\AutoTest\\shujia'],
             binaries=[('C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe','.'),
             ('D:\\Program Files\\Python38\\Lib\\site-packages\\allure_pytest-2.8.18.dist-info','allure_pytest-2.8.18.dist-info'),
             ('D:\\Program Files\\Python38\\Lib\\site-packages\\allure-2.7.0','allure-2.7.0'),
             ('D:\\Program Files\\Python38\\Lib\\site-packages\\pytest_rerunfailures-9.0.dist-info','pytest_rerunfailures-9.0.dist-info'),
             ('D:\\Program Files\\Python38\\Lib\\site-packages\\pytest_rerunfailures.py','.'),
             ('D:\\doc\\pd_code\\AutoTest\\shujia\\to_html.exe','.')
             ],
             datas=[
             (SETUP_DIR+'file','file'),(SETUP_DIR+'testcase','testcase'),(SETUP_DIR+'conftest.py','.')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.datas +=[('zc.ico','D:\\doc\\pd_code\\AutoTest\\shujia\\zc.ico','DATA')]
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
