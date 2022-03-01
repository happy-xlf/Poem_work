import pandas as pd


# 乐 9440       test:1000
# 悲 13784      test:1000
# 忧 3977       test:300
# 思 10550      test:1000
# 喜 6578       test:500
# 怒 2158       test:200
# 惧 493        test:100

def split_data():
    data=pd.read_excel('train.xlsx')
    sentence_list=data.get('sentence')
    label_list=data.get('label')
    emotion = ['悲', '惧', '乐', '怒', '思', '喜', '忧']
    ans={}
    train_senten=[]
    train_label=[]
    test_senten=[]
    test_label=[]
    k1=k2=k3=k4=k5=k6=k7=0
    for i in range(len(sentence_list)):
        lab=label_list[i]
        sente=sentence_list[i]
        if lab in emotion:
            if lab == '悲':
                if k1<=1000:
                    k1+=1
                    test_senten.append(sente)
                    test_label.append(0)
                else:
                    train_label.append(0)
                    train_senten.append(sente)
            elif lab == '惧':
                if k2<=100:
                    k2+=1
                    test_senten.append(sente)
                    test_label.append(1)
                else:
                    train_label.append(1)
                    train_senten.append(sente)
            elif lab == '乐':
                if k3<=1000:
                    k3+=1
                    test_senten.append(sente)
                    test_label.append(2)
                else:
                    train_label.append(2)
                    train_senten.append(sente)
            elif lab == '怒':
                if k4<=200:
                    k4+=1
                    test_senten.append(sente)
                    test_label.append(3)
                else:
                    train_label.append(3)
                    train_senten.append(sente)
            elif lab == '思':
                if k5<=1000:
                    k5+=1
                    test_senten.append(sente)
                    test_label.append(4)
                else:
                    train_label.append(4)
                    train_senten.append(sente)
            elif lab == '喜':
                if k6<=500:
                    k6+=1
                    test_senten.append(sente)
                    test_label.append(5)
                else:
                    train_label.append(5)
                    train_senten.append(sente)
            elif lab == '忧':
                if k7<=300:
                    k7+=1
                    test_senten.append(sente)
                    test_label.append(6)
                else:
                    train_label.append(6)
                    train_senten.append(sente)
    import xlwt

    xl = xlwt.Workbook()
    # 调用对象的add_sheet方法
    sheet1 = xl.add_sheet('sheet1', cell_overwrite_ok=True)

    sheet1.write(0, 0, "sentence")
    sheet1.write(0, 1, 'label')
    for i in range(0, len(test_senten)):
        sheet1.write(i + 1, 0, test_senten[i])
        sheet1.write(i + 1, 1, test_label[i])
    xl.save("data/test.xlsx")

if __name__ == '__main__':
    split_data()