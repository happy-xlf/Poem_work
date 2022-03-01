#提取七言诗词构成训练集

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
    qi_list=[]
    for it in list:
        newfile =file+it
        print(newfile)
        # 获取诗词内容
        data = pd.read_excel(newfile)
        formal=data.formal
        content=data.content
        for i in range(len(formal)):
            fom=formal[i]
            if fom=='七言绝句':
                text=content[i].replace('\n','')
                text_list=re.split('[，。]',text)
                #print(text_list)
                if len(text_list)==9 and len(text_list[len(text_list)-1])==0:
                    f = True
                    for i in range(len(text_list)-1):
                        it=text_list[i]
                        #print(len(it))
                        if len(it)!=7 or it.find('□')!=-1:
                            f=False
                            break
                    if f:
                        #print(text)
                        qi_list.append(text[:32])
                        qi_list.append(text[32:64])
            elif fom=='七言':
                text = content[i].replace('\n', '')
                text_list = re.split('[，。]', text)
                print(text_list)
                if len(text_list)==5 and len(text_list[len(text_list)-1])==0:
                    f = True
                    for i in range(len(text_list)-1):
                        it=text_list[i]
                        print(len(it))
                        if len(it)!=7 or it.find('□')!=-1:
                            f=False
                            break
                    if f:
                        #print(text)
                        qi_list.append(text[:32])
            elif fom=='七言律诗':
                text = content[i].replace('\n', '')
                text_list = re.split('[，。]', text)
                print(text_list)
                if len(text_list)==17 and len(text_list[len(text_list)-1])==0:
                    f = True
                    for i in range(len(text_list)-1):
                        it=text_list[i]
                        print(len(it))
                        if len(it)!=7 or it.find('□')!=-1:
                            f=False
                            break
                    if f:
                        #print(text)
                        qi_list.append(text[:32])
                        qi_list.append(text[32:64])
                        qi_list.append(text[64:96])
                        qi_list.append(text[96:128])
        print(qi_list)
        return qi_list

def write(content):
    with open("./poem_train/qi_jueju.txt", "w", encoding="utf-8") as f:
        for it in content:
            f.write(it)  # 自带文件关闭功能，不需要再写f.close()
            f.write("\n")


if __name__ == '__main__':
    content=read()
    write(content)