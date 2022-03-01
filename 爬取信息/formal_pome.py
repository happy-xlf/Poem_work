#对诗词添加formal：五言，五言绝句，五言律诗，七言，七言绝句，七言律诗

import xlwt
import pandas as pd

#读取源数据，获取诗词内容
def read_excel(file):
    data=pd.read_excel(file)
    content=data.content
    return content

#诗词形式获取
def formal(content):
    formal_list=[]
    for it in content:
        ju_list=str(it).replace('\n','').replace('.','。').split('。')
        print(ju_list)
        if (len(ju_list)-1==8):
            if len(ju_list[0])==11:
                formal_list.append("五言律诗")
                print("五言律诗")
            elif len(ju_list[0])==15:
                formal_list.append("七言律诗")
                print("七言律诗")
            else:
                formal_list.append("无")
                print("无")
        elif len(ju_list)-1==4:
            if len(ju_list[0])==11:
                formal_list.append("五言绝句")
                print("五言绝句")
            elif len(ju_list[0])==15:
                formal_list.append("七言绝句")
                print("七言绝句")
            else:
                formal_list.append("无")
                print("无")
        else:
            if len(ju_list[0])==11:
                formal_list.append("五言")
                print("五言")
            elif len(ju_list[0]) == 15:
                formal_list.append("七言")
                print("七言")
            else:
                formal_list.append("无")
                print("无")
    return formal_list

from xlrd import open_workbook
from xlutils.copy import copy
#将分类结果重新写入原excel中
def write_to(data,file):
    print(len(data))
    xl =open_workbook(file)
    excel = copy(xl)
    sheet1 = excel.get_sheet(0)

    sheet1.write(0, 8, "formal")
    for i in range(0, len(data)):
        sheet1.write(i + 1, 8, data[i])

    excel.save(file)

#获取指定文件夹下的excel
import os
def get_filename(path,filetype):  # 输入路径、文件类型例如'.xlsx'
    name = []
    for root,dirs,files in os.walk(path):
        for i in files:
            if os.path.splitext(i)[1]==filetype:
                name.append(i)
    return name            # 输出由有后缀的文件名组成的列表


if __name__ == '__main__':
    #获取指定文件夹下的源数据
    file='data/'
    list=get_filename(file,'.xlsx')
    for it in list:
        newfile=file+it
        #获取诗词内容
        data=read_excel(newfile)
        #根据诗词内容，获取对应的诗词形式
        formal_data=formal(data)
        #将诗词形式重新写入源数据
        write_to(formal_data,newfile)

