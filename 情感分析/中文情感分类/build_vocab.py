# -*-coding:utf-8-*-
import pickle

from tqdm import tqdm

from 情感分析.中文情感分类 import dataset
# from 情感分析.imdb_sentiment.vocab import Vocab
from torch.utils.data import DataLoader

class Vocab:
    UNK_TAG = "<UNK>"  # 表示未知字符
    PAD_TAG = "<PAD>"  # 填充符
    PAD = 0
    UNK = 1

    def __init__(self):
        self.dict = {  # 保存词语和对应的数字
            self.UNK_TAG: self.UNK,
            self.PAD_TAG: self.PAD
        }
        self.count = {}  # 统计词频的

    def fit(self, sentence):
        """
        接受句子，统计词频
        :param sentence:[str,str,str]
        :return:None
        """
        for word in sentence:
            self.count[word] = self.count.get(word, 0) + 1  # 所有的句子fit之后，self.count就有了所有词语的词频

    def build_vocab(self, min_count=1, max_count=None, max_features=None):
        """
        根据条件构造 词典
        :param min_count:最小词频
        :param max_count: 最大词频
        :param max_features: 最大词语数
        :return:
        """
        if min_count is not None:
            self.count = {word: count for word, count in self.count.items() if count >= min_count}
        if max_count is not None:
            self.count = {word: count for word, count in self.count.items() if count <= max_count}
        if max_features is not None:
            # [(k,v),(k,v)....] --->{k:v,k:v}
            self.count = dict(sorted(self.count.items(), lambda x: x[-1], reverse=True)[:max_features])

        for word in self.count:
            self.dict[word] = len(self.dict)  # 每次word对应一个数字

        # 把dict进行翻转
        self.inverse_dict = dict(zip(self.dict.values(), self.dict.keys()))

    def transform(self, sentence, max_len=None):
        """
        把句子转化为数字序列
        :param sentence:[str,str,str]
        :return: [int,int,int]
        """
        if len(sentence) > max_len:
            sentence = sentence[:max_len]
        else:
            sentence = sentence + [self.PAD_TAG] * (max_len - len(sentence))  # 填充PAD

        return [self.dict.get(i, 1) for i in sentence]

    def inverse_transform(self, incides):
        """
        把数字序列转化为字符
        :param incides: [int,int,int]
        :return: [str,str,str]
        """
        return [self.inverse_dict.get(i, "<UNK>") for i in incides]

    def __len__(self):
        return len(self.dict)

def collate_fn(batch):
    """
    对batch数据进行处理
    :param batch: [一个getitem的结果，getitem的结果,getitem的结果]
    :return: 元组
    """
    reviews, labels = zip(*batch)

    return reviews, labels



def get_dataloader(train=True):
    imdb_dataset = dataset.ImdbDataset(train)
    my_dataloader = DataLoader(imdb_dataset, batch_size=200, shuffle=True, collate_fn=collate_fn)
    return my_dataloader


if __name__ == '__main__':

    # sentences = [["今天", "天气", "很", "好"],
    #              ["今天", "去", "吃", "什么"]]
    # ws = Vocab()
    # for sentence in sentences:
    #     # 统计词频
    #     ws.fit(sentence)
    # # 构造词典
    # ws.build_vocab(min_count=1)
    # print(ws.dict)
    # # 把句子转换成数字序列
    # ret = ws.transform(["好", "好", "好", "好", "好", "好", "好", "热", "呀"], max_len=13)
    # print(ret)
    # # 把数字序列转换成句子
    # ret = ws.inverse_transform(ret)
    # print(ret)
    # pass


    ws = Vocab()
    dl_train = get_dataloader(True)
    dl_test = get_dataloader(False)
    for reviews, label in tqdm(dl_train, total=len(dl_train)):
        for sentence in reviews:
            ws.fit(sentence)
    for reviews, label in tqdm(dl_test, total=len(dl_test)):
        for sentence in reviews:
            ws.fit(sentence)
    ws.build_vocab()
    print(len(ws))

    pickle.dump(ws, open("./models/vocab.pkl", "wb"))
