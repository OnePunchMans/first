from sklearn import svm
from pymongo import MongoClient
import  pandas as pd
day=MongoClient().get_database('day')

# 定义SVR预测函数
def svr_predict(tickerlist, strattime_trainX, endtime_trainX, strattime_trainY, endtime_trainY, time_testX):
    #取一支股票数据
    Per_Train_X = pd.DataFrame(day.get_collection('600570').find(projection={'open', 'high','low','close','vol','amount'}))
    Train_X = Per_Train_X

    Train_X = []

    for i in xrange(len(Per_Train_X)):
        Train_X.append(list(Per_Train_X.iloc[i]))

    #拿到开盘价
    Train_label = Per_Train_X.iloc[1:,:][['open']]
    Train_label = list(Train_label['openPrice'])


    # Get test data
if len(Train_X) == len(Train_label):
    Per_Test_X = DataAPI.MktEqudGet(secID=tickerlist, tradeDa
    te = time_testX, field = ['openPrice', 'highestPrice', 'lowestPrice', 'c
                              losePrice','turnoverVol','turnoverValue'],pandas="1")
                              Test_X = []
    for i in xrange(len(Per_Test_X)):
        Test_X.append(list(Per_Test_X.iloc[i]))
    # Fit regression model
    clf = svm.SVR()
    clf.fit(Train_X, Train_label)
    # print clf.fit(Train_X, Train_label)
    PRY = clf.predict(Test_X)
return '%.2f' % PRY[0]
# retunr rount(PRY[0],2)
else:
pass
from CAL.PyCAL import *
from heapq import nsmallest
import pandas as pd

start = '2013-05-01'  # 回测起始时间
end = '2015-10-01'  # 回测结束时间
benchmark = 'HS300'  # 策略参考标准
universe = set_universe('ZZ500')  # + set_universe('SH180') + se
t_universe('HS300')  # 证券池，支持股票和基金
# universe = StockScreener(Factor('LCAP').nsmall(300)) #先用筛选器选择出市值最小的N只股票
capital_base = 1000000  # 起始资金
freq = 'd'  # 策略类型，'d'表示日间
策略使用日线回测，'m'
表示日内策略使用分钟线回测
refresh_rate = 1  # 调仓频率，表示执行hand
le_data的时间间隔，若freq = 'd'
时间间隔的单位为交易日，若freq = 'm'
时间
间隔为分钟
commission = Commission(buycost=0.0008, sellcost=0.0018)  # 佣金万八
cal = Calendar('China.SSE')
stocknum = 50


def initialize(account):  # 初始化虚拟账户状态

    pass


def handle_data(account):  # 每个交易日的买入卖出指令

    global stocknum


# 获得日期
today = Date.fromDateTime(account.current_date).strftime('%Y
                                                         % m % d
') # 当天日期
strattime_trainY = cal.advanceDate(today, '-100B', BizDayConve
ntion.Preceding).strftime('%Y%m%d')
endtime_trainY = time_testX = cal.advanceDate(today, '-1B', Bi
zDayConvention.Preceding).strftime('%Y%m%d')
strattime_trainX = cal.advanceDate(strattime_trainY, '-2B', Bi
zDayConvention.Preceding).strftime('%Y%m%d')
endtime_trainX = cal.advanceDate(endtime_trainY, '-2B', BizDay
Convention.Preceding).strftime('%Y%m%d')
history_start_time = cal.advanceDate(today, '-2B', BizDayConve
ntion.Preceding).strftime('%Y%m%d')
history_end_time = cal.advanceDate(today, '-1B', BizDayConvent
ion.Preceding).strftime('%Y%m%d')
############################################################
###########
# # 获取当日净利润增长率大于1的前N支股票,由于API的读取数量限制，分批运
行API。
# getData_today = pd.DataFrame()
# for i in xrange(300,len(account.universe),300):
# tmp = DataAPI.MktStockFactorsOneDayGet(secID=account.u
niverse[i - 300:i], tradeDate = today, field = ['secID', 'MA5', 'MA10', 'Ne
                                                tProfitGrowRate'],pandas="1")
                                                # getData_today = pd.concat([getData_today,tmp],axis = 0)
                                                # i = (len(account.universe) / 300)*300
                                                # tmp = DataAPI.MktStockFactorsOneDayGet(secID=account.unive
                                                rse[i:], tradeDate = today, field = ['secID', 'NetProfitGrowRate'], pand
as="1")
# getData_today = pd.concat([getData_today,tmp],axis = 0)
# getData_today=getData_today[getData_today.NetProfitGrowRat
e >= 1.0].dropna()

# getData_today=getData_today.sort(columns='NetProfitGrowRat
e
',ascending=False)
# getData_today=getData_today.head(100)
# buylist = list(getData_today['secID'])
############################################################
###########
# 去除流动性差的股票
tv = account.get_attribute_history('turnoverValue', 20)
mtv = {sec: sum(tvs) / 20. for sec, tvs in tv.items()}
per_butylist = [s for s in account.universe if mtv.get(s, 0)
                >= 10 ** 7]
bucket = {}
for stock in per_butylist:
    bucket[stock] = account.referencePrice[stock]
buylist = nsmallest(stocknum, bucket, key=bucket.get)
############################################################
#############
history = pd.DataFrame()
for i in xrange(300, len(account.universe), 300):
    tmp = DataAPI.MktEqudGet(secID=account.universe[i - 300:i]
                             , beginDate=history_start_time, endDate=history_end_time, field=u"s
    ecID, closePrice
    ",pandas="
    1
    ")
    history = pd.concat([history, tmp], axis=0)
    i = (len(account.universe) / 300) * 300
    tmp = DataAPI.MktEqudGet(secID=account.universe[i:], beginDat
    e = history_start_time, endDate = history_end_time, field = u"secID,clos
    ePrice
    ",pandas="
    1
    ")
    history = pd.concat([history, tmp], axis=0)
    # history = account.get_attribute_history('closePrice', 2)
    # history = DataAPI.MktEqudGet(secID=account.universe,beginD
    ate = history_start_time, endDate = history_end_time, field = u"secID,cl
    osePrice
    ",pandas="
    1
    ")
    history.columns = ['secID', 'closePrice']
    keys = list(history['secID'])
    history.set_index('secID', inplace=True)
    ############################################################

    # Sell&止损
    for stock in account.valid_secpos:
        if
    stock in keys:
    PRY = svr_predict(stock, strattime_trainX, endtime_tra
    inX, strattime_trainY, endtime_trainY, time_testX)
    if (PRY < (list(history['closePrice'][stock])[-1]))
            or (((list(history['closePrice'][stock])[-1] / list(history['close
                         Price'][stock])[0])-1) <= -0.05):
                         order_to(stock, 0)
                 # Buy
                 for stock in buylist:
    N = stocknum - len(account.valid_secpos)
    if (stock in keys) and (N > 0):


        if
    stock not in account.valid_secpos:
    PRY = svr_predict(stock, strattime_trainX, end
    time_trainX, strattime_trainY, endtime_trainY, time_testX)
    if (PRY > list(history['closePrice'][stock])[
        -1]):
        amount = (account.cash / N) / account.refere
    ncePrice[stock]
    order(stock, amount)
