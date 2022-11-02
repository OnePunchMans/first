#coding:gbk
import requests
from lxml import etree
import pandas as pd
import json
import re
import sys
import openpyxl
from pymongo import MongoClient

client = MongoClient()
client.drop_database('lianjia')
all = client.lianjia.all
new = client.lianjia.new
new2 = client.lianjia.new2
ten = client.lianjia.ten
fifteen = client.lianjia.fifteen
twenty = client.lianjia.twenty

url = 'https://jn.lianjia.com'
first = '/xiaoqu/'  # 小区首页
##########################################
#1.新发布房子（且低于均价） new.csv
#2.价格低于10%  ten.csv
#3.价格低于15%  fifteen.csv
#4.一个月内新发布的房子 new2.csv

##########################################
flag =0
column = ['县', '街道', '小区', '小区均价', '标题', '链接', '房子总价', '单价','价格比', '建筑面积', '套内面积', '公摊', '楼层', '总高', '年代', '发布天数',
          '电梯', '装修情况', '户型', '抵押情况', '板房/塔楼', '是否满5', '挂牌时间', '上次交易']
data = etree.HTML(requests.get(url + first).text).xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div/a')  # 所有县
for second in data:#遍历所有县
    #跳过历下
    # if flag == 0:
    #     flag = flag + 1
    #     continue;

    xian = second.xpath('string(.)') #县名字
    if (xian not in ['历下','高新']):
        continue
    data2 = etree.HTML(requests.get(url + second.xpath('@href')[0]).text).xpath(
        '/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a')  # 所有街道
    flag2 =0
    for three in data2:#遍历所有街道
        flag2 = flag2 + 1

        jiedao = three.xpath('string(.)')
        #jiedao[three.xpath('string(.)')] = three.xpath('@href')[0]
        data3 = etree.HTML(requests.get(url + three.xpath('@href')[0]).text)  # 所有的小区
        # 判断是否有第二页 begin
        pagedata = json.loads(data3.xpath('/html/body/div[4]/div[1]/div[3]/div[2]/div/@page-data')[0])
        page = pagedata['totalPage'] if pagedata != None and pagedata['totalPage'] > 1 else 1
        for j in range(1, page + 1):
            if (j != 1):  # 不是第一页，查找下一页的url
                data3 = data3 = etree.HTML(requests.get(url + three.xpath('@href')[0]+'/pg'+str(j)).text)  # 所有的小区
            ############判断是否有第二页 end
            for i in range(1, 31):#遍历所有的小区
                if ('0' in data3.xpath('/html/body/div[4]/div[1]/ul/li[' + str(i) + ']/div[2]/div[2]/a/span/text()')):
                    continue
                if (data3.xpath('/html/body/div[4]/div[1]/ul/li[' + str(i) + ']/div[1]/div[1]/a')== []):
                    break
                xiaoqu = etree.HTML(requests.get(data3.xpath('/html/body/div[4]/div[1]/ul/li[' + str(i) + ']/div[1]/div[1]/a/@href')[0]).text)  # 小区页面
                if (len(xiaoqu.xpath('//*[@id="goodSell"]/div/a/@href')) == 0):
                    break
                #小区名:均价
                name = data3.xpath('/html/body/div[4]/div[1]/ul/li[' + str(i) + ']/div[1]/div[1]/a/text()')[0]
                temp =xiaoqu.xpath('/html/body/div[6]/div[2]/div[1]/div/span[1]/text()')[0]
                price = float('0' if temp=='暂无参考均价'  else re.findall( r'\d+' ,temp )[0])
                #是否有在售房子，没有则退出

                fangziList = etree.HTML(requests.get(xiaoqu.xpath('//*[@id="goodSell"]/div/a/@href')[0]).text)
                try:
                    # 判断是否有第二页 begin
                    pagedata = json.loads(fangziList.xpath('//*[@class="page-box house-lst-page-box"]/@page-data')[0])
                    page2 = pagedata['totalPage'] if pagedata != None and pagedata['totalPage'] > 1 else 1
                    for b in range(1 ,page2 + 1):
                        if (b != 1):  # 不是第一页，查找下一页的url
                            er = xiaoqu.xpath('//*[@id="goodSell"]/div/a/@href')[0]
                            fangziList =  etree.HTML(requests.get(er.replace('ershoufang/','ershoufang/pg'+str(b))).text)
                        ############判断是否有第二页 end
                        for x in range(1, 31):
                            if (fangziList.xpath('//*[@id="content"]/div[1]/ul/li[' + str(x) + ']/div[1]/div[1]/a') == []):
                                break
                            jiage = float(fangziList.xpath('//*[@id="content"]/div[1]/ul/li[' + str(x) + ']/div[1]/div[6]/div[1]/span/text()')[0])
                            danjia = float(fangziList.xpath('//*[@id="content"]/div[1]/ul/li[' + str(x) + ']/div[1]/div[6]/div[2]/@data-price')[0])
                            #'2室1厅 | 58.41平米 | 南 北 | 精装 | 中楼层(共6层) | 1990年建 | 板楼'
                            label = fangziList.xpath('//*[@id="content"]/div[1]/ul/li[' + str(x) + ']/div[1]/div[3]/div/text()')[0].split('|')
                            fangName = fangziList.xpath('//*[@id="content"]/div[1]/ul/li[' + str(x) + ']/div[1]/div[1]/a/text()')[0]
                            lianjie = fangziList.xpath('//*[@id="content"]/div[1]/ul/li[' + str(x) + ']/div[1]/div[1]/a/@href')[0]
                            if('车位' in label[0] or '公寓' in fangName):#排除车位和部分公寓
                                continue
                            mianji = label[1].replace('平米','')
                            louceng =label[4].strip()[0] #楼层
                            gaodu = re.findall( r'\d+' ,label[4])[0] #总楼层
                            niandai = re.findall( r'\d+' ,label[5])[0] if len(re.findall( r'\d+' ,label[5]))>0 else  '' #年代

                            tian = fangziList.xpath('//*[@id="content"]/div[1]/ul/li[' + str(x) + ']/div[1]/div[4]/text()')[0].split('/')
                            tian = tian[1] if len(tian) > 1 else ''
                            #row = [xian, jiedao, name, price, jiage, mianji, danjia, louceng, gaodu, niandai, tian,lianjie]

                            #listnew2专用，不要明细
                            #['县','街道','小区','小区均价','房子总价','建筑面积','单价','楼层','总高','年代','发布天数','链接']
                            #[xian,jiedao,name,price,jiage,mianji,danjia,louceng,gaodu,niandai,tian,lianjie]

                            #如果价格低于小区均价10%；进去看明细，否则不搭理
                            fangzi = etree.HTML(requests.get(lianjie).text)
                            zhuzhai = fangzi.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[4]/span[2]/text()')[0]#住宅还是公寓
                            if ('普通住宅'not  in zhuzhai):#再次淘汰公寓
                                continue
                            jianzhu= re.findall( r'\d+' ,fangzi.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[3]/text()')[0])[0]#建筑面积
                            tao = fangzi.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[5]/text()')[0]
                            taonei = 0 if '暂无数据'==tao else re.findall( r'\d+' ,tao)[0]#套内
                            gongtan = 0 if '暂无数据'==tao else round((1 - int(taonei) / int(jianzhu) )*100,2) #公摊
                            huxing = fangzi.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[1]/text()')[0].replace('"','')#户型
                            banta = fangzi.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[6]/text()')[0].replace('"','')#板房/塔楼
                            zhuangxiu = fangzi.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[9]/text()')[0].replace('"','')#装修情况
                            dianti = fangzi.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[12]/text()')[0].replace('"','')#电梯
                            guapai = fangzi.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[1]/span[2]/text()')[0]#挂牌时间
                            shangci = fangzi.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[3]/span[2]/text()')[0]#上次交易
                            nianxian = fangzi.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[5]/span[2]/text()')[0]#年限
                            diya = fangzi.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[7]/span[2]/text()')[0].strip()#抵押
                            #['县', '街道', '小区', '小区均价','链接','房子总价',  '单价','建筑面积', '套内面积','公摊',  '楼层', '总高', '年代', '发布天数','电梯','装修情况','住宅/公寓','抵押情况','板房/塔楼','是否满5','挂牌时间','上次交易' ]
                            try:
                                rate =  round(danjia/price,2)
                            except Exception as e:
                                rate = None
                            row = [xian, jiedao, name, price,fangName,lianjie, jiage,danjia,rate, mianji,taonei,gongtan,  louceng, gaodu, niandai, tian,dianti,zhuangxiu,huxing,diya,banta,nianxian,guapai,shangci ]
                            all.insert_one(dict(zip(column,row)));
                            if danjia < price:
                                if ('天' in tian):
                                    new.insert_one(dict(zip(column,row)));
                                if (danjia <= price * 0.9):
                                    ten.insert_one(dict(zip(column,row)));
                                if (danjia <= price * 0.85):
                                    fifteen.insert_one(dict(zip(column,row)));
                                if (danjia <= price * 0.8):
                                    twenty.insert_one(dict(zip(column, row)));
                            elif ('天' in tian):
                                new2.insert_one(dict(zip(column,row)));
                except Exception as e:
                    print(e)
                #print('--------%s' % name)#完成几个小区

        print('----%s'%jiedao)
        #dfAll = pd.DataFrame(lsAll, columns=column )
    print(xian)
writer = pd.ExcelWriter(r'C:\Users\root\Desktop\BaiduNetdiskWorkspace\jinan.xlsx', engine='openpyxl')
pd.DataFrame(all.find()).to_excel(writer, sheet_name='所有房子', index=False)
pd.DataFrame(new.find()).to_excel(writer, sheet_name='新发布且低于均价', index=False)
pd.DataFrame(ten.find()).to_excel(writer, sheet_name='低于10%', index=False)
pd.DataFrame(fifteen.find()).to_excel(writer, sheet_name='低于15%', index=False)
pd.DataFrame(twenty.find()).to_excel(writer, sheet_name='低于20%', index=False)
pd.DataFrame(new2.find()).to_excel(writer, sheet_name='新发布高于均价', index=False)
writer.close()







