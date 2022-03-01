import numpy
import xlwt
import pandas as pd

ans=[]

def read_author():
    file="author.xlsx"
    data=pd.read_excel(file).fillna("无")
    author=list(data.author)
    all_desty=list(data.desty)
    experience=list(data.experience)

    dict_exp={}
    dict_des={}

    for i in range(len(author)):
        dict_exp[author[i]]=experience[i]
        dict_des[author[i]]=all_desty[i]


    #去重
    author=list(set(author))
    file2="../data/ming.xlsx"
    song=pd.read_excel(file2).fillna("无")
    author_name=list(song.author)
    new_author=list(set(author_name))

    dict={}
    for it in new_author:
        dict[it]=[]

    title=list(song.title)
    appear=list(song.appear)
    back=list(song.background)
    for i in range(len(author_name)):
        name = author_name[i]
        if name=='佚名':
            continue
        content=title[i]+appear[i]+back[i]

        friend=[]
        for j in range(len(author)):
            if content.find(author[j])!=-1 and dict_des[author[j]]=="明代":
                friend.append(author[j])
        #print(name+": "+str(friend))
        dict[name]+=friend
        dict[name]=list(set(dict[name]))
        dict[name]=dict[name]
    print("--------------------ans--------------------------")
    ans_author=[]
    ans_friend=[]
    for it in dict:
        if dict[it]!=[]:
            ans_author.append(it)
            ans_friend.append(','.join(dict[it]))
            print(it+":"+str(dict[it]))



    xl = xlwt.Workbook()
    # 调用对象的add_sheet方法
    sheet1 = xl.add_sheet('sheet1', cell_overwrite_ok=True)

    sheet1.write(0, 0, "author")
    sheet1.write(0, 1, 'friend')


    for i in range(0, len(ans_author)):
        sheet1.write(i + 1, 0, ans_author[i])
        sheet1.write(i + 1, 1, ans_friend[i])

    xl.save("friend_ming.xlsx")






if __name__ == '__main__':
    read_author()