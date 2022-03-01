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


#获取指定文件夹下的excel
import os
def get_filename(path,filetype):  # 输入路径、文件类型例如'.xlsx'
    name = []
    for root,dirs,files in os.walk(path):
        for i in files:
            if os.path.splitext(i)[1]==filetype:
                name.append(i)
    return name            # 输出由有后缀的文件名组成的列表

def create_poem():
    file = 'data/'
    lists = get_filename(file, '.xlsx')
    for it in lists:
        newfile = file + it
        print(newfile)
        # 获取诗词内容
        data = pd.read_excel(newfile).fillna("无")

        title=list(data.title)
        desty=list(data.desty)
        author=list(data.author)
        content=list(data.content)
        trans_content=list(data.trans_content)
        background=list(data.background)
        tag=list(data.tag)
        formal=list(data.formal)
        date=list(data.data)
        ci_name=list(data.ci_name)
        qu_name=list(data.qu_name)

        poem_label='poem'
        author_label='author'
        desty_label='desty'
        formal_label='formal'
        tag_label='tag'
        cipai_label='ci_pai'
        qupai_label='qu_pai'

        for i in range(len(title)):
            print("第"+str(i)+"个")
            attr1 = {"name": title[i], "content": content[i], "trans_content": trans_content[i],
                     "background": background[i],"date":date[i]}
            CreateNode(graph, poem_label, attr1)
            print("创建诗词：" + title[i] + "成功！！")
            if tag[i]!='无':
                tag_list=tag[i].split(',')
                for it in tag_list:
                    attr2={"name":it}
                    # 创建关系
                    m_r_name1 = "分类"
                    reValue1 = CreateRelationship(graph, poem_label, attr1, tag_label, attr2, m_r_name1)
                    print("创建关系：" + title[i] + "-所属类别-" + it + "成功")
                    m_r_name2 = "包含"
                    reValue2 = CreateRelationship(graph, tag_label, attr2, poem_label, attr1, m_r_name2)
                    print("创建关系：" + it + "-包含-" + title[i] + "成功")
            if formal[i]!='无':
                attr2={"name":formal[i]}
                # 创建关系
                m_r_name1 = "形式"
                reValue1 = CreateRelationship(graph, poem_label, attr1, formal_label, attr2, m_r_name1)
                print("创建关系：" + title[i] + "-所属形式-" + formal[i] + "成功")
                m_r_name2 = "包含"
                reValue2 = CreateRelationship(graph, formal_label, attr2, poem_label, attr1, m_r_name2)
                print("创建关系：" + formal[i] + "-包含-" + title[i] + "成功")
            if ci_name[i]!='无':
                attr2 = {"name": ci_name[i]}
                if MatchNode(graph, cipai_label, attr2) == None:
                    CreateNode(graph, cipai_label, attr2)
                    print("创建词牌名：" + ci_name[i] + "成功！！")
                # 创建关系
                m_r_name1 = "词牌名"
                reValue1 = CreateRelationship(graph, poem_label, attr1, cipai_label, attr2, m_r_name1)
                print("创建关系：" + title[i] + "-词牌名-" + ci_name[i] + "成功")
                m_r_name2 = "包含"
                reValue2 = CreateRelationship(graph, cipai_label, attr2, poem_label, attr1, m_r_name2)
                print("创建关系：" + ci_name[i] + "-包含-" + title[i] + "成功")
            if qu_name[i]!='无':
                attr2 = {"name": qu_name[i]}
                if MatchNode(graph, qupai_label, attr2) == None:
                    CreateNode(graph, qupai_label, attr2)
                    print("创建曲牌名：" + qu_name[i] + "成功！！")
                # 创建关系
                m_r_name1 = "曲牌名"
                reValue1 = CreateRelationship(graph, poem_label, attr1, qupai_label, attr2, m_r_name1)
                print("创建关系：" + title[i] + "-曲牌名-" + qu_name[i] + "成功")
                m_r_name2 = "包含"
                reValue2 = CreateRelationship(graph, qupai_label, attr2, poem_label, attr1, m_r_name2)
                print("创建关系：" + qu_name[i] + "-包含-" + title[i] + "成功")
            if author[i]!='无':
                #创建作者写作关系
                attr2={"name":author[i]}
                if MatchNode(graph,author_label,attr2)!=None:
                    #创建关系
                    m_r_name1 = "写作"
                    reValue1 = CreateRelationship(graph, author_label, attr2, poem_label, attr1, m_r_name1)
                    print("创建关系："+author[i]+"-写作-"+title[i]+"成功")
                    m_r_name2 = "作者"
                    reValue2 = CreateRelationship(graph,poem_label, attr1, author_label, attr2,  m_r_name2)
                    print("创建关系：" + title[i] + "-作者-" + author[i] + "成功")
            if desty[i]!='无':
                attr2 = {"name": desty[i]}
                if MatchNode(graph, desty_label, attr2) == None:
                    CreateNode(graph, desty_label, attr2)
                    print("创建朝代：" + desty[i] + "成功！！")
                # 创建关系
                m_r_name1 = "朝代"
                reValue1 = CreateRelationship(graph, poem_label, attr1, desty_label, attr2, m_r_name1)
                print("创建关系：" + title[i] + "-所属朝代-" + desty[i] + "成功")
                m_r_name2 = "包含诗词"
                reValue2 = CreateRelationship(graph, desty_label, attr2, poem_label, attr1, m_r_name2)
                print("创建关系：" + desty[i] + "-包含-" + title[i] + "成功")


if __name__ == '__main__':
    create_poem()





