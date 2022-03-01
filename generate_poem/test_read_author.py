import pandas as pd

#获取指定文件夹下的excel
import os
def get_filename(path,filetype):  # 输入路径、文件类型例如'.xlsx'
    name = []
    for root,dirs,files in os.walk(path):
        for i in files:
            if os.path.splitext(i)[1]==filetype:
                name.append(i)
    return name            # 输出由有后缀的文件名组成的列表

def read_real_where_name():
    file='data2/gu_jin_lng_lat.xlsx'
    data=pd.read_excel(file)
    gu_name=list(data.gu_name)
    return gu_name

def read_gu_dict():
    file = 'data2/gu_jin_lng_lat.xlsx'
    data = pd.read_excel(file)
    gu_name = list(data.gu_name)
    jin_name=list(data.jin_name)
    lng=list(data.lng)
    lat=list(data.lat)
    gu_dict={}
    for i in range(len(gu_name)):
        gu=gu_name[i]
        gu_dict[gu]={"jin_name":jin_name[i],"lng":lng[i],"lat":lat[i]}
    return gu_dict

def read_where(file,gu_name):
    data=pd.read_excel(file)
    wheres=data.wheres
    real_where=[]
    for i in range(len(wheres)):
        where_name=wheres[i]
        where_list=where_name.split(',')
        for it in where_list:
            if it in gu_name and it!='无':
                real_where.append(it)
    real_where=list(set(real_where))
    for it in real_where:
        jin=gu_dict[it]['jin_name']
        lat=gu_dict[it]['lat']
        lng=gu_dict[it]['lng']
        print(it,jin,lat,lng)

if __name__ == '__main__':
    file = 'author/'
    lists = get_filename(file, '.xlsx')
    gu_name=read_real_where_name()
    gu_dict=read_gu_dict()
    print(gu_name)
    for it in lists:
        newfile = file + it
        print(newfile)
        author=it.split('.')[0]
        print(author)
        read_where(newfile,gu_name)
