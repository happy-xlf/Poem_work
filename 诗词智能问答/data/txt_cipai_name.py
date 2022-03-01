# -*- coding: utf-8 -*- 
# @Time : 2021/12/24 20:17 
# @Author : xlf
# @File : txt_cipai_name.py
from 诗词智能问答.utils.mysqlhelper import MySqLHelper
import pandas as pd

def txt_cipai_name():

    data=pd.read_excel('cipai_name.xlsx')
    cn=data.get('title')
    with open("../dict/cipai_name.txt", "w",encoding='utf-8') as f:
        for it in cn:
            f.write(it)  # 自带文件关闭功能，不需要再写f.close()
            f.write("\n")

def txt_qupai_name():
    data = pd.read_excel('qupai_name.xlsx')
    cn = data.get('qu_name')
    with open("../dict/qupai_name.txt", "w", encoding='utf-8') as f:
        for it in cn:
            f.write(it)  # 自带文件关闭功能，不需要再写f.close()
            f.write("\n")

if __name__ == '__main__':
    txt_qupai_name()