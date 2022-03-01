import requests
import json
import requests
import json


def coords(city):
    # 输入API问号前固定不变的部分
    url = 'https://restapi.amap.com/v3/geocode/geo'

    # 将两个参数放入字典
    params = {'key': '3409090984aea93d6ee622ffa4097165',
              'address': city}
    res = requests.get(url, params)
    jd = json.loads(res.text)
    print(jd)
    if len(jd['geocodes']) != 0:
        coords = jd['geocodes'][0]['location']
        address=jd['geocodes'][0]['formatted_address']
        print(address)
        return coords,address
    else:
        return '无','无'


areas = ['内湖']
for i in areas:
    loca,address = coords(i)
    if loca!='无':
        print(loca)