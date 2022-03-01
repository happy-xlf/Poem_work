import pandas as pd
import numpy as np
import re
from py2neo import Node,Relationship,Graph,NodeMatcher,RelationshipMatcher

# 创建节点
def CreateNode(m_graph,m_label,m_attrs):
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

def create_common_name():
    file = './data2/common_name.xlsx'
    data = pd.read_excel(file).fillna("无")
    hc=list(data.hc)
    author=list(data.author)
    common_name_label="common_name"
    author_label="author"
    for i in range(len(hc)):
        common_name=hc[i]
        authors=author[i].split(',')
        attr1={"name":common_name}
        CreateNode(graph, common_name_label, attr1)
        print("创建合称："+common_name+"成功！！")

        for it in authors:
            attr2={"name":it}
            # 创建关系
            m_r_name1 = "合称"
            reValue1 = CreateRelationship(graph, author_label, attr2, common_name_label, attr1, m_r_name1)
            print("创建关系：" + it + "-合称-" + common_name + "成功")

            # 创建关系
            m_r_name2 = "包含"
            reValue2 = CreateRelationship(graph,common_name_label, attr1, author_label, attr2,  m_r_name2)
            print("创建关系：" + common_name + "-包含-" + it+ "成功")



if __name__ == '__main__':
    create_common_name()





