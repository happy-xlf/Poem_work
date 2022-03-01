# -*- coding: utf-8 -*- 
# @Time : 2021/12/30 15:17 
# @Author : xlf
# @File : txt_get_allpoem.py

from py2neo import Graph
import pandas as pd


g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="fengge666")
sql = "MATCH (m:poem) return m.name"
data=g.run(sql).data()
poem_name = [i['m.name'] for i in data]
print(poem_name)
with open("../dict/poem.txt", "w", encoding='utf-8') as f:
    for it in poem_name:
        f.write(it)  # 自带文件关闭功能，不需要再写f.close()
        f.write("\n")