
from pages.basePage import Page
from selenium.webdriver.common.by import By
import time
from common import param

class ReportDesignPage(Page):

    def sql_search(self,datasource,sql):
        #选择数据源
        self.select_datasource(datasource)
        #点击数据源
        self.datasource_click(datasource)
        self.input_sql(sql)
        result = self.get_result()
        return result


    def sql_search_pubulic(self,datasource,sql):
        #其他模块进入后，先回到父frame
        menu = self.get_show_frame_title()
        self.to_frame(param.report_design_menu)     
        result = self.sql_search(datasource,sql)
        self.to_frame(menu)
        return result

    datasource = (By.XPATH,'//*[@id="container"]/div/ul/li[2]/a')
    # connectsource_btn = (By.XPATH,'//div[@id="_datasource_container"]/button/i[@class="ureport ureport-shareconnection"]')
    connectsource_btn = (By.XPATH,'//button[@title="添加内置数据源连接"]')
    selected_source = (By.XPATH,'//a[@class="ds_name"]')
    # connectsource = (By.XPATH,'/html/body/div[4]')
    connectsource_result_str = '/html/body/div[@class="modal fade in"]'
    select_datasource_str = '//div[@class="modal-body"]/table[@class="table table-bordered"]/tbody/tr'
    def select_datasource(self,dataSource):
        #点击数据源按钮
        self.move_to_element_click(self.datasource)
        # if self.find_element_attr(self.datasource,'aria-expanded')[0] == 'false':
        #     time.sleep(2)
        sources = []
        if self.is_exist_no_wait(self.selected_source) == True:
            sources = self.get_eles_text(self.selected_source)
        if dataSource not in sources :
            if self.ele_is_exist(self.connectsource_btn) == False:
                time.sleep(3)   

            self.move_to_element_click(self.connectsource_btn)
            if self.is_display_no_wait((By.XPATH,self.connectsource_result_str)) == False:
                time.sleep(5)   

            dataSources = self.get_eles_text((By.XPATH,self.select_datasource_str+'/td[1]'))
            i = 0 
            for source in dataSources:
                i = i + 1
                if source == dataSource:
                    self.move_to_element_click((By.XPATH,self.select_datasource_str+'['+str(i)+']/td[2]/a/i'))
                    break
    
    add_data_context_str = '//ul[@class="context-menu-list context-menu-root"]'
    def datasource_click(self,dataSource):
        source_a = (By.LINK_TEXT,dataSource)
        self.context_click(source_a)

        elements = self.find_elements((By.XPATH,self.add_data_context_str))
        for i in range(1,len(elements)+1):
            if self.is_display_no_wait((By.XPATH,self.add_data_context_str+'['+str(i)+']')) == True:
                self.move_to_element_click((By.XPATH,self.add_data_context_str+'['+str(i)+']/li[1]/span'))

    # sql_diglog_str = '/html/body/div[6]'
    def input_sql(self,sql):
        if self.is_display_no_wait((By.XPATH,self.connectsource_result_str)) == False:
            time.sleep(5)
        self.clear((By.XPATH,self.connectsource_result_str+'/div/div/div[2]/div/div[2]/div[2]/textarea'))
        self.send_keys((By.XPATH,self.connectsource_result_str+'/div/div/div[2]/div/div[2]/div[2]/textarea'),sql)

        self.move_to_element_click((By.XPATH,self.connectsource_result_str+'/div/div/div[@class="modal-footer"]/button[1]'))
    

    sql_look_btn = (By.XPATH,'//div[@class="modal fade in"]/div/div/div[@class="modal-footer"]/button')
    sql_close_btn = (By.XPATH,'//div[@class="modal fade in"]/div/div/div[@class="modal-header"]/button')
    def get_result(self):
        results = self.get_eles_text((By.XPATH,self.connectsource_result_str+'/div/div/div[2]/table/tbody/tr/td'))
        self.move_to_element_click(self.sql_look_btn)
        self.move_to_element_click(self.sql_close_btn)
        return results

 
    def to_frame(self,frame):
        self.switch_to_parent_frame() 
        self.move_to_element_click((By.XPATH,'//ul[@id="page_tab_ul"]/li[@title="'+frame+'"]'))
        self.switch_frame((By.XPATH,'//div[@title="'+frame+'"]/iframe'))


    def get_show_frame_title(self):
        self.switch_to_parent_frame()
        title = self.find_element_attr((By.XPATH,'//div[@class="page_iframe_li page_show"]'),'title')
        return title[0]


    

        

        



        
