# -*- coding: utf-8 -*- 
# @Time : 2021/12/24 20:40 
# @Author : xlf
# @File : txt_poem.py
from 诗词智能问答.utils.mysqlhelper import MySqLHelper


def txt_poem():
    poem_list=[]
    db=MySqLHelper()
    desty=['tang']
    for dd in desty:
        sql="select * from "+str(dd)+""
        ret,count=db.selectall(sql=sql)
        for row in ret:
            poem_name=str(row[0])
            poem_list.append(poem_name)
    with open("../dict/tang_poem.txt", "w",encoding='utf-8') as f:
        for it in poem_list:
            f.write(it)  # 自带文件关闭功能，不需要再写f.close()
            f.write("\n")

if __name__ == '__main__':
    txt_poem()