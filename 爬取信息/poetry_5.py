#提取相关的五言诗词，构成训练集
import pandas as pd
import re

#获取指定文件夹下的excel
import os
def get_filename(path,filetype):  # 输入路径、文件类型例如'.xlsx'
    name = []
    for root,dirs,files in os.walk(path):
        for i in files:
            if os.path.splitext(i)[1]==filetype:
                name.append(i)
    return name            # 输出由有后缀的文件名组成的列表

def read():
    file = 'data/'
    list = get_filename(file, '.xlsx')
    wu_list=[]
    for it in list:
        newfile =file+it
        print(newfile)
        # 获取诗词内容
        data = pd.read_excel(newfile)
        formal=data.formal
        content=data.content
        for i in range(len(formal)):
            fom=formal[i]
            if fom=='五言绝句':
                text=content[i].replace('\n','')
                text_list=re.split('[，。]',text)
                #print(text_list)
                if len(text_list)==9 and len(text_list[len(text_list)-1])==0:
                    f = True
                    for i in range(len(text_list)-1):
                        it=text_list[i]
                        #print(len(it))
                        if len(it)!=5 or it.find('□')!=-1:
                            f=False
                            break
                    if f:
                        #print(text)
                        wu_list.append(text[:24])
                        wu_list.append(text[24:48])
            elif fom=='五言':
                text = content[i].replace('\n', '')
                text_list = re.split('[，。]', text)
                print(text_list)
                if len(text_list[len(text_list)-1])==0:
                    f = True
                    for i in range(len(text_list)-1):
                        it=text_list[i]
                        print(len(it))
                        if len(it)!=5 or it.find('□')!=-1:
                            f=False
                            break
                    if f:
                        #print(text)
                        if len(text_list)==5:
                            wu_list.append(text[:24])
                        elif len(text_list)==13:
                            wu_list.append(text[:24])
                            wu_list.append(text[24:48])
                            wu_list.append(text[48:72])
            elif fom=='七言律诗':
                text = content[i].replace('\n', '')
                text_list = re.split('[，。]', text)
                print(text_list)
                if len(text_list)==17 and len(text_list[len(text_list)-1])==0:
                    f = True
                    for i in range(len(text_list)-1):
                        it=text_list[i]
                        print(len(it))
                        if len(it)!=5 or it.find('□')!=-1:
                            f=False
                            break
                    if f:
                        #print(text)
                        wu_list.append(text[:24])
                        wu_list.append(text[24:48])
                        wu_list.append(text[48:72])
                        wu_list.append(text[72:96])
        print(wu_list)
        return wu_list

def write(content):
    with open("./poem_train/wu_jueju.txt", "w", encoding="utf-8") as f:
        for it in content:
            f.write(it)  # 自带文件关闭功能，不需要再写f.close()
            f.write("\n")


if __name__ == '__main__':
    content=read()
    write(content)