import urllib.request
import urllib.parse
from lxml import etree
from pyhanlp import *
import pandas as pd

def query(content):
    # 请求地址
    url = 'https://baike.baidu.com/item/' + urllib.parse.quote(content)
    print(url)
    # 请求头部
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    # 利用请求地址和请求头部构造请求对象
    req = urllib.request.Request(url=url, headers=headers, method='GET')
    # 发送请求，获得响应
    response = urllib.request.urlopen(req)
    # 读取响应，获得文本
    text = response.read().decode('utf-8')
    # 构造 _Element 对象
    html = etree.HTML(text)
    # 使用 xpath 匹配数据，得到匹配字符串列表
    #'/html/body/div[3]/div[2]/div/div[1]/div[7]/dl[2]/dd[5]/a'
    #sen_list = html.xpath('//div[contains(@class,"lemma-summary") or contains(@class,"lemmaWgt-lemmaSummary")]//text()')
    f=False
    sen_list=html.xpath('/html/body/div[3]/div[2]/div/div[1]/dl[1]/dd/h2//text()')
    if sen_list==[]:
        sen_list = html.xpath(
            '//div[contains(@class,"lemma-summary") or contains(@class,"lemmaWgt-lemmaSummary")]//text()')
    if sen_list!=[]:
        # 过滤数据，去掉空白
        sen_list_after_filter = [item.strip('\n') for item in sen_list]
        # 将字符串列表连成字符串并返回
        text=''.join(sen_list_after_filter)
        CRFnewSegment = HanLP.newSegment("crf")
        term_list = CRFnewSegment.seg(text)
        ci=['ns']
        where_list=[]
        for it in term_list:
            if str(it.nature) in ci:
                where_list.append(str(it.word))
        if len(where_list)>0:
            print(where_list)
            return where_list[0]
        else:
            return "无"
    else:
        return "无"


from xlrd import open_workbook
from xlutils.copy import copy

#将分类结果重新写入原excel中
def write_to(data,file):
    print(len(data))
    xl =open_workbook(file)
    excel = copy(xl)
    sheet1 = excel.get_sheet(0)

    sheet1.write(0, 1, "jin_where")
    for i in range(0, len(data)):
        sheet1.write(i + 1, 1, data[i])

    excel.save(file)

if __name__ == '__main__':
    jin_list=[]
    data=pd.read_excel('gu_where.xlsx')
    gu_where=data.gu_where
    for i in range(len(gu_where)):
        content=gu_where[i]
        print(content)
        result = query(content)
        print("查询结果：%s" % result)
        jin_list.append(result)
    write_to(jin_list,'gu_where.xlsx')