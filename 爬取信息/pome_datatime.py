#根据古诗的欣赏和背景来抽取：诗词的具体创作时间

import re
from pyhanlp import *
import pandas as pd
#人名“nr“
#地名“ns”
#机构名“nt”

def demo_CRF_lexical_analyzer(text):
    CRFnewSegment = HanLP.newSegment("crf")
    term_list = CRFnewSegment.seg(text)
    ans=[]
    for it in term_list:
        if str(it.nature)=='t' or str(it.nature)=='m':
            ans.append(str(it.word))
    #print(ans)
    return ans

from xlrd import open_workbook
from xlutils.copy import copy

#将分类结果重新写入原excel中
def write_to(data,file):
    print(len(data))
    xl =open_workbook(file)
    excel = copy(xl)
    sheet1 = excel.get_sheet(0)

    sheet1.write(0, 9, "data")
    for i in range(0, len(data)):
        sheet1.write(i + 1, 9, data[i])

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
    file = 'data/'
    list = get_filename(file, '.xlsx')
    for it in list:
        newfile = file + it
        pome_time = []
        print("开始"+str(newfile))
        data=pd.read_excel(newfile).fillna("无")
        appear=data.appear
        back=data.background
        if len(appear)>5000:
            maxn=5000
        else:
            maxn=len(appear)
        for i in range(maxn):
            print("第"+str(i+1)+"个：")
            app=appear[i]
            bk=back[i]
            if app=="无" and bk =="无":
                pome_time.append("无")
                print("无")
                continue
            #print("===============欣赏===================")
            app_time=demo_CRF_lexical_analyzer(app)
            #print("===============背景===================")
            bk_time=demo_CRF_lexical_analyzer(bk)

            f=False
            for it in bk_time:
                if bool(re.search(r'\d', it))  == True:
                    print(it)
                    pome_time.append(it)
                    f=True
                    break
            if f==False:
                for it in app_time:
                    if bool(re.search(r'\d', it)) == True:
                        print(it)
                        pome_time.append(it)
                        f=True
                        break
            if f==False:
                pome_time.append("无")
                print("无")

        write_to(pome_time,newfile)




