# #!/usr/bin/python
# #coding=utf-8


# import unittest
# import sys
# from common import HTMLTestRunner
# from testcase.testLoginPage import  TestLoginPage
# from testcase.testLabelPage import TestLabelPage
# from testcase.testAllLabelPage import TestAllLabelPage
# from email.mime.text import MIMEText
# import smtplib
# import datetime


# def send_email(newfile):
#     f = open(newfile,'rb')
#     mail_body = f.read()
#     f.close()
#     smtpserver = 'smtp.exmail.qq.com'
#     #发件箱用户名密码
#     user_f = 'xin.zhou@ifudata.com'
#     pwd_f = 'Luhan0420'
#     #收件箱用户名
#     user_r = 'xin.zhou@ifudata.com'

#     #主题
#     now = datetime.datetime.now().strftime('%Y%m%d')
#     subject = '自动化测试报告'+now

#     msg = MIMEText(mail_body,'html','utf-8')

#     msg['From'] = user_f
#     msg['To'] = pwd_f
#     msg['Subject'] = subject

#     server = smtplib.SMTP()
#     server.connect(smtpserver,25)
#     server.login(user_f,pwd_f)
#     server.sendmail(user_f,user_r,msg.as_string())
#     server.quit()


# def mk_html(htmlPath):
#     fp = open(htmlPath, "wb")
#     runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'数家测试登录', description=u'测试用例结果')
#     runner.run(testunit)
#     fp.close()


# if __name__ == '__main__':
#     testunit = unittest.TestSuite()
#     testunit.addTest(TestLoginPage('testLoginFail'))
#     testunit.addTest(TestLoginPage('testLoginSuccess'))
#     # testunit.addTest(TestLabelPage('testMonthSearch'))
#     # testunit.addTest(TestAllLabelPage('testAllLabel'))


#     now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
#     htmlPath = r'.\shujia_result\page_login_Report'+now+'.html'

#     mk_html(htmlPath)
#     send_email(htmlPath)

