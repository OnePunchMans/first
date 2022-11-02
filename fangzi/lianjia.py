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
first = '/xiaoqu/'  # С����ҳ
##########################################
#1.�·������ӣ��ҵ��ھ��ۣ� new.csv
#2.�۸����10%  ten.csv
#3.�۸����15%  fifteen.csv
#4.һ�������·����ķ��� new2.csv

##########################################
flag =0
column = ['��', '�ֵ�', 'С��', 'С������', '����', '����', '�����ܼ�', '����','�۸��', '�������', '�������', '��̯', '¥��', '�ܸ�', '���', '��������',
          '����', 'װ�����', '����', '��Ѻ���', '�巿/��¥', '�Ƿ���5', '����ʱ��', '�ϴν���']
data = etree.HTML(requests.get(url + first).text).xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div/a')  # ������
for second in data:#����������
    #��������
    # if flag == 0:
    #     flag = flag + 1
    #     continue;

    xian = second.xpath('string(.)') #������
    if (xian not in ['����','����']):
        continue
    data2 = etree.HTML(requests.get(url + second.xpath('@href')[0]).text).xpath(
        '/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a')  # ���нֵ�
    flag2 =0
    for three in data2:#�������нֵ�
        flag2 = flag2 + 1

        jiedao = three.xpath('string(.)')
        #jiedao[three.xpath('string(.)')] = three.xpath('@href')[0]
        data3 = etree.HTML(requests.get(url + three.xpath('@href')[0]).text)  # ���е�С��
        # �ж��Ƿ��еڶ�ҳ begin
        pagedata = json.loads(data3.xpath('/html/body/div[4]/div[1]/div[3]/div[2]/div/@page-data')[0])
        page = pagedata['totalPage'] if pagedata != None and pagedata['totalPage'] > 1 else 1
        for j in range(1, page + 1):
            if (j != 1):  # ���ǵ�һҳ��������һҳ��url
                data3 = data3 = etree.HTML(requests.get(url + three.xpath('@href')[0]+'/pg'+str(j)).text)  # ���е�С��
            ############�ж��Ƿ��еڶ�ҳ end
            for i in range(1, 31):#�������е�С��
                if ('0' in data3.xpath('/html/body/div[4]/div[1]/ul/li[' + str(i) + ']/div[2]/div[2]/a/span/text()')):
                    continue
                if (data3.xpath('/html/body/div[4]/div[1]/ul/li[' + str(i) + ']/div[1]/div[1]/a')== []):
                    break
                xiaoqu = etree.HTML(requests.get(data3.xpath('/html/body/div[4]/div[1]/ul/li[' + str(i) + ']/div[1]/div[1]/a/@href')[0]).text)  # С��ҳ��
                if (len(xiaoqu.xpath('//*[@id="goodSell"]/div/a/@href')) == 0):
                    break
                #С����:����
                name = data3.xpath('/html/body/div[4]/div[1]/ul/li[' + str(i) + ']/div[1]/div[1]/a/text()')[0]
                temp =xiaoqu.xpath('/html/body/div[6]/div[2]/div[1]/div/span[1]/text()')[0]
                price = float('0' if temp=='���޲ο�����'  else re.findall( r'\d+' ,temp )[0])
                #�Ƿ������۷��ӣ�û�����˳�

                fangziList = etree.HTML(requests.get(xiaoqu.xpath('//*[@id="goodSell"]/div/a/@href')[0]).text)
                try:
                    # �ж��Ƿ��еڶ�ҳ begin
                    pagedata = json.loads(fangziList.xpath('//*[@class="page-box house-lst-page-box"]/@page-data')[0])
                    page2 = pagedata['totalPage'] if pagedata != None and pagedata['totalPage'] > 1 else 1
                    for b in range(1 ,page2 + 1):
                        if (b != 1):  # ���ǵ�һҳ��������һҳ��url
                            er = xiaoqu.xpath('//*[@id="goodSell"]/div/a/@href')[0]
                            fangziList =  etree.HTML(requests.get(er.replace('ershoufang/','ershoufang/pg'+str(b))).text)
                        ############�ж��Ƿ��еڶ�ҳ end
                        for x in range(1, 31):
                            if (fangziList.xpath('//*[@id="content"]/div[1]/ul/li[' + str(x) + ']/div[1]/div[1]/a') == []):
                                break
                            jiage = float(fangziList.xpath('//*[@id="content"]/div[1]/ul/li[' + str(x) + ']/div[1]/div[6]/div[1]/span/text()')[0])
                            danjia = float(fangziList.xpath('//*[@id="content"]/div[1]/ul/li[' + str(x) + ']/div[1]/div[6]/div[2]/@data-price')[0])
                            #'2��1�� | 58.41ƽ�� | �� �� | ��װ | ��¥��(��6��) | 1990�꽨 | ��¥'
                            label = fangziList.xpath('//*[@id="content"]/div[1]/ul/li[' + str(x) + ']/div[1]/div[3]/div/text()')[0].split('|')
                            fangName = fangziList.xpath('//*[@id="content"]/div[1]/ul/li[' + str(x) + ']/div[1]/div[1]/a/text()')[0]
                            lianjie = fangziList.xpath('//*[@id="content"]/div[1]/ul/li[' + str(x) + ']/div[1]/div[1]/a/@href')[0]
                            if('��λ' in label[0] or '��Ԣ' in fangName):#�ų���λ�Ͳ��ֹ�Ԣ
                                continue
                            mianji = label[1].replace('ƽ��','')
                            louceng =label[4].strip()[0] #¥��
                            gaodu = re.findall( r'\d+' ,label[4])[0] #��¥��
                            niandai = re.findall( r'\d+' ,label[5])[0] if len(re.findall( r'\d+' ,label[5]))>0 else  '' #���

                            tian = fangziList.xpath('//*[@id="content"]/div[1]/ul/li[' + str(x) + ']/div[1]/div[4]/text()')[0].split('/')
                            tian = tian[1] if len(tian) > 1 else ''
                            #row = [xian, jiedao, name, price, jiage, mianji, danjia, louceng, gaodu, niandai, tian,lianjie]

                            #listnew2ר�ã���Ҫ��ϸ
                            #['��','�ֵ�','С��','С������','�����ܼ�','�������','����','¥��','�ܸ�','���','��������','����']
                            #[xian,jiedao,name,price,jiage,mianji,danjia,louceng,gaodu,niandai,tian,lianjie]

                            #����۸����С������10%����ȥ����ϸ�����򲻴���
                            fangzi = etree.HTML(requests.get(lianjie).text)
                            zhuzhai = fangzi.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[4]/span[2]/text()')[0]#סլ���ǹ�Ԣ
                            if ('��ͨסլ'not  in zhuzhai):#�ٴ���̭��Ԣ
                                continue
                            jianzhu= re.findall( r'\d+' ,fangzi.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[3]/text()')[0])[0]#�������
                            tao = fangzi.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[5]/text()')[0]
                            taonei = 0 if '��������'==tao else re.findall( r'\d+' ,tao)[0]#����
                            gongtan = 0 if '��������'==tao else round((1 - int(taonei) / int(jianzhu) )*100,2) #��̯
                            huxing = fangzi.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[1]/text()')[0].replace('"','')#����
                            banta = fangzi.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[6]/text()')[0].replace('"','')#�巿/��¥
                            zhuangxiu = fangzi.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[9]/text()')[0].replace('"','')#װ�����
                            dianti = fangzi.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[12]/text()')[0].replace('"','')#����
                            guapai = fangzi.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[1]/span[2]/text()')[0]#����ʱ��
                            shangci = fangzi.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[3]/span[2]/text()')[0]#�ϴν���
                            nianxian = fangzi.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[5]/span[2]/text()')[0]#����
                            diya = fangzi.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[7]/span[2]/text()')[0].strip()#��Ѻ
                            #['��', '�ֵ�', 'С��', 'С������','����','�����ܼ�',  '����','�������', '�������','��̯',  '¥��', '�ܸ�', '���', '��������','����','װ�����','סլ/��Ԣ','��Ѻ���','�巿/��¥','�Ƿ���5','����ʱ��','�ϴν���' ]
                            try:
                                rate =  round(danjia/price,2)
                            except Exception as e:
                                rate = None
                            row = [xian, jiedao, name, price,fangName,lianjie, jiage,danjia,rate, mianji,taonei,gongtan,  louceng, gaodu, niandai, tian,dianti,zhuangxiu,huxing,diya,banta,nianxian,guapai,shangci ]
                            all.insert_one(dict(zip(column,row)));
                            if danjia < price:
                                if ('��' in tian):
                                    new.insert_one(dict(zip(column,row)));
                                if (danjia <= price * 0.9):
                                    ten.insert_one(dict(zip(column,row)));
                                if (danjia <= price * 0.85):
                                    fifteen.insert_one(dict(zip(column,row)));
                                if (danjia <= price * 0.8):
                                    twenty.insert_one(dict(zip(column, row)));
                            elif ('��' in tian):
                                new2.insert_one(dict(zip(column,row)));
                except Exception as e:
                    print(e)
                #print('--------%s' % name)#��ɼ���С��

        print('----%s'%jiedao)
        #dfAll = pd.DataFrame(lsAll, columns=column )
    print(xian)
writer = pd.ExcelWriter(r'C:\Users\root\Desktop\BaiduNetdiskWorkspace\jinan.xlsx', engine='openpyxl')
pd.DataFrame(all.find()).to_excel(writer, sheet_name='���з���', index=False)
pd.DataFrame(new.find()).to_excel(writer, sheet_name='�·����ҵ��ھ���', index=False)
pd.DataFrame(ten.find()).to_excel(writer, sheet_name='����10%', index=False)
pd.DataFrame(fifteen.find()).to_excel(writer, sheet_name='����15%', index=False)
pd.DataFrame(twenty.find()).to_excel(writer, sheet_name='����20%', index=False)
pd.DataFrame(new2.find()).to_excel(writer, sheet_name='�·������ھ���', index=False)
writer.close()







