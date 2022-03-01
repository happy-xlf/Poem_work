# coding:utf-8
import re
from pyhanlp import *
import pandas as pd
#人名“nr“
#地名“ns”
#机构名“nt”

import os
#获取文件夹下的所有文件名
def get_filename(path,filetype):  # 输入路径、文件类型例如'.xlsx'
    name = []
    for root,dirs,files in os.walk(path):
        for i in files:
            if os.path.splitext(i)[1]==filetype:
                name.append(i)
    return name            # 输出由有后缀的文件名组成的列表

#添加自定义语料库：作者名，朝代年号
def add_user_dict():
    CustomDictionary = JClass("com.hankcs.hanlp.dictionary.CustomDictionary")
    #添加作者名字
    author_data=pd.read_excel('./data2/author_new.xlsx')
    name=author_data.author
    for it in name:
        CustomDictionary.add(it,"nr")
    #添加时间词
    time=[]
    file = 'data3/'
    lists = get_filename(file, '.xlsx')
    for it in lists:
        newfile = file + it
        dd=pd.read_excel(newfile).year_hao
        time.extend(dd)
    print(time)
    for t in time:
        print(t)
        CustomDictionary.add(t,"t")

#处理作者关键信息：时间，人物，地点，事件
def key_print(lists,text,new_author):
    time = []
    where = []
    author = []
    move=[]
    for it in lists:
        simple = it.split('/')
        if simple[1] == 't':
            time.append(simple[0])
        elif simple[1] == 'nr':
            author.append(simple[0])
        elif simple[1] == 'ns':
            where.append(simple[0])
        elif simple[1] == 'v':
            move.append(simple[0])

    if len(move)!=0 or len(where)!=0:
        newtime=""
        for it in time:
            if bool(re.search(r'\d',it)) and it.find('年')!=-1:
                newtime=it
        if newtime!="":
            print("时间：" + newtime)
            #保存时间
            data_list.append(newtime)
        else:
            if len(data_list)==0:
                data_list.append(time[0])
                print("时间："+time[0])
            else:
                print("时间："+str(data_list[len(data_list)-1]))
                data_list.append(data_list[len(data_list)-1])

        if len(author)!=0:
            author=list(set(author))
            author_list.append(",".join(author))
            print("人物:"+" ".join(author))
        else:
            author_list.append(new_author)
            print("人物:"+new_author)
        if len(where)!=0:
            where_list.append(",".join(where))
            print("地点：" + " ".join(where))
        else:
            where_list.append("无")
            print("地点：无")
        #处理事件
        things=[]
        if len(move)!=0:
            thing_list=re.split('[，。；]+',text)
            for v in move:
                for it in thing_list:
                    if it.find(v)!=-1:
                            things.append(it)
            #去重
            set_things=list(set(things))
            things_list.append(",".join(set_things))
            print("事件：")
            print(set_things)
        else:
            things_list.append("无")
            print("事件：无")
    #事件：动作+人物+地点


#用crf模型提取词性
def demo_CRF_lexical_analyzer(text,new_author):

    global bg_time
    CRFnewSegment = HanLP.newSegment("crf")
    term_list = CRFnewSegment.enableCustomDictionaryForcing(True).seg(text)
    ans=[]
    #'p'介词
    #'ns'地名
    #'t'时间词
    #'nz'其他专名
    #'j'简称略语
    #'m'数词
    #'n'名词
    #至少得有时间词与人物
    f1=False
    f2=False
    lists=['n','nr','v','nz','ns','t']
    tmp=[]
    for it in term_list:
        if str(it.nature) in lists:
            tmp.append(str(it.word)+"/"+str(it.nature))
            if str(it.nature)=='t':
                if bool(re.search(r'\d',it.word)):
                    bg_time=str(it.word)
                    f1 = True
            elif str(it.nature)=='ns':
                f2=True
    if f1:
        print(tmp)
        key_print(tmp,text,new_author)
    else:
        if f2:
            if bg_time!='':
                tmp.append(bg_time+"/t")
            print(tmp)
            key_print(tmp,text,new_author)
import xlwt

#进行诗人个人生平分析
def author_identity(text,author):
    lists = text.split("。")

    for it in lists:
        print(it)
        demo_CRF_lexical_analyzer(it,author)
    print("============分析结果================")
    print(len(data_list))
    for i in range(len(data_list)):
        print(data_list[i], author_list[i], where_list[i], things_list[i])

    print("===========保存数据================")
    xl = xlwt.Workbook()
    # 调用对象的add_sheet方法
    sheet1 = xl.add_sheet('sheet1', cell_overwrite_ok=True)

    sheet1.write(0, 0, "data")
    sheet1.write(0, 1, "author")
    sheet1.write(0, 2, "where")
    sheet1.write(0, 3, "things")
    for i in range(0, len(data_list)):
        sheet1.write(i + 1, 0, data_list[i])
        sheet1.write(i + 1, 1, author_list[i])
        sheet1.write(i + 1, 2, where_list[i])
        sheet1.write(i + 1, 3, things_list[i])

    xl.save("./author2/"+author+".xlsx")

#清洗作者，只要包含个人生平的作者信息
def read_author():
    author_list = pd.read_excel('./data2/author_new.xlsx').fillna('无')
    author_name = author_list.author
    author_experience = author_list.experience
    for i in range(len(author_experience)):
        if author_experience[i]!='无':
            new_author_name.append(author_name[i])
            new_author_experience.append(author_experience[i])


#开始处理
if __name__ == '__main__':
    add_user_dict()
    #提取最终的包含个人经历的作者
    new_author_name = []
    new_author_experience = []
    read_author()
    #输出一共多少个
    print(len(new_author_name))
    for i in range(len(new_author_name)):
        bg_time=""
        print("第"+str(i)+"个")
        author=new_author_name[i]
        text=new_author_experience[i]
        # 时间序列
        data_list = []
        author_list = []
        where_list = []
        things_list = []
        author_identity(text,author)
