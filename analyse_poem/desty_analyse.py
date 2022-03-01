import pandas as pd
import numpy as np
import re
from py2neo import Node,Relationship,Graph,NodeMatcher,RelationshipMatcher
from analyse_poem.utils.mysqlhelper import MySqLHelper

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


def sum_desty():
    matcher = NodeMatcher(graph)
    relationship_matcher=RelationshipMatcher(graph)
    desty_list=['唐代','宋代','元代','明代','清代']
    desty_len=[]
    for i in range(len(desty_list)):
        node1 = matcher.match('desty').where("_.name="+"\'"+desty_list[i]+"\'").first()
        relationship = list(relationship_matcher.match([node1], r_type='包含诗词'))
        desty_len.append(len(relationship))
        print(desty_list[i]+": "+str(len(relationship)))
    print(desty_len)

def sum_poem():
    matcher = NodeMatcher(graph)
    relationship_matcher=RelationshipMatcher(graph)
    desty_list=['唐代','宋代','元代','明代','清代']
    desty_len=[]
    for i in range(len(desty_list)):
        node1 = matcher.match('desty').where("_.name="+"\'"+desty_list[i]+"\'").first()
        relationship = list(relationship_matcher.match([node1], r_type='包含'))
        desty_len.append(len(relationship))
        print(desty_list[i]+": "+str(len(relationship)))
    print(desty_len)

def poem_desty_produce():
    matcher = NodeMatcher(graph)
    relationship_matcher = RelationshipMatcher(graph)
    desty_list = ['唐代', '宋代', '元代', '明代', '清代']
    for i in range(len(desty_list)):
        node1 = matcher.match('desty').where("_.name=" + "\'" + desty_list[i] + "\'").first()
        relationship = list(relationship_matcher.match([node1], r_type='包含'))
        print(desty_list[i] + ": " )
        print(relationship)

def tts():
    data = graph.run(
        'match data=(p:desty{name:'"'宋代'"'})-[r:`包含`]->(a:author)  return a.name,a.src,a.produce LIMIT 10000 ').data()
    data_list=[]
    i=0
    for it in data:
        name=it.get('a.name')
        src=it.get('a.src')
        produce=it.get('a.produce')
        if i<8 and src!='http://www.huihua8.com/uploads/allimg/20190802kkk01/1531722472-EPucovIBNQ.jpg':
            print(name+" "+src+" "+produce)
            result={}
            result['name']=name
            result['src']=src
            result['produce']=produce
            data_list.append(result)
            i=i+1
        elif i==8:
            break
    print(data_list)
    k=json.dumps(data_list)
    print(k)

def desty_poem():
    data = graph.run(
        'match data=(p:desty{name:'"'唐代'"'})-[r:`包含诗词`]->(a:poem)  return a.name,a.content,a.date,a.background,a.trans_content LIMIT 1000 ').data()
    data_list=[]
    i=0
    for it in data:
        name=it.get('a.name')
        content=str(it.get('a.content')).replace('\n','')
        date=it.get('a.date')
        background = it.get('a.background')
        trans=str(it.get('a.trans_content')).replace('\n','')

        kind=graph.run(
        'match data=(p:poem{name:'+"'"+name+"'"+'})-[r:`分类`]->(a:tag)  return a.name').data()
        pomer = graph.run(
            'match data=(p:poem{name:' + "'" + name + "'" + '})-[r:`作者`]->(a:author)  return a.name').data()
        formal = graph.run(
            'match data=(p:poem{name:' + "'" + name + "'" + '})-[r:`形式`]->(a:formal)  return a.name').data()
        formal_name=""
        if len(formal)!=0:
            formal_name = str(formal[0].get('a.name'))
        poem_kind=""
        for kit in kind:
            poem_kind=poem_kind+str(kit.get('a.name'))+","

        if len(pomer)!=0:
            author_name = pomer[0].get('a.name')
            print(name)
            print(author_name)
            print("分类：" + poem_kind)
            print("诗词形式："+formal_name)
            print(content)
            print(date)
            print(background)
            print(trans)
            result={}
            result['name']=name
            result['author_name']=author_name
            result['']
            data_list.append(result)

def read_where():
    data=pd.read_excel('../爬取信息/古今地名/gu_jin_lng_lat.xlsx')
    gu_name=list(data.get('gu_name'))
    return gu_name

def travel_poem(name):
    gu_name=read_where()
    data = graph.run(
        'match data=(p:author{name:'+"'"+name+"'"+'})-[r:`事迹`]->(a:things)  return a.where_name,a.date,a.name').data()
    data_list = []
    i = 0
    ans=[]
    for it in data:
        where_name = it.get('a.where_name')
        date = it.get('a.date')
        things_name = it.get('a.name')
        where_list=str(where_name).split(',')
        for it in where_list:
            if it in gu_name:
                ans.append(it)
                print(date+" "+things_name+" "+it)
    ans=list(set(ans))
    ans=",".join(ans)
    print(ans)
def common_name(name):
    data = graph.run(
        'match data=(p:author{name:'+"'"+name+"'"+'})-[r:`合称`]->(a:common_name)  return a.name').data()
    ans = []
    for it in data:
        name = it.get('a.name')
        ans.append(name)
    ans=",".join(ans)
    print(ans)

def zuopin(name):
    data = graph.run(
        'match data=(p:author{name:' + "'" + name + "'" + '})-[r:`写作`]->(a:poem)  return a.name limit 30').data()
    ans = []
    for it in data:
        name = it.get('a.name')
        ans.append(name)
    ans = ",".join(ans)
    print(ans)
    return ans

def things(name):
    data = graph.run(
        'match data=(p:author{name:' + "'" + name + "'" + '})-[r:`事迹`]->(a:things)  return a.name,a.date,p.bg_time,p.ed_time').data()
    ans = []
    bg=int(str(data[0].get('p.bg_time')).replace('年',''))
    ed=int(str(data[0].get('p.ed_time')).replace('年',''))
    print(str(bg)+" "+str(ed))
    ans=[]
    current_time=-1
    dit = {}
    for i in range(len(data)):
        name = str(data[len(data)-i-1].get('a.name'))
        date=int(str(data[len(data)-i-1].get('a.date')).replace('年',''))
        if date>=bg and date<=ed:
            if current_time!=date:
                newdit={}
                if current_time!=-1:
                    newdit[current_time]=dit[current_time]
                    ans.append(newdit)
                current_time=date
                dit[date]=name
            else:
                dit[date]=dit[date]+"<br>"+name
    newdit = {}
    newdit[current_time] = dit[current_time]
    ans.append(newdit)
    print(ans)
    new_ans=[]
    for it in ans:
        for k in it:
            dit={}
            dit['time']=str(k)+"年"
            dit['things']=it[k]
            new_ans.append(dit)
    print(new_ans)

def new_things(name):
    data = graph.run(
        'match data=(p:author{name:' + "'" + name + "'" + '})-[r:`事迹`]->(a:things)  return a.name,a.date,p.bg_time,p.ed_time,p.produce').data()
    ans = []
    bg = int(str(data[0].get('p.bg_time')).replace('年', ''))
    ed = int(str(data[0].get('p.ed_time')).replace('年', ''))
    produce=str(data[0].get('p.produce')).split('。')[0]+"。"
    print(str(bg) + " " + str(ed))
    print(produce)
    ans = []
    current_time = -1
    dit = {}
    for i in range(len(data)):
        name = str(data[len(data) - i - 1].get('a.name'))
        date = int(re.findall(r'\d+',str(data[len(data) - i - 1].get('a.date')))[0])
        print(str(date)+" "+name)
        if date >= bg and date <= ed:
            if date not in dit.keys():
                dit[date] = name
            else:
                dit[date] = dit[date] + "<br>" + name
    jsonDate=[]
    jsonDate.append({'time':str(bg)+"年~"+str(ed)+"年",'things':produce})
    new_dit=sorted(dit)
    for it in new_dit:
        dict={}
        dict['time']=str(it)+"年"
        dict['things']=dit[it].replace(',','<br>')
        print(str(it)+" "+dit[it].replace(',','<br>'))
        jsonDate.append(dict)
    print(jsonDate)

def get_common_name(author_name):
    data = graph.run(
        'match data=(p:author{name:' + "'" + author_name + "'" + '})-[r:`合称`]->(a:common_name)  return a.name,p.src').data()
    common_list = []
    author_img_src=str(data[0].get('p.src'))
    other_src="/static/images/color_back.jpeg"
    ans_map={}
    ans = {}
    nodes = []
    edges = []
    i=0
    ans_map[author_name]=i
    i=i+1
    for it in data:
        name = it.get('a.name')
        ans_map[name]=i
        common_list.append(name)
        i=i+1
    #加入作者节点
    dit={}
    dit["name"]=author_name
    dit["image"]=author_img_src
    nodes.append(dit)
    for it in common_list:
        dic={}
        dic["name"]=it
        dic["image"]=other_src
        nodes.append(dic)

    #加入其他合称的作者节点与关系
    for it in common_list:
        data = graph.run(
            'match data=(p:common_name{name:' + "'" + it + "'" + '})-[r:`包含`]->(a:author)  return a.name,a.src').data()
        for k in data:
            qi_name=str(k.get('a.name'))
            qi_src=str(k.get('a.src'))
            if qi_name not in ans_map.keys():
                dic = {}
                dic["name"] = qi_name
                dic["image"] = qi_src
                nodes.append(dic)
                ans_map[qi_name] = i
                i=i+1
            dic = {}
            dic["source"] = ans_map[qi_name]
            dic["target"] = ans_map[it]
            dic["relation"] = "合称"
            edges.append(dic)

    ans["nodes"] = nodes
    ans["edges"] = edges
    print(json.dumps(ans).encode('utf-8').decode("unicode-escape"))


def get_friend_relation(author_name):
    data = graph.run(
        'match data=(p:author{name:' + "'" + author_name + "'" + '})-[r:`好友`]->(a:author) return p.bg_time,p.ed_time,p.src,a.name,a.src,a.bg_time,a.ed_time').data()
    bg_time=int(str(data[0].get('p.bg_time')).replace('年',''))
    ed_time=int(str(data[0].get('p.ed_time')).replace('年',''))
    friend_map={}
    friend_src={}
    ans = {}
    nodes = []
    edges = []
    i=0
    author_img_src=str(data[0].get('p.src'))
    friend_map[author_name]=i
    friend_src[author_name]=author_img_src
    #添加作者节点
    dit = {}
    dit["name"] = author_name
    dit["image"] = author_img_src
    nodes.append(dit)
    i=i+1
    friend_list=[]
    bg_time_list=[]
    ed_time_list=[]
    for it in data:
        name=str(it.get('a.name'))
        img_src=str(it.get('a.src'))
        a_bg_time=str(it.get('a.bg_time'))
        a_ed_time=str(it.get('a.ed_time'))
        if a_bg_time=='无' or a_ed_time=='无' or img_src=="http://www.huihua8.com/uploads/allimg/20190802kkk01/1531722472-EPucovIBNQ.jpg":
            continue
        a_bg_time=int(a_bg_time.replace('年',''))
        a_ed_time =int(a_ed_time.replace('年',''))
        if a_ed_time<bg_time or a_bg_time>ed_time:
            continue
        friend_map[name]=i
        friend_src[name]=img_src
        # 构建第一层作者关系网络
        dic = {}
        dic["name"] = name
        dic["image"] = friend_src[name]
        nodes.append(dic)

        edg_dic = {}
        edg_dic["source"] = 0
        edg_dic["target"] = friend_map[name]
        edg_dic["relation"] = "好友"
        edges.append(edg_dic)
        friend_list.append(name)
        bg_time_list.append(a_bg_time)
        ed_time_list.append(a_ed_time)
        i=i+1

    #构建第二层还有关系网
    for j in range(len(friend_list)):
        bg_time=bg_time_list[j]
        ed_time=ed_time_list[j]
        data = graph.run(
            'match data=(p:author{name:' + "'" + friend_list[j] + "'" + '})-[r:`好友`]->(a:author)  return p.bg_time,p.ed_time,p.src,a.name,a.src,a.bg_time,a.ed_time ').data()
        for kk in data:
            name=str(kk.get('a.name'))
            img_src=str(kk.get('a.src'))
            a_bg_time = str(kk.get('a.bg_time'))
            a_ed_time = str(kk.get('a.ed_time'))
            if a_bg_time == '无' or a_ed_time == '无' or img_src=="http://www.huihua8.com/uploads/allimg/20190802kkk01/1531722472-EPucovIBNQ.jpg":
                continue
            a_bg_time = int(a_bg_time.replace('年', ''))
            a_ed_time = int(a_ed_time.replace('年', ''))
            if a_ed_time < bg_time or a_bg_time > ed_time:
                continue
            if name not in friend_map.keys():
                friend_map[name]=i
                i=i+1
                friend_src[name]=img_src
                #添加新节点
                dic = {}
                dic["name"] = name
                dic["image"] = img_src
                nodes.append(dic)
            #添加对应的链接线
            edg_dic = {}
            edg_dic["source"] = friend_map[friend_list[j]]
            edg_dic["target"] = friend_map[name]
            edg_dic["relation"] = "好友"
            edges.append(edg_dic)
    ans["nodes"]=nodes
    ans["edges"]=edges
    print(json.dumps(ans))


def get_where_relation(author_name):
    address_data=pd.read_excel('gu_jin_lng_lat.xlsx')
    gu_name=list(address_data.get('gu_name'))

    data = graph.run(
        'match data=(p:author{name:' + "'" + author_name + "'" + '})-[r:`事迹`]->(a:things) return a.date,a.name,a.where_name').data()
    date_list=[]
    things_list=[]
    where_list=[]

    for it in data:
        date=str(it.get('a.date'))
        things=str(it.get('a.name'))
        where_name=str(it.get('a.where_name'))
        if things!='无':
            date_list.append(str(date))
            things_list.append(things)
            where_list.append(where_name)
    ans_list=[]
    ans_dic={}
    for i in range(len(date_list)):
        i=len(date_list)-i-1
        date=date_list[i]
        things=things_list[i]
        where_name=where_list[i].split(',')
        for k in where_name:
            if k in gu_name and k not in ans_dic:
                dit={}
                dit['name']=k
                dit['things']=date+","+things
                ans_dic[k]=date+","+things
                ans_list.append(dit)
                break
    new_ans_list=[]
    head=ans_list[0]['name']
    small = []
    small.append({"name": head})
    small.append({"name":head,"value":100,"things":ans_dic[head]})
    new_ans_list.append(small)
    for i in range(1,len(ans_list)):
        next=ans_list[i]['name']
        small=[]
        small.append({"name":head})
        small.append({"name":next,"value":100,"things":ans_dic[next]})
        new_ans_list.append(small)
    for i in range(1,len(ans_list)):
        if i==1:
            head=ans_list[i]['name']
            continue
        next=ans_list[i]['name']
        small = []
        small.append({"name": head})
        small.append({"name": next, "value": 100, "things": ans_dic[next]})
        new_ans_list.append(small)
        head=next
    ans_xlf={}
    ans_xlf["one"]=new_ans_list
    print(json.dumps(ans_xlf).encode('utf-8').decode("unicode-escape"))
import json

def get_all_lng_lat():
    address_data = pd.read_excel('gu_jin_lng_lat.xlsx')
    gu_name = list(address_data.get('gu_name'))
    lng=list(address_data.get('lng'))
    lat=list(address_data.get('lat'))
    ans={}
    for i in range(len(gu_name)):
        gu=gu_name[i]
        lg=lng[i]
        lt=lat[i]
        ans[gu]=[lg,lt]
    print(json.dumps(ans).encode('utf-8').decode("unicode-escape"))

def get_poem_about_things(poem_name):
    db=MySqLHelper()
    desty = ['tang', 'song', 'yuan', 'ming', 'qing']
    author=''
    bg_time=''
    for it in desty:
        sql = "select * from " + it + " where title = '" + poem_name + "';"
        ret = db.selectone(sql=sql)
        if ret!=None:
            author=ret[2]
            bg_time=str(ret[9]).replace('年','')
            break
    print(author)
    print(bg_time)
    date_list=[]
    back_list=[]
    poem_list=[]
    content_list=[]
    left=int(bg_time)-3
    right=int(bg_time)+3
    for it in desty:
        sql = "select * from " + it + " where author = '" + author + "';"
        ret,count = db.selectall(sql=sql)
        if ret!=None:
            for row in ret:
                if str(row[9])!='无' and str(row[9]).find('．')==-1 and str(row[9]).find('—')==-1 and str(row[6])!='无':
                    time=int(str(row[9]).replace('年',''))
                    if time>=left and time<=right and bool(re.search(r'\d', row[6])):
                        date_list.append(time)
                        back_list.append(row[6])
                        poem_list.append(row[0])
                        content_list.append(row[3])
    jsonData=[]
    for dd in range(left,right+1):
        for i in range(len(date_list)):
            time=date_list[i]
            poem=poem_list[i]
            back=back_list[i]
            content=content_list[i].replace('\n','').split('。')
            ans_content=[]
            for it in content:
                if it!='':
                    ans_content.append(it+"。")
            if time==dd:
                dic={}
                dic['date']=str(time)+"年"
                dic['title']=poem
                dic['back']=back
                dic['content']=ans_content
                jsonData.append(dic)
    print(json.dumps(jsonData).encode('utf-8').decode("unicode-escape"))


def test(name):
    db=MySqLHelper()
    sql = "select * from tang where title = '" + name + "';"
    ret = db.selectone(sql=sql)
    content=''
    if ret != None:
        author = ret[2]
        bg_time = str(ret[9]).replace('年', '')
        content=ret[3].replace('\n', '')
    conten_list=content.split('。')
    print(conten_list)



if __name__ == '__main__':
    get_poem_about_things("登岳阳楼")
    # test("登岳阳楼")





