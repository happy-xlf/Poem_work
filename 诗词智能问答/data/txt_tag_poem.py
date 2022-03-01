# -*- coding: utf-8 -*- 
# @Time : 2021/12/24 20:26 
# @Author : xlf
# @File : txt_tag_poem.py
import pandas as pd

def txt_tag():

    data=pd.read_excel('tag_name.xlsx')
    cn=data.get('tag')
    with open("../dict/tag.txt", "w",encoding='utf-8') as f:
        for it in cn:
            f.write(it)  # 自带文件关闭功能，不需要再写f.close()
            f.write("\n")


if __name__ == '__main__':
    txt_tag()