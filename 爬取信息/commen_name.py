import requests
from bs4 import BeautifulSoup
from lxml import etree

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}#创建头部信息

hc=[]

url='https://www.xungushici.com/authors'
r=requests.get(url,headers=headers)
content=r.content.decode('utf-8')
soup = BeautifulSoup(content, 'html.parser')
orign_href='https://www.xungushici.com'


hecheng=soup.find('div',id='divHeCheng')
list=hecheng.find_all('li',class_="m-1 badge badge-light")
dic={}
for i in range(1,len(list)):
    href=orign_href+list[i].a['href']
    hecehng=list[i].a.text
    hc.append(hecehng)
    r2 = requests.get(href, headers=headers)
    content2 = r2.content.decode('utf-8')
    soup2 = BeautifulSoup(content2, 'html.parser')
    pomdiv=soup2.find('div',class_='col col-sm-12 col-lg-9')
    card=pomdiv.find_all('div',class_='card mt-3')
    author_list=[]
    for it in card:
        h4=it.find('h4',class_='card-title')
        list_a=h4.find_all('a')
        desty=list_a[0].text
        author=list_a[1].text
        author_list.append(author)
    dic[hecehng]=",".join(author_list)

import xlwt

xl = xlwt.Workbook()
# 调用对象的add_sheet方法
sheet1 = xl.add_sheet('sheet1', cell_overwrite_ok=True)

sheet1.write(0,0,"hc")
sheet1.write(0,1,'author')
for i in range(0,len(hc)):
    sheet1.write(i+1,0,hc[i])
    sheet1.write(i+1,1,dic[hc[i]])

xl.save("common_name.xlsx")


for it in hc:
    print(it+": "+dic[it])

