# -*-coding:utf-8-*-
import os
import pickle
import re
import zipfile
import jieba

from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
import pandas as pd

class ImdbDataset(Dataset):
    def __init__(self, train=True):
        # super(ImdbDataset,self).__init__()
        # if not os.path.exists("./data/download"):
        #     unzip_file("./data/test.zip", "./data/download")
        #     unzip_file("./data/train.zip", "./data/download")
        # data_path = r"./data/download"
        # data_path += r"/train" if train else r"/test"
        # self.total_path = []  # 保存所有的文件路径
        # for temp_path in [r"/pos", r"/neg"]:
        #     cur_path = data_path + temp_path
        #     self.total_path += [os.path.join(cur_path, i) for i in os.listdir(cur_path) if i.endswith(".txt")]
        if train == True:
            url = 'data/newtrain.xlsx'
        else:
            url = "data/newtest.xlsx"
        data = pd.read_excel(url)
        sentence = data.get('sentence')
        label = data.get('label')
        #print(sentence)
        #print(label)
        self.sentence_list=sentence
        self.label_list=label



    def __getitem__(self, idx):
        line_text=self.sentence_list[idx]
        # 从txt获取评论并分词
        review = tokenlize(line_text)
        # 获取评论对应的label
        label = int(self.label_list[idx])
        return review, label

    def __len__(self):
        return len(self.sentence_list)


def tokenlize(sentence):
    """
    进行文本分词
    :param sentence: str
    :return: [str,str,str]
    """

    fileters = ['!', '"', '#', '$', '%', '&', '\(', '\)', '\*', '\+', ',', '-', '\.', '/', ':', ';', '<', '=', '>',
                '\?', '@', '\[', '\\', '\]', '^', '_', '`', '\{', '\|', '\}', '~', '\t', '\n', '\x97', '\x96', '”',
                '“', ]
    sentence = re.sub("|".join(fileters), "", sentence)
    sentence=jieba.cut(sentence,cut_all=False)
    sentence=' '.join(sentence)
    result = [i for i in sentence.split(" ") if len(i) > 0]
    result=movestopwords(result)
    return result

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


# 对句子去除停用词
def movestopwords(sentence):
    stopwords = stopwordslist('data/stop_words.txt')  # 这里加载停用词的路径
    outstr = []
    for word in sentence:
        if word not in stopwords:
            if word != '\t' and '\n':
                outstr.append(word)
                # outstr += " "
    return outstr


# 以下为调试代码
def collate_fn(batch):
    """
    对batch数据进行处理
    :param batch: [一个getitem的结果，getitem的结果,getitem的结果]
    :return: 元组
    """
    reviews, labels = zip(*batch)

    return reviews, labels

# def test_file(train=True):
#     if not os.path.exists("./data/download"):
#         unzip_file("./data/data.zip", "./data/download")
#     data_path = r"./data/download"
#     data_path += r"/train" if train else r"/test"
#     total_path = []  # 保存所有的文件路径
#     for temp_path in [r"/pos", r"/neg"]:
#         cur_path = data_path + temp_path
#         total_path += [os.path.join(cur_path, i) for i in os.listdir(cur_path) if i.endswith(".txt")]
#     print(total_path)

if __name__ == "__main__":
    from 情感分析.imdb_sentiment.vocab import Vocab
    imdb_dataset = ImdbDataset(True)
    my_dataloader = DataLoader(imdb_dataset, batch_size=2, shuffle=True, collate_fn=collate_fn)
    for review,label in my_dataloader:
        vocab_model = pickle.load(open("./models/vocab.pkl", "rb"))
        print(review[0])
        result = vocab_model.transform(review[0], 30)
        print(result)
        break

    # unzip_file("./data/a.zip", "./data/download")
    # if os.path.exists("./data/download"):
    #     print("T")

    # data = open("./data/download/train/pos\\10032_10.txt", "r", encoding="utf-8").read()
    # result = tokenlize("--or something like that. Who the hell said that theatre stopped at the orchestra pit--or even at the theatre door?")
    # result = tokenlize(data)
    # print(result)

    # test_file()