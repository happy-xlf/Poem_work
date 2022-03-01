import pandas as pd
import re
import jieba

def test(train=False):
    if train == True:
        url = 'data/Train.xlsx'
    else:
        url = "data/test.xlsx"
    data = pd.read_excel(url)
    sentence = data.get('/Doc/Sentence')
    label = data.get('/Doc/Sentence/@label')
    sentence_list=[]
    label_list=[]
    for i in range(len(sentence)):
        if label[i]==1 or label[i]==2:
            sentence_list.append(sentence[i])
            label_list.append(label[i])
    import xlwt

    xl = xlwt.Workbook()
    # 调用对象的add_sheet方法
    sheet1 = xl.add_sheet('sheet1', cell_overwrite_ok=True)

    sheet1.write(0, 0, "sentence")
    sheet1.write(0, 1, 'label')
    for i in range(0, len(sentence_list)):
        sheet1.write(i + 1, 0, sentence_list[i])
        sheet1.write(i + 1, 1, label_list[i])
    xl.save("newtest.xlsx")


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

if __name__ == '__main__':
    # test()
    ans=tokenlize('我很高兴来到@。北京大学！')
    print(ans)