# -*- coding: utf-8 -*- 
# @Time : 2021/12/24 19:56 
# @Author : xlf
# @File : txt_common_name.py

from 诗词智能问答.utils.mysqlhelper import MySqLHelper
import pandas as pd

def txt_common_name():

    data=pd.read_excel('common_name.xlsx')
    cn=data.get('hc')
    with open("../dict/common_name.txt", "w",encoding='utf-8') as f:
        for it in cn:
            f.write(it)  # 自带文件关闭功能，不需要再写f.close()
            f.write("\n")

if __name__ == '__main__':
    txt_common_name()