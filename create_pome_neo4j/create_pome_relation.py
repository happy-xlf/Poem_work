import pandas as pd
import numpy as np
import re
from py2neo import Node,Relationship,Graph,NodeMatcher,RelationshipMatcher

# 创建节点
def CreateNode(m_graph,m_label,m_attrs):
    m_n="_.name="+"\'"+m_attrs['name']+"\'"
    matcher = NodeMatcher(m_graph)
    re_value = matcher.match(m_label).where(m_n).first()
    print(re_value)
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



def get_data():
    #title = [], desty = [], author = [], content = [], trans_content = [], appear = [], background = []
    file = 'tang.xlsx'
    data = pd.read_excel(file).fillna("无")

    title = list(data.title)
    desty=list(data.desty)
    author=list(data.author)
    content=list(data.content)
    trans_content=list(data.trans_content)
    appear=list(data.appear)
    background=list(data.background)
    label1="pome"
    label2="author"
    label3="desty"
    for i in range(len(title)):
        if title[i]==" nan":
            title[i]=""
        if content[i]==" nan":
            content[i]=""
        if trans_content[i]==" nan":
            trans_content[i]=""
        if appear[i]==" nan":
            appear[i]=""
        if background[i]==" nan":
            background[i]=""
        attr1={"name":title[i],"content":content[i],"trans_content":trans_content[i],"appear":appear[i],"background":background[i]}
        CreateNode(graph, label1, attr1)
        attr2 = {"name": author[i]}
        if MatchNode(graph,label2,attr2)==None:
            CreateNode(graph, label2, attr2)
        attr3 = {"name": desty[i]}
        CreateNode(graph, label3, attr3)
        m_r_name = "创作"
        reValue = CreateRelationship(graph,label2,attr2,label1,attr1,m_r_name)
        m_r_name2 = "朝代"
        reValue2 = CreateRelationship(graph, label1, attr1, label3, attr3, m_r_name2)
        print(reValue)
        print(reValue2)

def update_author():
    label2 = "author"
    file = "author.xlsx"
    data = pd.read_excel(file).fillna("无")

    file2 = "src.xlsx"
    data2=pd.read_excel(file2).fillna("无")


    produce = list(data.produce)
    # 获取诗人名字
    name = list(data.author)
    bg = []
    ed = []
    zi = []
    hao = []
    pome_self = []

    # 获取诗人诗集数目
    num = list(data.num)

    for it in produce:
        # 获取诗人个人简介
        pome_self.append(it)
        # 获取诗人出生，去世的年份
        datas = re.findall(r"\d+", it)
        if len(datas) != 0 and len(datas) != 1:
            bg.append(datas[0] + "年")
            # print("生于"+datas[0])
            flag = False
            for j in range(1, len(datas)):
                if len(datas[j]) >= len(datas[0]) and int(datas[j]) - int(datas[0]) > 15:
                    ed.append(datas[j] + "年")
                    # print("死于"+datas[j])
                    flag = True
                    break
            if flag == False:
                ed.append("无")
        else:
            bg.append("无")
            ed.append("无")

        # 获取诗人，字，号
        ztext = re.findall(r".*字(.*?)[，|。]", it)
        if len(ztext) != 0:
            zi.append(ztext)
        else:
            zi.append("无")
        # print(ztext)
        htext = str(re.findall(r".*号(.*?)[，|。]", it)).replace('“', '').replace('”', '')
        if len(htext) != 0:
            hao.append(htext)
        else:
            hao.append("无")

    for i in range(len(zi)):
        attr={"name":name[i]}
        newattr={"name":name[i],"生于":bg[i],"去世于":ed[i],"字":zi[i],"号":hao[i],"数目":num[i],"简介":pome_self[i]}
        if updateNode(graph,label2,attr,newattr)==False:
            print("没有该诗人"+name[i])
            CreateNode(graph,label2,newattr)




if __name__ == '__main__':
    get_data()





