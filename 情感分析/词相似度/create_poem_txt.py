import pandas as pd

def read_poem():
    data=pd.read_excel('tang.xlsx')
    content=data.get('content')
    ans_content=[]
    for it in content:
        ans_content.append(str(it).replace('\n',''))
    with open("tang.txt", "w",encoding='utf-8') as f:
        for it in ans_content:
            f.write(it)
            f.write('\n')


if __name__ == '__main__':
    read_poem()