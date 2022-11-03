'''
行业数据分析
用于行业轮动、龙头轮动
'''

import requests as req
#get方式
url ='https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112302366161903067474_1667409740341&pn=1&pz=500&po=1&np=1&fields=f12%2Cf13%2Cf14%2Cf164&fid=f164&fs=m%3A90%2Bt%3A2&ut=b2884a393a59ad64002292a3e90d46a5&_=1667409740345'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Referer': 'http://quote.eastmoney.com/center/gridlist.html'
}

result = req.get(url = url,headers = headers)
#{"f12":"BK0475","f13":90,"f14":"银行","f164":-3894917728.0}
data = eval(result.text[result.text.index('(') + 1: result.text.index(')')])['data']['diff']

cb: jQuery112302366161903067474_1667409740339
fid: f164
po: 1
pz: 50
pn: 2
np: 1
fltt: 2
invt: 2
ut: b2884a393a59ad64002292a3e90d46a5
fs: m:90 t:2
fields: f12,f14,f2,f109,f164,f165,f166,f167,f168,f169,f170,f171,f172,f173,f257,f258,f124,f1,f13


'''{"f1":2,"f2":14798.15,"f12":"BK0428","f13":90,"f14":"电力行业","f109":-2.99,"f124":1667374801,"f164":-3949682848.0,
"f165":-4.67,"f166":-1884099040.0,"f167":-2.23,"f168":-2065583808.0,"f169":-2.44,"f170":125388544.0,"f171":0.15,
"f172":3824294656.0,"f173":4.52,"f257":"华能水电","f258":"600025","f259":1}'''
columns = ['f1']
url2 = 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112302366161903067474_1667409740339&fid=f164&po=1&pz=50&pn=2&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A2&fields=f12%2Cf14%2Cf2%2Cf109%2Cf164%2Cf165%2Cf166%2Cf167%2Cf168%2Cf169%2Cf170%2Cf171%2Cf172%2Cf173%2Cf257%2Cf258%2Cf124%2Cf1%2Cf13'