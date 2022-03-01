import pandas as pd
from xlrd import open_workbook
from xlutils.copy import copy

#将分类结果重新写入原excel中
def write_to(file):
    xl =open_workbook(file)
    excel = copy(xl)
    sheet1 = excel.get_sheet(0)

    sheet1.write(0, 2, "wheres")
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
    file = 'author/'
    list = get_filename(file, '.xlsx')
    for it in list:
        newfile = file + it
        write_to(newfile)
