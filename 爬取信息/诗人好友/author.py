# -*- coding: utf-8 -*- 
# @Time : 2022/1/1 14:35 
# @Author : xlf
# @File : author.py

import requests
from bs4 import BeautifulSoup
from lxml import etree
import re

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}#创建头部信息
pom_list=[]
k=1
for i in range(1,2010):
    url='https://www.xungushici.com/authors/p-'+str(i)
    r=requests.get(url,headers=headers)
    content=r.content.decode('utf-8')
    soup = BeautifulSoup(content, 'html.parser')

    hed=soup.find('div',class_='col col-sm-12 col-lg-9')
    list=hed.find_all('div',class_="card mt-3")

    origin_url='https://www.xungushici.com'

    for it in list:
        content = {}
        # 1.1获取单页所有诗集
        title = it.find('h4', class_='card-title')
        poemauthor=title.find_all('a')[1].text
        desty=title.find_all('a')[0].text
        #print(poemauthor+"+"+desty)
        #获取诗人图像
        if it.find('a',class_='ml-2 d-none d-md-block')!=None:
            src=it.find('a',class_='ml-2 d-none d-md-block').img['src']
        else:
            src="http://www.huihua8.com/uploads/allimg/20190802kkk01/1531722472-EPucovIBNQ.jpg"
        content['src']=src
        href=title.find_all('a')[1]['href']
        #对应的诗人个人详情页面
        real_href = origin_url + href
        #诗人简介及诗集个数
        text = it.find('p', class_='card-text').text
        #诗人的诗集个数
        numtext = it.find('p', class_='card-text').a.text
        pattern = re.compile(r'\d+')
        num=re.findall(pattern, numtext)[0]

        #进入诗人详情页面
        r2=requests.get(real_href,headers=headers)
        content2=r2.content.decode('utf-8')
        soup2 = BeautifulSoup(content2, 'html.parser')
        ul=soup2.find('ul',class_='nav nav-tabs bg-primary')
        if ul!=None:
            list_li=ul.find_all('li',class_='nav-item')
            exp = ""
            for it in list_li:
                if it.a.text=="人物生平" or it.a.text=="人物" or it.a.text=="生平":
                    urlsp=origin_url+it.a['href']
                    r3 = requests.get(urlsp, headers=headers)
                    content3 = r3.content.decode('utf-8')
                    soup3 = BeautifulSoup(content3, 'html.parser')
                    list_p=soup3.select('body > div.container > div > div.col.col-sm-12.col-lg-9 > div:nth-child(3) > div.card > div')
                    for it in list_p:
                        exp=it.get_text().replace('\n','').replace('\t','').replace('\r','')
            content['author']=poemauthor
            content['produce']=text
            content['num']=num
            content['desty'] = desty
            content['experience'] = exp
            pom_list.append(content)
        else:
            content['author'] = poemauthor
            content['produce'] = text
            content['num'] = num
            content['desty'] = desty
            content['experience'] = "无"
            pom_list.append(content)
        print("第"+str(k)+"个")
        k=k+1

import xlwt

xl = xlwt.Workbook()
# 调用对象的add_sheet方法
sheet1 = xl.add_sheet('sheet1', cell_overwrite_ok=True)

sheet1.write(0,0,"author")
sheet1.write(0,1,'produce')
sheet1.write(0,2,'num')
sheet1.write(0,3,'experience')
sheet1.write(0,4,'src')
sheet1.write(0,5,'desty')

for i in range(0,len(pom_list)):
    sheet1.write(i+1,0,pom_list[i]['author'])
    sheet1.write(i+1, 1, pom_list[i]['produce'])
    sheet1.write(i+1, 2, pom_list[i]['num'])
    sheet1.write(i+1, 3, pom_list[i]['experience'])
    sheet1.write(i + 1, 4, pom_list[i]['src'])
    sheet1.write(i + 1, 5, pom_list[i]['desty'])
xl.save("author3.xlsx")
