import pandas as pd
import xlwt


#获取指定文件夹下的excel
import os
def get_filename(path,filetype):  # 输入路径、文件类型例如'.xlsx'
    name = []
    for root,dirs,files in os.walk(path):
        for i in files:
            if os.path.splitext(i)[1]==filetype:
                name.append(i)
    return name            # 输出由有后缀的文件名组成的列表

#将分类结果重新写入原excel中
def write_to(data):
    import  xlwt

    xl = xlwt.Workbook()
    # 调用对象的add_sheet方法
    sheet1 = xl.add_sheet('sheet1', cell_overwrite_ok=True)

    sheet1.write(0, 0, "gu_where")

    for i in range(0, len(data)):
        sheet1.write(i + 1, 0, data[i])

    xl.save("gu_where.xlsx")

if __name__ == '__main__':
    file = 'author2/'
    lists = get_filename(file, '.xlsx')
    where_list = []
    for it in lists:
        newfile = file + it
        data=pd.read_excel(newfile)
        where_name=list(data.wheres)
        for it in where_name:
            it_list=it.split(',')
            for k in it_list:
                where_list.append(k)
    where_list=list(set(where_list))
    print(len(where_list))
    print(where_list)
    write_to(where_list)





