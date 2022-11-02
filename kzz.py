import cx_Oracle as ora
import requests
import pandas as pd
from pymongo import MongoClient
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Content-Type': 'application/javascript; charset=UTF-8'
                    'intellpositionL=1079.19px; em_hq_fls=js; em-quote-version=topspeed; intellpositionT=655px; qgqp_b_id=b4f57b496c07d0473e46a74980edfcd2; st_si=06946111717677; st_asi=delete; HAList=a-sz-300585-%u5965%u8054%u7535%u5B50%2Ca-sz-300799-%u5DE6%u6C5F%u79D1%u6280%2Ca-sz-301110-%u9752%u6728%u80A1%u4EFD%2Ca-sz-000839-%u4E2D%u4FE1%u56FD%u5B89%2Ca-sh-600448-%u534E%u7EBA%u80A1%u4EFD%2Ca-sh-600626-%u7533%u8FBE%u80A1%u4EFD%2Ca-sz-301288-N%u6E05%u7814%2Ca-sz-300748-%u91D1%u529B%u6C38%u78C1%2Cty-1-113550-%u5E38%u6C7D%u8F6C%u503A%2Cty-1-113545-%u91D1%u80FD%u8F6C%u503A%2Cty-114-ppm-%u805A%u4E19%u70EF%u4E3B%u529B; st_pvi=62673658268851; st_sp=2021-01-04%2009%3A23%3A33; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=386; st_psi=20220429171537348-113200301201-9735272807'
}


# oracle 版本
def getKzzO():
    url = 'http://74.push2.eastmoney.com/api/qt/clist/get'

    param = {'cb': 'jQuery112406100520667018259_1652761304346',
             'pn': '1',
             'pz': '5000',
             'po': '1',
             'np': '1',
             'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
             'fltt': '2',
             'invt': '2',
             'wbp2u': '|0|0|0|web',
             'fid': 'f243',
             'fs': 'b:MK0354',
             'fields': 'f1,f152,f2,f3,f12,f13,f14,f227,f228,f229,f230,f231,f232,f233,f234,f235,f236,f237,f238,f239,f240,f241,f242,f26,f243',
             '_': '1652761304353'}

    cursor = ora.connect('hzz/hzz@127.0.0.1:1521/orcl').cursor()
    result = requests.get(url, param, headers=headers)
    data = eval(result.text[result.text.index('(') + 1: result.text.index(')')].replace('-', ''))['data']['diff']
    data = [list(map(str, dock.values())) for dock in data]
    cursor.execute('truncate table t_kzz')
    cursor.executemany(
        'insert into t_kzz values(:1,:2,:3,:4,:5,:6,:1,:2,:3,:4,:5,:6,:1,:2,:3,:4,:5,:6,:1,:2,:3,:4,:5,:6,:25)',
        data)
    cursor.execute('commit ')
    print('共计可转债%d' % len(data))
    return [x[3] for x in data]


def getKzz(asc = 'ASC'):
    url = 'http://74.push2.eastmoney.com/api/qt/clist/get'

    param = {'cb': 'jQuery112406100520667018259_1652761304346',
             'pn': '1',
             'pz': '5000',
             'po': '1',
             'np': '1',
             'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
             'fltt': '2',
             'invt': '2',
             'wbp2u': '|0|0|0|web',
             'fid': 'f243',
             'fs': 'b:MK0354',
             'fields': 'f1,f152,f2,f3,f12,f13,f14,f227,f228,f229,f230,f231,f232,f233,f234,f235,f236,f237,f238,f239,f240,f241,f242,f26,f243',
             '_': '1652761304353'}

    result = requests.get(url, param, headers=headers)
    data = eval(result.text[result.text.index('(') + 1: result.text.index(')')])['data']['diff']

    data = [i.values() for i in data]
    df = pd.DataFrame(data,
                      columns=['a', '价格', '涨幅', '代码', '1上0深', '名称', '上市日期', 'b', '纯债价值', '昨日收盘价', '股价', '股票涨幅', 'c',
                               '股票代码', '上深', '股票', '转股价', '转股价值',
                               '转股溢价率', '纯债溢价率', '回售触发价', '强赎触发价', '到期赎回价', '转股日', '申购日期'])
    df['涨幅'] = df[df['涨幅'] != '-']['涨幅']
    df['股票涨幅'] = df[df['股票涨幅'] != '-']['股票涨幅']
    df['差'] = round(df['涨幅'].apply(pd.to_numeric) - df['股票涨幅'].apply(pd.to_numeric),2)
    df.sort_values(by=['差'], ascending=asc=='ASC', inplace=True)
    df.to_csv('kzz.csv',encoding='GBK',index=False)
    print('共计可转债%d' % len(df))

    # csv_file = open('kzz.csv', 'w+', newline='', encoding='GBK')  # 覆盖写
    # writer = csv.writer(csv_file)
    # for dock in data:
    #     writer.writerow(dock.values())
    # print('共计可转债%d' % len(data))

    # reader = csv.reader(open('kzz.csv', 'r', newline='', encoding='GBK'))
    # df = pd.DataFrame(reader,columns=['a','价格','涨幅','代码','1上0深','名称','上市日期','b','纯债价值','昨日收盘价','股价','股票涨幅','c','股票代码','上深','股票','转股价','转股价值',
    #                            '转股溢价率','纯债溢价率','回售触发价','强赎触发价','到期赎回价','转股日','申购日期'])
    #
    # df['差'] = df['涨幅'].apply(pd.to_numeric) - df['股票涨幅'].apply(pd.to_numeric)
    # df.sort_values(by= ['差'] ,ascending= False ,inplace= True)
    # df.to_csv('kzz.csv')


def get1():
    df = pd.read_csv('kzz.csv',encoding='GBK')
    print(df.head(10))
    #print(df.to_dict(orient='rows') )



# 可转债明细
def getKzzDetailOnece(code, type=0, count=5000, beg=None):
    # 数据来自集思录
    # url1 = 'https://www.jisilu.cn/data/cbnew/detail_pic/?display=premium_rt&bond_id='#价格&溢价率
    url = 'https://www.jisilu.cn/data/cbnew/detail_hist/{1}?___jsl=LST___t=1653625077235'  # 30天明细

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Referer': 'https://www.jisilu.cn/data/convert_bond_detail/123085'
    }

    data = eval(requests.get(url.replace('{1}', code['f12']), headers=headers).text)['rows']
    if (len(data) == 0):  #
        print("%s :未上市" % code['f12'])
        return
    if (type != 0):
        return data
    # 因为数据是一个list；因此需要处理为一个json格式的数组
    rows = pandas.DataFrame([x['cell'] for x in data],
                            columns=['bond_id', 'last_chg_dt', 'ytm_rt', 'premium_rt', 'convert_value', 'price',
                                     'volume', 'stock_volume', 'curr_iss_amt', 'cflg', 'amt_change', 'turnover_rt'])
    # mongo从操作
    day = MongoClient().get_database('kzz').get_collection(code['f12'][-6:])
    day.insert_many(rows.to_dict(orient="records"))
    print('%s :ok' % code['f12'][-6:])


def getKzzDetailEveryDay(code, type=0, count=5000, beg=None):
    # 数据来自集思录
    # url1 = 'https://www.jisilu.cn/data/cbnew/detail_pic/?display=premium_rt&bond_id='#价格&溢价率
    url = 'https://www.jisilu.cn/data/cbnew/detail_hist/{1}?___jsl=LST___t=1653625077235'  # 30天明细

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Referer': 'https://www.jisilu.cn/data/convert_bond_detail/123085'
    }
    data = eval(requests.get(url.replace('{1}', code['f12']), headers=headers).text)['rows']
    if (len(data) == 0):  #
        print("%s :未上市" % code['f12'])
        return
    if (type != 0):
        return data
    rows = pandas.DataFrame([x['cell'] for x in data],
                            columns=['bond_id', 'last_chg_dt', 'ytm_rt', 'premium_rt', 'convert_value', 'price',
                                     'volume', 'stock_volume', 'curr_iss_amt', 'cflg', 'amt_change', 'turnover_rt'])

    day = MongoClient().get_database('kzz').get_collection(code['f12'][-6:])
    if day.find_one() != None:
        riqi = day.find().sort('last_chg_dt', -1)[0]['last_chg_dt']
        rows = rows[rows['last_chg_dt'] > riqi]
    if rows.size > 0:
        day.insert_many(rows.to_dict(orient="records"))
    print('%s :ok' % code['f12'][-6:])


if __name__ == '__main__':
    # getGonggao('2022-04-23', etime=datetime.date.today().__str__())
    #getKzz('Desc')
    getKzz()
