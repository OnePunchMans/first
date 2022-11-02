from selenium.webdriver import Chrome360
from time import sleep
import pandas as pd
import datetime
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm
import requests
import csv

from pymongo import MongoClient

url = 'http://8.push2his.eastmoney.com/api/qt/stock/kline/get'
# 日线 和年线的 lmt参数不一样，行数 smplmt 行数
param = {'cb': 'jQuery112403131720271237055_1650959579097',
         'secid': '0.000839',
         'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
         'fields1': 'f1,f2,f3,f4,f5,f6',
         'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
         'klt': '101',
         'fqt': '0',
         'beg': '0',
         'end': '20500101',
         'smplmt': '5000',
         'lmt': '1000000',
         '_': '1650959579149'
         }

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Content-Type': 'application/javascript; charset=UTF-8'
                    'intellpositionL=1079.19px; em_hq_fls=js; em-quote-version=topspeed; intellpositionT=655px; qgqp_b_id=b4f57b496c07d0473e46a74980edfcd2; st_si=06946111717677; st_asi=delete; HAList=a-sz-300585-%u5965%u8054%u7535%u5B50%2Ca-sz-300799-%u5DE6%u6C5F%u79D1%u6280%2Ca-sz-301110-%u9752%u6728%u80A1%u4EFD%2Ca-sz-000839-%u4E2D%u4FE1%u56FD%u5B89%2Ca-sh-600448-%u534E%u7EBA%u80A1%u4EFD%2Ca-sh-600626-%u7533%u8FBE%u80A1%u4EFD%2Ca-sz-301288-N%u6E05%u7814%2Ca-sz-300748-%u91D1%u529B%u6C38%u78C1%2Cty-1-113550-%u5E38%u6C7D%u8F6C%u503A%2Cty-1-113545-%u91D1%u80FD%u8F6C%u503A%2Cty-114-ppm-%u805A%u4E19%u70EF%u4E3B%u529B; st_pvi=62673658268851; st_sp=2021-01-04%2009%3A23%3A33; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=386; st_psi=20220429171537348-113200301201-9735272807'
}


def log(text):
    print('-' * 15)
    print(text)


# decorator
def logging(func):
    def wrapper(*args, **kw):
        print('excute %s():' % func.__name__)
        return func(*args, **kw)

    return wrapper


class Gonggao(object):

    def __init__(self):
        # self.stock_list = stock_list
        self.work_dir = os.path.join(os.getcwd(), str(datetime.date.today()))  # os.getcwd()获取当前路径 + 时间

        if not os.path.isdir(self.work_dir):
            os.mkdir(self.work_dir)

        @logging
        def setOptions(self):
            options = Options()
            options.page_load_strategy = 'normal'
            options.add_experimental_option('prefs', {
                "download.default_directory": self.work_dir,  # 更改默认下载地址
                "download.prompt_for_download": False,  # 自动下载文件
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True  # 不直接在chrome内显示pdf
            })
            return options

        self.driver = Chrome360(chrome_options=setOptions(self))  # webdriver.Chrome(options=set_driver(self))
        self.url = 'http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search&lastPage=index'

    @logging
    def rename(self, file_name, work_dir):
        flag = 0
        while flag == 0:
            try:
                file_list = os.listdir(work_dir)
                file_list.sort(key=lambda fn: os.path.getmtime(work_dir + "\\" + fn))  # 按时间排序
                target_file = file_list[-1]
                old = os.path.join(work_dir, target_file)
                new = os.path.join(work_dir, file_name)
                assert target_file[-3:].lower() == 'pdf'
                flag = 1
                if not os.path.exists(new):
                    log('找到目标文件，开始改名')
                    print('From:' + old)
                    print('To:' + new)
                    os.renames(old, new)
                else:
                    log('文件已存在：' + new)
            except Exception as e:
                print('错误明细是', e.__class__.__name__, e)
                print('错误,等待三秒后重试：可能由于【文件未下载完成】或【文件已存在】导致')
                sleep(3)

    @logging
    def getGongGao(self, stime, etime=datetime.date.today().__str__()):
        self.flag_search = 0
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        zhiya = {}
        ########设置查询时间范围########
        elem = self.driver.find_element(By.CLASS_NAME,
                                        'el-date-editor.el-range-editor.el-input__inner.handle-datepicker.el-date-editor--daterange.el-range-editor--medium')
        elem.click()
        elem.find_elements(By.CLASS_NAME, 'el-range-input')[0].send_keys(stime)
        sleep(1)
        self.driver.find_elements(By.CLASS_NAME, 'el-range-input')[1].clear()
        sleep(1)
        elem.find_elements(By.CLASS_NAME, 'el-range-input')[1].send_keys(etime)
        sleep(1)
        #
        # self.driver.find_elements(By.CLASS_NAME, 'el-range-input')[1].send_keys(etime)
        self.driver.find_element(By.CLASS_NAME, 'el-button.query-btn.el-button--primary').click()  # 点击查询
        sleep(3)

        while self.driver.find_element(By.CLASS_NAME, 'btn-next').get_attribute("disabled") == None:
            results = self.driver.find_elements(By.CLASS_NAME, 'el-table__row')  # 公告
            for row in enumerate(results):
                text = result.find_element(By.CLASS_NAME, 'ahover').text  # 公告标题
                if '质押' in text or '解押' in text:
                    href = row.find_element(By.XPATH, './a').get_attribute('href')
                    print('进入下载页面：' + href)
                    self.driver.get(href)
                    download_icon = self.driver.find_element(By.CLASS_NAME,
                                                             'el-button.el-button--primary.el-button--mini')  # 下载按钮
                    download_icon.click()
                    self.rename(text, self.work_dir)  # 加上股票代码和名字
                    # 把有质押和解质押的股票放入dict
                    zhiya.pop(result.find_element(By.CLASS_NAME, 'code').text,
                              result.find_element(By.CLASS_NAME, 'code.delete-hl').text)
            self.driver.find_element(By.CLASS_NAME, 'btn-next').click()  # 翻页
            sleep(3)

        # 下载文件
        return zhiya

    @logging
    def get_document(self, txdate):

        zhiya = self.getGongGao(self, txdate)
        sleep(1)
        self.driver.quit()
        log('已获取文件：')
        list(map(lambda x: print(x), self.done_list))


def getGonggao(stime, etime=datetime.date.today().__str__()):
    url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '164',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search&lastPage=index',
        'Host': 'www.cninfo.com.cn',
        'Origin': 'http://www.cninfo.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    params = {
        'pageNum': '',
        'pageSize': 30,
        'column': 'szse',
        'tabName': 'fulltext',
        'plate': '',
        'stock': '',
        'searchkey': '',
        'secid': '',
        'category': '',
        'trade': '',
        'seDate': '2022-10-22~2022-04-23',
        'sortName': '',
        'sortType': '',
        'isHLtitle': 'true'
    }
    client = MongoClient()
    db = client.gonggao
    mySet = db.job

    for i in range(1, 500):
        sleep(1)
        params['pageNum'] = i
        params['seDate'] = stime + '~' + etime
        result = requests.post(url, json=params, headers=headers)
        null = ""  # 使用eval的时候要先定义，eval无法解析null
        true = "True"
        if result.status_code == 200 and eval(result.text)['announcements'] == "":
            break

        data = eval(result.text)['announcements']

        for gonggao in data:
            mySet.insert_one(gonggao)


# 日线
def getDay(code, type=0, count=5000, beg=None):
    # 深，创业板 是0. 上证是1.
    param['secid'] = code  # 股票代码
    param['smplmt'] = count
    if (beg):
        param['beg'] = beg
    result = requests.get(url, param, headers=headers)
    data = eval(result.text[result.text.index('(') + 1: result.text.index(')')])['data']['klines']
    if (len(data) == 0):  #
        print("未上市")
        return

    if (type != 0):
        return data

    # 因为数据是一个list；因此需要处理为一个json格式的数组
    rows = pd.DataFrame([i.split(',') for i in data], index=[x[0] for x in [i.split(',') for i in data]],
                        columns=['dat', 'open', 'close', 'high', 'low', 'vol', 'amount', 'amplitude', 'Chg%', 'change',
                                 'rate', ])
    #
    # mongo从操作
    dock_name = '1.000001' if code == '1.000001' else code[-6:]
    day = MongoClient().day[dock_name]
    day.insert_many(rows.to_dict(orient="records"))


# 通过东方财富获取所有的股票实时信息，主要使用股票代码，存在csv里
def getDock():
    csv_file = open('../dock.csv', 'w+', newline='', encoding='GBK')  # 覆盖写
    writer = csv.writer(csv_file)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Referer': 'http://quote.eastmoney.com/center/gridlist.html'
    }
    param = {'cb': 'jQuery112408687766348402066_1650501102436',
             'pn': '1',
             'pz': '10000',
             'po': '1',
             'np': '1',
             'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
             'fltt': '2',
             'invt': '2',
             'fid': 'f3',
             'fs': 'm:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048',
             'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152',
             '_': '1650501102448'}
    # 样例
    url = 'http://59.push2.eastmoney.com/api/qt/clist/get'
    '''{"f1": 2, "f2": 10.8, "f3": 9.98, "f4": 0.98, "f5": 1712485, "f6": 1790640576.0, "f7": 8.04, "f8": 16.8,
     "f9": 153.84, "f10": 0.78, "f11": 0.0, "f12": "600313", "f13": 1, "f14": "农发种业", "f15": 10.8, "f16": 10.01,
     "f17": 10.01, "f18": 9.82, "f20": 11687745560, "f21": 11009488756, "f22": 0.0, "f23": 7.67, "f24": 90.48,
     "f25": 104.55, "f62": 116099850.0, "f115": 212.92, "f128": "-", "f140": "-", "f141": "-", "f136": "-", "f152": 2}'''

    result = requests.get(url, param, headers=headers)
    data = eval(result.text[result.text.index('(') + 1: result.text.index(')')])['data']['diff']
    return data

    data = [i.values() for i in data]
    df = pd.DataFrame(data,
                      columns=['a', '价格', '涨幅', '代码', '1上0深', '名称', '上市日期', 'b', '纯债价值', '昨日收盘价',
                               '股价', '股票涨幅', 'c', '股票代码', '上深', '股票', '转股价', '转股价值', '转股溢价率', '纯债溢价率',
                               '回售触发价', '强赎触发价', '到期赎回价', '转股日', '申购日期'])

    df.to_csv('kzz.csv', encoding='GBK', index=False)
    print('共计股票%d' % len(df))

    for dock in data:
        writer.writerow(dock.values())
    print('共计股票%d' % len(data))
    return data


# 一次性插入
def oneInsert():
    data = getDock()
    data1 = [i['f12'] for i in data]
    do = MongoClient().get_database('day').list_collection_names()
    dock = list(set(data1) ^ set(do))
    dock.append('1.000001')
    num = 1
    for i in data:
        if (i['f12'] in dock):
            print('%s dock:%s' % (num, i['f12']))
            getDay(str(i['f13']) + '.' + str(i['f12']))

            num = num + 1
            sleep(0.01)


def everyDayInsert():
    data = getDock()
    day = MongoClient().get_database('day')
    do = day.list_collection_names()
    riqi = day['1.000001'].find().sort('dat', -1)[0]['dat']
    # 查找上证指数最新日期
    sh = getDay('1.000001', 1, 120)  # 上证指数
    txdate = sh[len(sh) - 1].split(',')[0]

    getDay('1.000001')
    # 数据库已存最新日期
    if (txdate > riqi):  # 存在则增量，不存在则全量
        print("需要更新%s--%s", (riqi, txdate))
        riqi = (datetime.datetime.strptime(riqi, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y%m%d')
        num = 1
        for row in data:
            if (row['f12'] in do):
                print('%d 增量dock:%s' % (num, row['f12']))
                getDay(str(row['f13']) + '.' + str(row['f12']), 0, beg=riqi)
            else:
                print('%s dock:%s' % (num, row['f12']))
                getDay(str(row['f13']) + '.' + str(row['f12']))

            num = num + 1
            sleep(0.01)
        return
    else:
        print("不需要更新")


# 白天更新数据的时候，最后的一条数据收盘价等数据不准确，需要更正的情况，使用；
def updateLast():
    day = MongoClient().get_database('day')
    riqi = day['1.000001'].find().sort('dat', -1)[0]['dat']
    ##1.先删除所有表最新的一天；
    for i in day.list_collection_names():
        day[i].delete_one({'dat': riqi})
    ##2.插入最新的一条
    everyDayInsert();


if __name__ == '__main__':
    # getGonggao(datetime.date.today().__str__(), etime=datetime.date.today().__str__())
    updateLast()
