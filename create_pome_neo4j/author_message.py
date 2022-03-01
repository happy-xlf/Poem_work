import pandas as pd
import re
def read_author():
    file="author3.xlsx"
    data=pd.read_excel(file).fillna("无")
    produce=list(data.produce)
    i=1
    bg=[]
    ed=[]
    zi=[]
    hao=[]
    pome_self=[]
    #获取诗人诗集数目
    num=list(data.num)

    for it in produce:
        #获取诗人个人简介
        pome_self.append(it)

        print("第"+str(i)+"个诗人：")
        # 获取诗人出生，去世的年份
        datas=re.findall(r"\d+",it)
        if len(datas)!=0 and len(datas)!=1:
            bg.append(datas[0]+"年")
            print("生于"+datas[0])
            flag=False
            for j in range(1,len(datas)):
                if len(datas[j])>=len(datas[0]) and int(datas[j])-int(datas[0])>15:
                    ed.append(datas[j]+"年")
                    print("死于"+datas[j])
                    flag=True
                    break
            if flag==False:
                print("死于:无")
                ed.append("无")
        else:
            print("生于死于:无")
            bg.append("无")
            ed.append("无")

        # 获取诗人，字，号
        ztext=re.findall(r".*字(.*?)[，|。]",it)
        if len(ztext)!=0:
            zi.append(ztext)
        else:
            zi.append("无")
        print(ztext)
        htext = str(re.findall(r".*号(.*?)[，|。]", it)).replace('“','').replace('”','')
        if len(htext)!=0:
            hao.append(htext)
        else:
            hao.append("无")
        print(htext)
        i = i + 1



if __name__ == '__main__':
    read_author()
