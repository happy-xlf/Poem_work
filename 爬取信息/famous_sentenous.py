import requests
from bs4 import BeautifulSoup
from lxml import etree

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}#创建头部信息
ans_sent=[]
ans_author=[]
ans_poem=[]
for i in range(1,136):
    url='https://www.xungushici.com/mingjus/p'+str(i)
    print("正在爬取第"+str(i)+"页！！！")
    r=requests.get(url,headers=headers)
    content=r.content.decode('utf-8')
    soup = BeautifulSoup(content, 'html.parser')

    sentenous_list=soup.find_all('li',class_="list-group-item d-flex justify-content-between align-items-center border-bottom spinner-border-sm")
    for it in sentenous_list:
        a_list=it.find_all('a')
        sent=a_list[0].text
        ju=a_list[1].text.split(" ")
        author=ju[0]
        poem_name=str(ju[1]).replace("《",'').replace("》",'')
        ans_sent.append(sent)
        ans_author.append(author)
        ans_poem.append(poem_name)

import xlwt

xl = xlwt.Workbook()
# 调用对象的add_sheet方法
sheet1 = xl.add_sheet('sheet1', cell_overwrite_ok=True)

sheet1.write(0,0,"sent")
sheet1.write(0,1,'author')
sheet1.write(0,2,'poem_name')
for i in range(0,len(ans_sent)):
    sheet1.write(i+1,0,ans_sent[i])
    sheet1.write(i+1,1,ans_author[i])
    sheet1.write(i + 1, 2, ans_poem[i])

xl.save("famous_sentenous.xlsx")


