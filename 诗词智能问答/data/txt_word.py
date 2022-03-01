# -*- coding: utf-8 -*- 
# @Time : 2021/12/24 20:21 
# @Author : xlf
# @File : txt_word.py
import pandas as pd

def txt_word():

    data=pd.read_excel('word.xlsx')
    cn=data.get('word')
    with open("../dict/word.txt", "w",encoding='utf-8') as f:
        for it in cn:
            f.write(it)  # 自带文件关闭功能，不需要再写f.close()
            f.write("\n")


if __name__ == '__main__':
    txt_word()