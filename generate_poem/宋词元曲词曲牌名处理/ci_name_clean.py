import pandas as pd

from xlrd import open_workbook
from xlutils.copy import copy
#将分类结果重新写入原excel中
def write_to(data,file):
    print(len(data))
    xl =open_workbook(file)
    excel = copy(xl)
    sheet1 = excel.get_sheet(0)

    sheet1.write(0, 10, "ci_name")
    for i in range(0, len(data)):
        sheet1.write(i + 1, 10, data[i])

    excel.save(file)

def ci_clean(file):
    data=pd.read_excel(file)
    title=data.title
    ci_list=[]
    for it in title:
        t_list=it.split('·')
        if len(t_list)==2:
            ci_list.append(t_list[0])
        else:
            ci_list.append('无')
    write_to(ci_list,file)
    print(ci_list)

if __name__ == '__main__':
    file='../data/song5.xlsx'
    ci_clean(file)