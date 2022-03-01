import numpy
import xlwt
import pandas as pd
import re
import jieba

from pyhanlp import *

ans=[]

def read_author():
    file="author3.xlsx"
    data=pd.read_excel(file).fillna("无")
    author=list(data.author)
    experience=list(data.experience)
    for i in range(10):
        text=experience[i]
        p2 = re.compile(r"[（](.*?)[）]", re.S)  # 贪婪匹配
        ans=re.findall(p2, text)
        print(ans)
        print(author[i])
        print("-------")

def jieba_word():
    file = "author3.xlsx"
    data = pd.read_excel(file).fillna("无")
    author = list(data.author)
    experience = list(data.experience)
    for i in range(10):
        text = experience[i]
        kw = jieba.analyse.extract_tags(text, topK=10, withWeight=True, allowPOS=('ns'))
        for item in kw:
            print(item[0])
        print("---------------")

def get_result(arr):
    re_list = []
    ner = ['ns']
    for x in arr:
        temp = x.split("/")
        if len(temp)==2:
            if (temp[1] in ner):
                re_list.append(temp[0])
    return re_list

def pyhnlp_word():
    file = "author3.xlsx"
    data = pd.read_excel(file).fillna("无")
    author = list(data.author)
    experience = list(data.experience)
    for i in range(10):
        text = experience[i]
        analyzer = PerceptronLexicalAnalyzer()
        segs = analyzer.analyze(text)
        arr = str(segs).split(" ")
        result = get_result(arr)
        print(result)
        print("-----------")



if __name__ == '__main__':
    pyhnlp_word()