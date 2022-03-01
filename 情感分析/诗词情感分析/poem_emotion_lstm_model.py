# -*-coding:utf-8-*-
import pickle

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam
from torch.utils.data import DataLoader
from tqdm import tqdm

from 情感分析.诗词情感分析 import dataset
from 情感分析.诗词情感分析.vocab import Vocab

train_batch_size = 512
test_batch_size = 128
voc_model = pickle.load(open("./model/vocab.pkl", "rb"))
sequence_max_len = 100


def collate_fn(batch):
    """
    对batch数据进行处理
    :param batch: [一个getitem的结果，getitem的结果,getitem的结果]
    :return: 元组
    """
    reviews, labels = zip(*batch)
    reviews = torch.LongTensor([voc_model.transform(i, max_len=sequence_max_len) for i in reviews])
    labels = torch.LongTensor(labels)
    return reviews, labels


def get_dataloader(train=True):
    imdb_dataset = dataset.ImdbDataset(train)
    batch_size = train_batch_size if train else test_batch_size
    return DataLoader(imdb_dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)


class ImdbModel(nn.Module):
    def __init__(self):
        super(ImdbModel, self).__init__()
        self.embedding = nn.Embedding(num_embeddings=len(voc_model), embedding_dim=200, padding_idx=voc_model.PAD).to()
        self.lstm = nn.LSTM(input_size=200, hidden_size=64, num_layers=6, batch_first=True, bidirectional=True,
                            dropout=0.1)
        self.fc1 = nn.Linear(64 * 2, 64)
        self.fc2 = nn.Linear(64, 7)

    def forward(self, input):
        """
        :param input:[batch_size,max_len]
        :return:
        """
        input_embeded = self.embedding(input)  # input embeded :[batch_size,max_len,200]

        output, (h_n, c_n) = self.lstm(input_embeded)  # h_n :[4,batch_size,hidden_size]
        # out :[batch_size,hidden_size*2]
        out = torch.cat([h_n[-1, :, :], h_n[-2, :, :]], dim=-1)  # 拼接正向最后一个输出和反向最后一个输出

        # 进行全连接
        out_fc1 = self.fc1(out)
        # 进行relu
        out_fc1_relu = F.relu(out_fc1)

        # 全连接
        out_fc2 = self.fc2(out_fc1_relu)  # out :[batch_size,2]
        return F.log_softmax(out_fc2, dim=-1)


def device():
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')


def train(imdb_model, epoch):
    """

    :param imdb_model:
    :param epoch:
    :return:
    """
    train_dataloader = get_dataloader(train=True)


    optimizer = Adam(imdb_model.parameters())
    for i in range(epoch):
        bar = tqdm(train_dataloader, total=len(train_dataloader))
        for idx, (data, target) in enumerate(bar):
            optimizer.zero_grad()
            data = data.to(device())
            target = target.to(device())
            output = imdb_model(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            optimizer.step()
            bar.set_description("epcoh:{}  idx:{}   loss:{:.6f}".format(i, idx, loss.item()))
        # if epoch%5==0:
        #     test(imdb_model)
    torch.save(imdb_model, 'model/lstm_model.pkl')


def test(imdb_model):
    """
    验证模型
    :param imdb_model:
    :return:
    """
    test_loss = 0
    correct = 0
    imdb_model.eval()
    test_dataloader = get_dataloader(train=False)
    with torch.no_grad():
        for data, target in tqdm(test_dataloader):
            data = data.to(device())
            target = target.to(device())
            output = imdb_model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()
            pred = output.data.max(1, keepdim=True)[1]  # 获取最大值的位置,[batch_size,1]
            correct += pred.eq(target.data.view_as(pred)).sum()
    test_loss /= len(test_dataloader.dataset)
    print('\nTest set: Avg. loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)\n'.format(
        test_loss, correct, len(test_dataloader.dataset),
        100. * correct / len(test_dataloader.dataset)))


def xlftest():
    import numpy as np
    model = torch.load('model/lstm_model.pkl')
    model.to(device())
    from 情感分析.诗词情感分析.dataset import tokenlize
    #乐，悲，忧，思，喜，怒，惧
    lines=[
           '昔闻洞庭水，今上岳阳楼。吴楚东南坼，乾坤日夜浮。亲朋无一字，老病有孤舟。戎马关山北，凭轩涕泗流。'
           ]
    for line in lines:
        print(line)
        review = tokenlize(line)
        # review=tokenlize(line)
        vocab_model = pickle.load(open("./models/vocab.pkl", "rb"))
        result = vocab_model.transform(review,sequence_max_len)
        # print(result)
        data = torch.LongTensor(result).to(device())
        data=torch.reshape(data,(1,sequence_max_len)).to(device())
        # print(data.shape)
        output = model(data)
        data=output.data.cpu().numpy()
        #['悲', '惧', '乐', '怒', '思', '喜', '忧']
        dit={}
        sum=0
        for i in range(len(data[0])):
            sum+=abs(float(data[0][i]))
            if i==0:
                dit['悲']=abs(float(data[0][i]))
            if i==1:
                dit['惧'] = abs(float(data[0][i]))
            if i==2:
                dit['乐']=abs(float(data[0][i]))
            if i==3:
                dit['怒'] = abs(float(data[0][i]))
            if i==4:
                dit['思']=abs(float(data[0][i]))
            if i==5:
                dit['喜'] =abs(float(data[0][i]))
            if i==6:
                dit['忧']=abs(float(data[0][i]))
        #dit=dict(sorted(dit.items(), key=lambda item: item[1], reverse=True))
        for key,value in dit.items():
            val=round((1-value/sum)*100,2)
            dit[key]=val
        dit = dict(sorted(dit.items(), key=lambda item: item[1], reverse=True))
        for key,value in dit.items():
            print(key+" "+str(value))
        # print(output.data.max(1, keepdim=True)[0].item())
        pred = output.data.max(1, keepdim=True)[1]  # 获取最大值的位置,[batch_size,1]
        # print(pred.item())
        #['悲', '惧', '乐', '怒', '思', '喜', '忧']
        if pred.item() == 0:
            print("悲")
        elif pred.item() == 1:
            print("惧")
        elif pred.item() == 2:
            print("乐")
        elif pred.item() == 3:
            print("怒")
        elif pred.item() == 4:
            print("思")
        elif pred.item() == 5:
            print("喜")
        elif pred.item() == 6:
            print("忧")

if __name__ == '__main__':
    imdb_model = ImdbModel().to(device())
    train(imdb_model,15)
    test(imdb_model)
    # xlftest()
