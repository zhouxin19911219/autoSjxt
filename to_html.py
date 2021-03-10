

import pytest
import os
import time
import json

if __name__ == '__main__':

    file_path = './report/html/widgets/history-trend.json'
    if os.path.exists(file_path) == True:
        file_before = open(file_path,encoding='utf-8')
        datas_before = file_before.readlines()
        file_before.close()
        data_before = ''.join(datas_before)
        data_before_result = data_before.split('[')[1].split(']')[0]
        

    os.system('allure generate report -o report/html --clean')


    while os.path.exists('./report/html')==False:
        time.sleep(2)
    
    if os.path.exists(file_path) == True:
        file_after = open(file_path,encoding='utf-8')
        datas_after = file_after.readlines()
        file_after.close()
        data_after = ''.join(datas_after)
        result = '['+data_after.split('[')[1].split(']')[0]+','+data_before_result+']'
        print('result:'+result)

        file_result = open(file_path,'w',encoding='utf-8')
        file_result.writelines(result)
        file_result.close()





    
    os.system('allure open report/html')





