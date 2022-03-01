# -*- coding: utf-8 -*- 
# @Time : 2021/12/24 19:56 
# @Author : xlf
# @File : txt_author.py

from 诗词智能问答.utils.mysqlhelper import MySqLHelper


def txt_author():
    author=[]
    db=MySqLHelper()
    sql="select * from author"
    ret,count=db.selectall(sql=sql)
    for row in ret:
        author_name=str(row[0])
        author.append(author_name)
    with open("../dict/author.txt", "w",encoding='utf-8') as f:
        for it in author:
            f.write(it)  # 自带文件关闭功能，不需要再写f.close()
            f.write("\n")

if __name__ == '__main__':
    txt_author()