import random

import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup
import numpy as np
import sklearn.linear_model as lm
import sklearn.pipeline as sp
import sklearn.model_selection as ms
import sklearn.metrics as sm
from datetime import datetime
import sklearn.svm as svm
import luna
def getData():
    soup = BeautifulSoup(requests.get('http://datachart.500.com/ssq/history/newinc/history.php?start=00001&end=').text,
                         'html.parser')
    tags = soup.find_all('tr', class_="t_tr1")
    lines = []
    for tag in tags:
        line = []
        for i in tag.find_all('td'):
            line.append(i.text)
        lines.append(line)

    df = pd.DataFrame(lines,columns=['期号','R1','R2','R3','R4','R5','R6','B','SUNDAY','jiangchi','one','oneM','two','twoM','zong','txdate'])
    df.to_csv('cai.csv')



def line():
    df = pd.read_csv('cai.csv')
    df['txdate'] = df['txdate'].str.replace('-', '')
    #定义一个定长数组
    lottery = []
    for i in df.sort_values(by='txdate').to_dict(orient='records'):
        x=[0] *36
        x[0] = i['txdate']
        x[i['R1']] = 1
        x[i['R2']] = 1
        x[i['R3']] = 1
        x[i['R4']] = 1
        x[i['R5']] = 1
        x[i['R6']] = 1
        x[34] = datetime.strptime(x[0],'%Y%m%d').isoweekday()
        tx = luna.Lunar(datetime.strptime(x[0],'%Y%m%d'))
        x[35] = tx
        lottery.append(x)
        print(tx.test())
        break
    lottery = pd.DataFrame(lottery)

    exit()
    print(len(lottery))
    #构建测试集，连续200天数据
    train_x = []
    train_y = []
    for i in range(2750):
        train_x.append(lottery.iloc[i:i+100,1].tolist())
        train_y.append(lottery.iloc[i+101,1])

    #先试试支持向量机（升维）
    model = svm.SVC(kernel='rbf',gamma =0.09527,C=1, class_weight='balanced',probability=True)
    model.fit(train_x,train_y)
    predit_y= model.predict(train_x)
    print(sm.r2_score(train_y,predit_y))

    #试试测试集
    test_x = []
    test_y = []
    for i in range(2751,2805):
        test_x.append(lottery.iloc[i:i + 100, 1].tolist())
        test_y.append(lottery.iloc[i + 101, 1])

    predit_y = model.predict(test_x)
    print(sm.r2_score(test_y, predit_y))
    print(sm.classification_report(test_y, predit_y))
    print (test_y)
    print(predit_y.tolist())
    print(test_y[:10])
    print(model.predict_proba(test_x)[:10])

if __name__ == '__main__':
    line()