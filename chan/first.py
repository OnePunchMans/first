from Score import Score
from gonggao import getDock
import numpy as np

class S0001(Score):


    #返回9*7矩阵，
    def isAgree(self, row):
        open = float(row['open'])
        close = float(row['close'])
        high = float(row['high'])
        low = float(row['low'])
        mat = np.zeros((9,7),dtype = int)

        '''
        定义2个条件(借鉴箱体图);q1>0.9(close > 0.9);q2>0.5(open > 0.5)
        振幅必须大于3
        收盘必须翻红>1
        '''
        if (close > open and close > (0.9 * high + 0.1 * low) and open >= (high + low) / 2 and
                float(row['Chg%']) > 1  and float(row['amplitude']) > 3):
            mat[0:int(float(row['Chg%'])),0:int(float(row['amplitude']))-2] = 1
            return (True,mat)
        else:
            return False,None

    def getBuy(self):
        for dock in (self.db.list_collection_names()):
            row = self.db.get_collection(dock).find().sort('dat', -1).limit(1);
            if self.isAgree(row):
                print(dock)

    def getBuyTime(self):
        for dock in getDock():
            '''{'f1': 2, 'f2': 14.95, 'f3': 0.54, 'f4': 0.08, 'f5': 13440, 'f6': 20089348.45, 'f7': 3.5, 'f8': 0.46, 'f9': 649.75, 'f10': 0.56, 'f11': 0.13, 
            'f12': '300536', 'f13': 0, 'f14': '农尚环境', 'f15': 15.18, 'f16': 14.66, 'f17': 15.13, 'f18': 14.87, 'f20': 4384657588, 'f21': 4384068663, 'f22': 0.13, 
            'f23': 7.16, 'f24': 0.27, 'f25': -30.79, 'f62': 1766242.0, 'f115': 2005.99, 'f128': '-', 'f140': '-', 'f141': '-', 'f136': '-', 'f152': 2}'''
            try:
                open = float(dock['f17'])
                close = float(dock['f2'])
                high = float(dock['f15'])
                low = float(dock['f16'])


                if (close > open and close > (0.9 * high + 0.1 * low) and open >= (high + low) / 2 and
                        float(dock['f3']) > 2 and float(dock['f7']) > 4):
                    print(dock['f14'],dock['f3'],dock['f7'])
                else:
                    pass
            except:
                pass
if __name__ == '__main__':
    #print(S0001().probability())
    S0001().getBuyTime()

