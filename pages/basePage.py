#! /usr/bin/python
#coding:utf-8

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import os
import datetime
import allure
import logging

class Page(object):
    '''
    基类
    '''
    def __init__(self,driver):
        self.date_log = datetime.datetime.now().strftime('%Y%m%d')        
        if os.path.exists(os.path.abspath('.')+'\\file\\screen\\'+self.date_log) == False:
            os.mkdir(os.path.abspath('.')+'\\file\\screen\\'+self.date_log)
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level = logging.INFO)
        handler = logging.FileHandler(os.path.abspath('.')+"\\file\\screen\\"+self.date_log+"\\log.txt")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    
    def find_element(self,loc):
        try:
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located(loc))
            self.driver.find_element(*loc)
        except (BaseException):
            self.png_to_allure()
        finally:
            self.logger.info('查找元素：{}'.format(loc))


    
    def find_element_value(self,loc):
        try:
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located(loc))
        except (BaseException):
            self.png_to_allure()
        else:
            return self.driver.find_element(*loc).get_attribute('value')
        finally:
            self.logger.info('获取元素value值：{}'.format(loc))

    def find_element_attr(self,loc,attr):
        try:
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located(loc))
            ele_len = len(self.driver.find_elements(*loc))
            ele = []
            for i in range(0,ele_len):
                e = self.driver.find_elements(*loc)[i].get_attribute(attr)
                ele.append(e)
            self.logger.info('获取{}元素属性：{}'.format(loc,attr))
        except (BaseException):
            self.png_to_allure()
            self.logger.info('获取{}元素属性：{}'.format(loc,attr))
        else:
            return ele
            
        
    
    def find_elements(self,loc):
        try:
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_all_elements_located(loc))
            self.logger.info('获取批量元素：{}'.format(loc))
        except (BaseException):
            self.png_to_allure()
            self.logger.info('获取批量元素：{}'.format(loc))
        else:
            return self.driver.find_elements(*loc)

    def get_text(self, loc ):
        try:
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located(loc))
            self.logger.info('获取元素text：{}'.format(loc))
        except (BaseException):
            self.png_to_allure()
            self.logger.info('获取元素text：{}'.format(loc))
        else:
            return self.driver.find_element(*loc).text

    def get_eles_text(self,loc):
        try:
            list_text=[]
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_all_elements_located(loc))
            for e in self.driver.find_elements(*loc):
                list_text.append(e.text)
            self.logger.info('获取批量元素text：{}：{}'.format(loc,list_text))
        except (BaseException,TimeoutError):
            self.png_to_allure()
            self.logger.info('获取批量元素text：{}：{}'.format(loc,list_text))
        else:
            return list_text

    def clear(self, loc):
        try:
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located(loc))
            self.driver.find_element(*loc).clear()
            
        except (BaseException):
            self.png_to_allure()
        finally:
            self.logger.info('清空元素：{}'.format(loc))

    def keys_clear(self,loc):
        try:
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located(loc))
            self.driver.find_element(*loc).send_keys(Keys.BACK_SPACE)        
        except (BaseException):
            self.png_to_allure()
        finally:
            self.logger.info('清空元素：{}'.format(loc))

    def send_keys(self, loc, text):
        try:
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located(loc))
            self.driver.find_element(*loc).send_keys( text )
        except (BaseException):
            self.png_to_allure()
        finally:
            self.logger.info('元素{}输入值：{}'.format(loc,text))

    def click(self , loc ):
        try:
            WebDriverWait(self.driver,5,0.5).until(EC.presence_of_element_located(loc))
            self.driver.find_element(*loc).click()
        except(BaseException,TimeoutError):
            self.png_to_allure()
        finally:
            self.logger.info('点击元素：{}'.format(loc))
        
    def not_wait_click(self , loc ):
        try:
            self.driver.find_element(*loc).click()
        except (BaseException):
            self.png_to_allure()
        finally:
            self.logger.info('点击元素：{}'.format(loc))


    def context_click(self, loc):
        try:
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located(loc))
            ele = self.driver.find_element(*loc)
            ActionChains(self.driver).context_click(ele).perform()
        except (BaseException):
            self.png_to_allure()
        finally:
            self.logger.info('根据内容点击元素：{}'.format(loc))

    def move_to_element_and_click_element(self , loc_hover , loc_click):
        try:
            ActionChains(self.driver).move_to_element(self.driver.find_element(*loc_hover)).click(self.driver.find_element(*loc_click)).perform()
        except (BaseException):
            self.png_to_allure()
        finally:
            self.logger.info('移动到{}点击元素：{}'.format(loc_hover,loc_click))

    def move_to_element_click(self,loc):
        try:
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located(loc))
            ele = self.driver.find_element(*loc)
            ActionChains(self.driver).move_to_element(ele).click(ele).perform()
        except (BaseException,TimeoutError):
            self.png_to_allure() 
        finally:
            self.logger.info('移动到元素位置并点击元素：{}'.format(loc))

    def get_title(self):
        self.logger.info('获取元素title：{}'.format(self.driver.title))
        return self.driver.title


    def is_exist(self,loc):
        try:
            WebDriverWait(self.driver,5,0.5).until(EC.presence_of_element_located(loc))
            self.logger.info('等待5s，判断元素{}是否存在：{}'.format(loc,'存在'))
            return True
        except:
            self.logger.info('等待5s，判断元素{}是否存在：{}'.format(loc,'不存在'))
            return False

            

    def is_exist_no_wait(self,loc):
        try:
            # self.driver.find_element(*loc)
            WebDriverWait(self.driver,1,0.5).until(EC.presence_of_element_located(loc))
            self.logger.info('判断元素{}是否存在：{}'.format(loc,'存在'))
            return True
        except:
            self.logger.info('判断元素{}是否存在：{}'.format(loc,'不存在'))
            return False

    def is_display(self,loc):
        try:
            WebDriverWait(self.driver,2,0.5).until(EC.presence_of_element_located(loc))
        except(BaseException):
            self.png_to_allure()
        finally:
            result = self.driver.find_element(*loc).is_displayed()
            self.logger.info('等待2s，判断元素{}是否显示display：{}'.format(loc,result))
            return result
            

    def is_display_no_wait(self,loc):
        result = self.driver.find_element(*loc).is_displayed()
        self.logger.info('判断元素{}是否显示display：{}'.format(loc,result))
        return result

    def switch_frame(self,loc):
        try:
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located(loc))
            self.driver.switch_to.frame(self.driver.find_element(*loc))
        except (BaseException):
            self.png_to_allure()

    def switch_to_parent_frame(self):
        try:
            self.driver.switch_to.parent_frame()
        except (BaseException):
            self.png_to_allure()
    
    def select_by_value(self,loc,val):
        try:
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located(loc))
            loc = self.driver.find_element(*loc)
            Select(loc).select_by_value(val)
        except (BaseException):
            self.png_to_allure()
        finally:
            self.logger.info('通过value值选择select：{}下拉框值：{}'.format(loc,val))
    
    def select_by_text(self,loc,text):
        try:
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located(loc))
            loc = self.driver.find_element(*loc)
            Select(loc).select_by_visible_text(text)
        except (BaseException):
            self.png_to_allure()
        finally:
            self.logger.info('通过text值选择select：{}下拉框值：{}'.format(loc,text))


    def ele_is_selected(self,loc):
        try:
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located(loc))
        except (BaseException):
            self.png_to_allure()
        else:
            result = self.driver.find_element(*loc).is_selected()
            self.logger.info('判断元素是否被选中：{}'.format(loc))
            return result


    def drag_drop(self,drag_loc,drop_loc):  
        try:    
            action = ActionChains(self.driver)
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located(drag_loc))
            drag = self.driver.find_element(*drag_loc)
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located(drop_loc))
            drop = self.driver.find_element(*drop_loc)
            action.drag_and_drop(drag,drop)
            action.perform()
        except (BaseException):
            self.png_to_allure()
        finally:
            self.logger.info('拖{}元素到位置：{}'.format(drag_loc,drop_loc))

    def add_child_ele(self,org_ele,add_ele):
        js = '$("'+org_ele+'").append("'+add_ele+'");'
        self.driver.execute_script(js)

    def add_class_attribute(self,class_loc,class_loc1,len):
        len = int(len)
        for i in range(0,len-1):
            js = "$('"+class_loc+"')["+i+"].setAttribute('class','"+class_loc1+"')"
            self.driver.execute_script(js)

    def add_ele_display(self,class_ele,attr):
        js = class_ele +".style.display='"+attr+"'"
        self.driver.execute_script(js)
    
    def ele_show(self,class_ele):
        js = class_ele +".show()"
        self.driver.execute_script(js)
    
    def ele_hide(self,class_ele):
        js = class_ele +".hide()"
        self.driver.execute_script(js)
    
    # def get_attr_length(self,class_loc):
    #     try:
    #         WebDriverWait(self.driver,20,0.5).until(EC.presence_of_all_elements_located(class_loc))
    #         ele_len = self.driver.find_elements(*class_loc)
    #     except (BaseException):
    #         self.png_to_allure()
    #     else:
    #         return len(ele_len)

    def remove_attr(self,attr_class,attr_value,attr):
        js = "$('input["+attr_class+"="+attr_value+"]').removeAttr('"+attr+"')"
        self.driver.execute_script(js)
    
    def add_attr(self,ele,i,attr,val):
        if i > 0 :
            js = "$('"+ele+"').eq("+str(i)+").attr('"+attr+"','"+val+"')"
            self.driver.execute_script(js)
        else:
            js = "$('"+ele+"').attr('"+attr+"','"+val+"')"
            self.driver.execute_script(js)

    def text_is_exist_no_wait(self,loc,text):
        result = EC.text_to_be_present_in_element(loc,text)(self.driver)
        logging.info('元素：{}是否存在text：{}'.format(loc,text))
        return result

    def text_is_exist(self,loc,text):
        try:
            WebDriverWait(self.driver,5,0.5).until(EC.text_to_be_present_in_element(loc,text))
        finally:
            result = EC.text_to_be_present_in_element(loc,text)(self.driver)
            logging.info('等待5s，元素：{}是否存在text：{}'.format(loc,text))
            return result
        
    def ele_is_exist(self,loc):
        try:
            WebDriverWait(self.driver,5,0.5).until(EC.visibility_of_element_located(loc))
        finally:
            result = EC.visibility_of_element_located(loc)
            logging.info('等待5s，元素：{}是否存在'.format(loc))
            return result

    def hover(self,loc):
        try:
            action = ActionChains(self.driver)
            loc_ele = self.driver.find_element(*loc)
            action.move_to_element(loc_ele).perform()
        except (BaseException):
            self.png_to_allure()

    #处理滚动条
    # def scroll_to_position(self,p):
    #     js = "var q=document.body.scrollTop="+p
    #     self.driver.execute_script(js)

    def scroll_to_ele(self,loc):
        try:
            target = self.driver.find_element(*loc)
            # self.driver.execute_script("arguments[0].scrollIntoView();",target)
            # self.driver.execute_script("$('"+css+"').get(0).scrollIntoView();")
            self.driver.execute_script("arguments[0].focus();", target)
            logging.info('滚动元素：{}'.format(loc))
        except (BaseException):
            self.png_to_allure()


    def scroll(self,css,i):
        try:
            css = css.replace('\xa0',' ')
            self.driver.execute_script("$('"+css+"').get("+i+").scrollIntoView();")
        except (BaseException):
            self.png_to_allure()

    def png_to_allure(self):
        
        filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.driver.save_screenshot(os.path.abspath('.')+'\\file\\screen\\'+self.date_log+'\\'+filename+'.png')
        with open(os.path.abspath('.')+'\\file\\screen\\'+self.date_log+'\\'+filename+'.png','rb') as f:
            file = f.read()
        print(os.path.abspath('.')+'\\file\\screen\\'+self.date_log+'\\'+filename+'.png')
        allure.attach(file,'',allure.attachment_type.PNG)
        logging.info('打印截图：{}'.format(os.path.abspath('.')+'\\file\\screen\\'+self.date_log+'\\'+filename+'.png'))


        


