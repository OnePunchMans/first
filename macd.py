import pandas
import requests



# day.insert_many(d)



def macd(data):
    data = np.array(df.close)
    m, n, T = 12, 26, 9
    EMA1 = np.copy(data)
    EMA2 = np.copy(data)
    f1 = (m - 1) / (m + 1)
    f2 = (n - 1) / (n + 1)
    f3 = (T - 1) / (T + 1)
    for i in range(1, len(data)):
        EMA1[i] = EMA1[i - 1] * f1 + EMA1[i] * (1 - f1)
        EMA2[i] = EMA2[i - 1] * f2 + EMA2[i] * (1 - f2)
    df['ma1'] = EMA1
    df['ma2'] = EMA2
    DIF = EMA1 - EMA2
    df['DIF'] = DIF
    DEA = np.copy(DIF)
    for i in range(1, len(data)):
        DEA[i] = DEA[i - 1] * f3 + DEA[i] * (1 - f3)
    df['DEA'] = DEA

def kdj():
    low_list = df['low'].rolling(window=9).min()
    low_list.fillna(value=df['low'].expanding().min(), inplace=True)
    high_list = df['high'].rolling(window=9).max()
    high_list.fillna(value=df['high'].expanding().max(), inplace=True)

    rsv = (df['close'] - low_list) / (high_list - low_list) * 100
    df['KDJ_K'] = rsv.ewm(com=2).mean()
    df['KDJ_D'] = df['KDJ_K'].ewm(com=2).mean()
    df['KDJ_J'] = 3 * df['KDJ_K'] - 2 * df['KDJ_D']

