import pandas as pd
import numpy as np
import re
from py2neo import Node,Relationship,Graph,NodeMatcher,RelationshipMatcher

# 创建节点
def CreateNode(m_graph,m_label,m_attrs):
    #根绝节点name属性，查找节点
    m_n="_.name="+"\'"+m_attrs['name']+"\'"
    matcher = NodeMatcher(m_graph)
    re_value = matcher.match(m_label).where(m_n).first()
    #print(re_value)
    if re_value is None:
        m_mode = Node(m_label,**m_attrs)
        n = graph.create(m_mode)
        return n
    return None
# 查询节点
def MatchNode(m_graph,m_label,m_attrs):
    m_n="_.name="+"\'"+m_attrs['name']+"\'"
    matcher = NodeMatcher(m_graph)
    re_value = matcher.match(m_label).where(m_n).first()
    return re_value
# 创建关系
def CreateRelationship(m_graph,m_label1,m_attrs1,m_label2,m_attrs2,m_r_name):
    reValue1 = MatchNode(m_graph,m_label1,m_attrs1)
    reValue2 = MatchNode(m_graph,m_label2,m_attrs2)
    if reValue1 is None or reValue2 is None:
        return False
    m_r = Relationship(reValue1,m_r_name,reValue2)
    n = graph.create(m_r)
    return n

#查找关系
def findRelationship(m_graph,m_label1,m_attrs1,m_label2,m_attrs2,m_r_name):
    reValue1 = MatchNode(m_graph, m_label1, m_attrs1)
    reValue2 = MatchNode(m_graph, m_label2, m_attrs2)
    if reValue1 is None or reValue2 is None:
        return False
    m_r = Relationship(reValue1, m_r_name['name'], reValue2)
    return m_r

def updateRelation(m_graph,m_label1,m_attrs1,m_label2,m_attrs2,m_r_name):
    reValue1 = MatchNode(m_graph, m_label1, m_attrs1)
    reValue2 = MatchNode(m_graph, m_label2, m_attrs2)
    if reValue1 is None or reValue2 is None:
        return False
    print(m_r_name)
    propertyes={'value': m_r_name['value'], 'danwei': m_r_name['danwei']}
    m_r = Relationship(reValue1, m_r_name['name'], reValue2,**propertyes)
    graph.merge(m_r)

#修改节点属性
def updateNode(m_graph,m_label1,m_attrs1,new_attrs):
    reValue1 = MatchNode(m_graph, m_label1, m_attrs1)
    if reValue1 is None:
        return False
    reValue1.update(new_attrs)
    graph.push(reValue1)



graph = Graph('http://localhost:7474',username='neo4j',password='fengge666')

#获取指定文件夹下的excel
import os
def get_filename(path,filetype):  # 输入路径、文件类型例如'.xlsx'
    name = []
    for root,dirs,files in os.walk(path):
        for i in files:
            if os.path.splitext(i)[1]==filetype:
                name.append(i)
    return name            # 输出由有后缀的文件名组成的列表

def read_real_where_name():
    file='data2/gu_jin_lng_lat.xlsx'
    data=pd.read_excel(file)
    gu_name=list(data.gu_name)
    return gu_name

def read_where(author,file,gu_name):
    data=pd.read_excel(file)
    date=list(data.data)
    where_name=list(data.wheres)
    things=list(data.things)
    for i in range(len(date)):
        #处理地区，满足我们需要的地区条件
        where_list=where_name[i].split(',')
        for it in where_list:
            if it in gu_name and it!='无':
                attr1={"name":things[i],"date":date[i],"where_name":where_name[i]}
                CreateNode(graph, things_label, attr1)
                print("创建事件：" + things[i] + "-成功！！")

                attr2 = {"name": author}
                # 创建关系
                m_r_name1 = "事迹"
                reValue1 = CreateRelationship(graph, author_label, attr2, things_label, attr1, m_r_name1)
                print("创建关系：" + author + "-事迹-" + things[i] + "-成功")
                break



if __name__ == '__main__':
    file = 'author/'
    lists = get_filename(file, '.xlsx')
    gu_name = read_real_where_name()
    author_label='author'
    things_label='things'
    for it in lists:
        newfile = file + it
        print(newfile)
        author = it.split('.')[0]
        print(author)
        read_where(author,newfile,gu_name)





