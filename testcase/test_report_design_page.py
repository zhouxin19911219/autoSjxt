import sys
sys.path.append('.')
from pages.reportDesignPage import ReportDesignPage
from pages.indexPage import IndexPage
import time
from common import param
import pytest



class Test_reportDesign_Page():

    # def sql_search(self,reportDesignPage,datasource,sql):
    #     #选择数据源
    #     reportDesignPage.select_datasource(datasource)
    #     #点击数据源
    #     reportDesignPage.datasource_click(datasource)
    #     reportDesignPage.input_sql(sql)
    #     result = reportDesignPage.get_result()
    #     return result


    # def sql_search_pubulic(self,driver,datasource,sql):
    #     reportDesignPage = ReportDesignPage(driver)
    #     #其他模块进入后，先回到父frame
    #     menu = reportDesignPage.get_show_frame_title()
    #     reportDesignPage.to_frame(param.report_design_menu)     
    #     result = self.sql_search(reportDesignPage,datasource,sql)
    #     reportDesignPage.to_frame(menu)
    #     return result
    pass
