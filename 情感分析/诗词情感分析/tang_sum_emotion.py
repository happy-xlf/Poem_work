from 情感分析.诗词情感分析.utils.mysqlhelper import MySqLHelper
import torch.nn as nn
import torch.nn.functional as F
import torch,pickle,re
import torch,pickle,re
from zhon.hanzi import punctuation

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

train_batch_size = 128
test_batch_size = 128
voc_model = pickle.load(open("./model/vocab.pkl", "rb"))
sequence_max_len = 100



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

#诗词分割
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
    punctuation_str = punctuation
    for i in punctuation_str:
        sentence = sentence.replace(i, '')
    sentence=' '.join(sentence)
    result = [i for i in sentence.split(" ") if len(i) > 0]
    return result


def poem_emotion_predict(line):
    sequence_max_len=100
    model = torch.load('./model/lstm_model.pkl')
    model.to(device())
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
    jsonData=[]
    name=[]
    val=[]
    for key,value in dit.items():
        name.append(key)
        val.append(value)
        #print(key+" "+str(value))
    dit={}
    dit['name']=name
    dit['value']=val
    jsonData.append(dit)
    # print(output.data.max(1, keepdim=True)[0].item())
    pred = output.data.max(1, keepdim=True)[1]  # 获取最大值的位置,[batch_size,1]
    # print(pred.item())
    val=['悲', '惧', '乐', '怒', '思', '喜', '忧']
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
    return val[pred.item()]


#唐：{'喜': 9927, '怒': 8028, '乐': 7963, '思': 6959, '忧': 5262, '悲': 5113, '惧': 5078}
#宋：{'喜': 42555, '怒': 31345, '乐': 30172, '思': 27462, '忧': 23317, '惧': 22896, '悲': 22253}
#元：{'喜': 8691, '乐': 6470, '怒': 6356, '思': 5147, '悲': 4655, '忧': 4010, '惧': 3911}
#明：{'乐': 18412, '悲': 31602, '喜': 13236, '忧': 7731, '思': 22604, '怒': 4633, '惧': 1782}
#清：{'悲': 33947, '怒': 4617, '忧': 6866, '乐': 15513, '思': 19265, '惧': 1359, '喜': 11864}
def get_data():
    db=MySqLHelper()
    sql="select * from ming"
    ret,count=db.selectall(sql=sql)
    ans_content=[]
    for row in ret:
        content=str(row[3]).replace('\n','')
        ans_content.append(content)
    return ans_content

def sum():
    ans_content=get_data()
    ans_sum={}

    for i in range(len(ans_content)):
        print("这是第"+str(i)+"个")
        emotion=str(poem_emotion_predict(ans_content[i]))
        if emotion in ans_sum.keys():
            ans_sum[emotion]=ans_sum[emotion]+1
        else:
            ans_sum[emotion] = 1
    ans_sum=dict(sorted(ans_sum.items(), key=lambda x: x[1], reverse=True))
    print(ans_sum)

if __name__ == '__main__':
    sum()
