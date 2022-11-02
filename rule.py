import pandas
import numpy as np
from pymongo import MongoClient


##三叠浪
def sandielang():
    c_all = [0, 0, 0, 0]  # 出现总次数
    # 0.只看收盘价
    c = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
         [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
    # c[0] #第一天上涨次数,2天上涨次数,三天上涨次数
    # 0.只看收盘价
    # 1.低开高走
    # 除了看收盘价，同时开盘价 <  昨日开盘价
    # 2.高开低走
    # 开>昨天；收 < 昨天（隐藏多种情况，如：收盘价>昨天）
    # 3.最高点
    # 最高点高于昨天

    cc = 1  # 无聊的计数器
    day = MongoClient().get_database('day');
    # 获得上证指数的每日涨跌情况
    sh = pandas.DataFrame(day.get_collection('000001').find().sort('dat', -1).limit(500)).sort_values('dat')
    sh = dict(zip(sh['dat'], sh['close']))
    dic = {}

    count = 0  # 计数器，只看三天，1是满足，2是第一天，4是第三天
    for i in day.list_collection_names():
        data = pandas.DataFrame(day.get_collection(i).find().sort('dat', -1).limit(200)).sort_values('dat')
        if len(data) < 3:  # 刨除未上市或者刚上市的
            continue
        row1 = data.iloc[0]
        row2 = data.iloc[1]

        # 单个股票的计数器
        c1_all = [0, 0, 0, 0]
        c1 = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
              [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]

        for j in data.iloc[2:].iterrows():
            d = j[1]

            if count <= 3 and count >= 1:
                try:  # 当日的大盘情况
                    c_all[count] += float(sh[d['dat']]) >= 0 and 1 or 0
                    c1_all[count] += float(sh[d['dat']]) >= 0 and 1 or 0
                except:
                    None

                if float(d['close']) > float(row2['close']):
                    c[0][0][count - 1] += 1  # 只看收盘价
                    c1[0][0][count - 1] += 1  # 只看收盘价
                    try:
                        c[1][0][count - 1] += float(sh[d['dat']]) >= 0 and 1 or 0  # 只看收盘价
                        c1[1][0][count - 1] += float(sh[d['dat']]) >= 0 and 1 or 0  # 只看收盘价
                    except:
                        None
                    if float(d['open']) < float(row2['open']):
                        c[0][1][count - 1] += 1  # 高开低走
                        c1[0][1][count - 1] += 1  # 高开低走
                        try:
                            c[1][1][count - 1] += float(sh[d['dat']]) >= 0 and 1 or 0  # 高开低走
                            c1[1][1][count - 1] += float(sh[d['dat']]) >= 0 and 1 or 0  # 高开低走
                        except:
                            None
                if float(d['high']) > float(row2['high']):
                    c[0][3][count - 1] += 1  # 只看收盘价
                    c1[0][3][count - 1] += 1  # 只看收盘价
                    try:
                        c[1][3][count - 1] += float(sh[d['dat']]) >= 0 and 1 or 0  # 只看收盘价
                        c1[1][3][count - 1] += float(sh[d['dat']]) >= 0 and 1 or 0  # 只看收盘价
                    except:
                        None
                if float(d['close']) < float(row2['close']) and float(d['open']) > float(row2['open']):
                    c[0][2][count - 1] += 1
                    c1[0][2][count - 1] += 1
                    try:
                        c[1][2][count - 1] += float(sh[d['dat']]) >= 0 and 1 or 0
                        c1[1][2][count - 1] += float(sh[d['dat']]) >= 0 and 1 or 0
                    except:
                        None

                count += 1
                if count == 4:
                    count = 0

            else:  # 点亮的话就不再储值
                if (float(d['close']) > float(row2['close']) and float(row2['close']) > float(row1['close'])):
                    count = 1
                    c_all[0] += 1
                    c1_all[0] += 1
            row1 = row2
            row2 = d

        # 求成功率
        temp1 = list(map(lambda x: 0 if c1_all[0] == 0 else round(x * 100 / c1_all[0], 2),
                         np.array(c1[0]).reshape(1, 12)[0].tolist()))
        temp2 = list(np.array(c1[1]).reshape(1, 12)[0].tolist())
        for x in range(12):
            if c1_all[x % 3] == 0:
                temp2[x] = 0
            else:
                temp2[x] = round(temp2[x] * 100 / c1_all[x % 3], 2)

        dic[i] = np.array(c1_all).tolist() + temp1 + temp2
        cc += 1
        if cc % 100 == 0:
            print('-----------------%s--------------' % cc)

    temp1 = list(map(lambda x: round(x * 100 / c_all[0], 2), np.array(c[0]).reshape(1, 12)[0].tolist()))
    temp2 = list(np.array(c[1]).reshape(1, 12)[0].tolist())
    for x in range(12):
        if c_all[x % 3] == 0:
            temp2[x] = 0
        else:
            temp2[x] = round(temp2[x] * 100 / c_all[x % 3], 2)

    dic['000000'] = np.array(c_all).tolist() + temp1 + temp2
    csv = pandas.DataFrame([x for x in dic.values()], index=[x for x in dic.keys()])
    csv.to_csv('sandielang.csv')

    print(dic['000000'])
#上升三部曲
def shangshengsanbuqu():
    day = MongoClient().get_database('day');
    for i in day.list_collection_names():
        if len(data) < 3:  # 刨除未上市或者刚上市的
            continue
        row1 = data.iloc[0]
        row2 = data.iloc[1]

        for j in data.iloc[2:].iterrows():




#长尾线
class ChangWeiXian(object):
    def __init__(self,data):
        self.data = data

    '''
    period 接收数字，代表年数
    
    '''
    def shenglu(self,period = 'y'):



