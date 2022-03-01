import pandas as pd
import requests
import json
def coords(city):
    # 输入API问号前固定不变的部分
    url = 'https://restapi.amap.com/v3/geocode/geo'

    # 将两个参数放入字典
    params = {'key': 'cd0c1ab60e3a22a87009a4196abd94e0',
              'address': city}
    res = requests.get(url, params)
    jd = json.loads(res.text)
    if len(jd['geocodes']) != 0:
        print(jd)
        coords = jd['geocodes'][0]['location']
        address=jd['geocodes'][0]['formatted_address']
        print(address)
        return coords,address
    else:
        return '无','无'

if __name__ == '__main__':
    data=pd.read_excel('gu_where.xlsx')
    gu_name=list(data.gu_where)
    jin_name=list(data.jin_where)
    ans_gu=[]
    ans_jin=[]
    #经度与纬度
    lng=[]
    lat=[]
    for i in  range(6500,len(gu_name)):
        gu=gu_name[i]
        jin=jin_name[i]
        loca, address = coords(gu)
        if loca != '无':
            ans_gu.append(gu)
            ans_jin.append(address)
            loca_list=loca.split(',')
            lng.append(loca_list[0])
            lat.append(loca_list[1])
            print(gu+" "+address+" "+str(loca_list[0])+" "+str(loca_list[1]))
        else:
            loca,address=coords(jin)
            if loca!='无':
                ans_gu.append(gu)
                ans_jin.append(address)
                loca_list = loca.split(',')
                lng.append(loca_list[0])
                lat.append(loca_list[1])
                print(gu+" "+address+" "+str(loca_list[0])+" "+str(loca_list[1]))
    import xlwt

    xl = xlwt.Workbook()
    # 调用对象的add_sheet方法
    sheet1 = xl.add_sheet('sheet1', cell_overwrite_ok=True)

    sheet1.write(0, 0, "gu_name")
    sheet1.write(0,1,"jin_name")
    sheet1.write(0,2,"lng")
    sheet1.write(0,3,"lat")
    for i in range(0, len(ans_jin)):
        sheet1.write(i + 1, 0, ans_gu[i])
        sheet1.write(i + 1, 1, ans_jin[i])
        sheet1.write(i + 1, 2, lng[i])
        sheet1.write(i + 1, 3, lat[i])

    xl.save("gu_jin_lng_lat2.xlsx")
