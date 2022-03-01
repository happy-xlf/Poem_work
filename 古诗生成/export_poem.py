from 古诗生成.wu_poem.test_pome import generate_poetry_auto,train_vec,cang
from 古诗生成.qi_poem.test_pome import generate_poetry_auto as qi_generate_poetry_auto,train_vec as qi_train_vec,cang as qi_cang
import torch
import torch.nn as nn
import numpy as np
from gensim.models.word2vec import Word2Vec
import pickle
import os
from 古诗生成.Mymodel import Mymodel


def qi_cang_poem():
    all_data, (w1, word_2_index, index_2_word) = qi_train_vec()
    model_result_file = 'qi_poem/model_lstm.pkl'
    model = pickle.load(open(model_result_file, "rb"))
    qi_cang("风花雪月", model, word_2_index, index_2_word, w1)

def qi_gen_poem():
    all_data, (w1, word_2_index, index_2_word) = qi_train_vec()
    model_result_file = 'qi_poem/model_lstm.pkl'
    model = pickle.load(open(model_result_file, "rb"))
    # qi_cang("风花雪月", model, word_2_index, index_2_word, w1)
    qi_generate_poetry_auto("徐", model, word_2_index, index_2_word, w1)


def wu_cang_poem():
    all_data, (w1, word_2_index, index_2_word) = qi_train_vec()
    model_result_file = 'wu_poem/model_lstm.pkl'
    model = pickle.load(open(model_result_file, "rb"))
    cang("风花雪月", model, word_2_index, index_2_word, w1)


def wu_gen_poem():
    all_data, (w1, word_2_index, index_2_word) = qi_train_vec()
    model_result_file = 'wu_poem/model_lstm.pkl'
    model = pickle.load(open(model_result_file, "rb"))
    # qi_cang("风花雪月", model, word_2_index, index_2_word, w1)
    generate_poetry_auto("徐", model, word_2_index, index_2_word, w1)

if __name__ == '__main__':

   wu_cang_poem()