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


def create_sentence():
    file='./data2/author.xlsx'
    data=pd.read_excel(file).fillna("无")
    author=list(data.author)
    produce=list(data.produce)
    num=list(data.num)
    src=list(data.src)
    desty=list(data.desty)
    bg_time=list(data.begin_time)
    ed_time=list(data.end_time)
    zi_list=list(data.zi)
    hao_list=list(data.hao)
    author_label='author'
    desty_label='desty'
    for i in range(len(author)):
        print("第"+str(i)+"个")
        attr1 = {"name": author[i], "produce": produce[i], "num": num[i],
                 "src": src[i],"bg_time":bg_time[i],"ed_time":ed_time[i],"zi":zi_list[i],"hao":hao_list[i]}
        CreateNode(graph, author_label, attr1)
        print("创建诗人：" + author[i] + "成功！！")
        attr2={"name":desty[i]}
        if MatchNode(graph,desty_label,attr2)==None:
            CreateNode(graph,desty_label,attr2)
            print("创建朝代："+desty[i]+"成功！！")
        #创建关系
        m_r_name1 = "朝代"
        reValue1 = CreateRelationship(graph, author_label, attr1, desty_label, attr2, m_r_name1)
        print("创建关系："+author[i]+"-所属朝代-"+desty[i]+"成功")
        m_r_name2 = "包含"
        reValue2 = CreateRelationship(graph,desty_label, attr2, author_label, attr1,  m_r_name2)
        print("创建关系：" + desty[i] + "-包含-" + author[i] + "成功")

def test():
    matcher = NodeMatcher(graph)
    re_value = matcher.match('ci_name').where("_.name='金刚随机无尽颂'")
    data=list(re_value)
    print(data)




if __name__ == '__main__':
    for i in range(100000):
        print(i)





