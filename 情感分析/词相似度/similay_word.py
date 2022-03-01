from gensim import models
from gensim.models.word2vec import Word2Vec
import os,re


def split_poetry(file='shici.txt'):
    all_data=open(file,"r",encoding="utf-8").read()
    all_data_split=" ".join(all_data)
    with open("split.txt", "w", encoding='utf-8') as f:
        f.write(all_data_split)

def train_vec(split_file='split.txt'):
    #word2vec模型
    vec_params_file= "vec_params.pkl"
    #判断切分文件是否存在，不存在进行切分
    if os.path.exists(split_file)==False:
        split_poetry()
    #读取切分的文件
    split_all_data=open(split_file,"r",encoding="utf-8").read().split("\n")
    #存在模型文件就去加载，返回数据即可
    if os.path.exists(vec_params_file):
        return Word2Vec.load(vec_params_file)
    #词向量大小：vector_size，构造word2vec模型，字维度107，只要出现一次就统计该字，workers=6同时工作
    embedding_num=128
    model=Word2Vec(split_all_data,vector_size=embedding_num,min_count=1,workers=6)
    #保存模型
    model.save(vec_params_file)
    return model

if __name__ == '__main__':
    # split_poetry()
    # model=train_vec()
    # res=model.wv.most_similar('喜',topn=100)
    # print(res)
    model=train_vec()
    emotion=['悲','惧','乐','怒','思','喜','忧']
    em_list={}
    val_list={}
    for e in emotion:
        res = model.wv.most_similar(e, topn=100)
        lists=[]
        v_list=[]
        lists.append(e)
        v_list.append(str(1))
        for item in res:
            print(item[0] + "," + str(item[1]))
            lists.append(item[0])
            v_list.append(str(item[1]))
        em_list[e]=",".join(lists)
        val_list[e]=",".join(v_list)
    import xlwt

    xl = xlwt.Workbook()
    # 调用对象的add_sheet方法
    sheet1 = xl.add_sheet('sheet1', cell_overwrite_ok=True)

    sheet1.write(0, 0, "emotion")
    sheet1.write(0, 1, 'similar')
    sheet1.write(0, 2, 'val')
    i=0
    for k in em_list.keys():
        sheet1.write(i + 1, 0, emotion[i])
        sheet1.write(i + 1, 1, em_list[k])
        sheet1.write(i + 1, 2, val_list[k])
        i+=1

    xl.save("new_emotion.xlsx")
