import pandas as pd
import xlwt



#读取yuan代的诗词
def read(file):
    data=pd.read_excel(file)
    title=data.title
    # 存储一个曲排名列表
    qu_list=[]
    for it in title:
        if it.find('·')!=-1:
            # 根据诗词名获取对应的曲牌名
            qu=it.split('·')
            qu_list.append(qu[0])
    new_qu=list(set(qu_list))
    #将曲牌名进行保存
    xl = xlwt.Workbook()
    # 调用对象的add_sheet方法
    sheet1 = xl.add_sheet('sheet1', cell_overwrite_ok=True)
    sheet1.write(0, 0, "qu_name")

    for i in range(0, len(new_qu)):
        sheet1.write(i + 1, 0, new_qu[i])

    xl.save("qupai_name.xlsx")





if __name__ == '__main__':
    file='data/yuan.xlsx'
    read(file)