import pickle
import jieba
import numpy as np
import pandas as pd
import pickle
from keras.engine.saving import load_model
from keras.layers.core import Activation, Dense, SpatialDropout1D
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.preprocessing import sequence
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report



def per_data():
    # 加载分词字典
    with open('model/word_dict.pickle', 'rb') as handle:
        word2index = pickle.load(handle)

    ### 准备数据
    MAX_FEATURES = 80002  # 最大词频数
    MAX_SENTENCE_LENGTH = 110  # 句子最大长度
    num_recs = 0  # 样本数

    with open('small_train.txt', 'r+', encoding="utf-8", errors='ignore') as f:
        lines = f.readlines()
        # 统计样本大小
        for line in lines:
            num_recs += 1

    # 初始化句子数组和label数组
    X = np.empty(num_recs, dtype=list)
    y = np.zeros(num_recs)
    i = 0

    with open('small_train.txt', 'r+', encoding="utf-8", errors='ignore') as f:
        for line in f:
            label, sentence = line.strip("\n").split("\t")
            words = jieba.cut(sentence)
            seqs = []
            for word in words:
                # 在词频中
                if word in word2index:
                    seqs.append(word2index[word])
                else:
                    seqs.append(word2index["UNK"])  # 不在词频内的补为UNK
            X[i] = seqs
            y[i] = int(label)
            i += 1

    # 把句子转换成数字序列，并对句子进行统一长度，长的截断，短的补0
    X = sequence.pad_sequences(X, maxlen=MAX_SENTENCE_LENGTH)
    # 使用pandas对label进行one-hot编码
    y1 = pd.get_dummies(y).values
    print(X.shape)
    print(y1.shape)


if __name__ == '__main__':
    per_data()