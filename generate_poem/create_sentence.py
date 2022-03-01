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


def create_sentence():
    file = 'sentences/'
    lists = get_filename(file, '.xlsx')
    for it in lists:
        newfile = file + it
        print(newfile)

        # 获取诗词内容
        data = pd.read_excel(newfile).fillna("无")

        sentens = list(data.sentens)
        author = list(data.author)
        title = list(data.title)
        keys = list(data.word)

        sentence_label='sentence'
        word_label='word'
        if len(sentens)>50000:
            lenth=50000
        else:
            lenth=len(sentens)
        for i in range(lenth):
            print("第" + str(i) + "个")
            attr1 = {"name": sentens[i], "author": author[i], "title": title[i]}
            CreateNode(graph, sentence_label, attr1)
            print("创建诗句：" + sentens[i] + "成功！！")
            word_list=keys[i].split(',')
            for it in word_list:
                attr2 = {"name": it}
                # 创建关系
                m_r_name1 = "关键字"
                reValue1 = CreateRelationship(graph, sentence_label, attr1, word_label, attr2, m_r_name1)
                print("创建关系：" + sentens[i] + "-关键字-" + it + "成功")
                m_r_name2 = "诗句"
                reValue2 = CreateRelationship(graph, word_label, attr2, sentence_label, attr1, m_r_name2)
                print("创建关系：" + it + "-诗句-" + sentens[i] + "成功")



if __name__ == '__main__':
    create_sentence()





