# -*- coding: utf-8 -*-
import requests


url='https://focu.youth.cn/article/s?signature=3nLo8BVlwPd52WM79oeYgWFloNPvfmvJ68319Ee0q6OyNbJvDX&uid=7853760&phone_code=e13403df4a29721be6f11cc593680de2&scid=33491155&time=1603873529&app_version=1.7.8&sign=0b215ec071ff1f2b5b2c1a053c5d2169'

#手机端微信
headers = {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip, deflate','Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4'}
#电脑端微信
# headers = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat'}
data = {'Hm_lvt_969516094b342230ceaf065c844d82f3':'1603715313','Hm_lvt_916ad8d30af21942f5082a138c9be38f':'1603715314','Hm_lpvt_969516094b342230ceaf065c844d82f3':'1603715457','Hm_lpvt_916ad8d30af21942f5082a138c9be38f':'1603715457','youth_share_article':'601725859d319da17f630cd6f2a0f102'}
cookies={}
# response = requests.get(url, headers=pc_headers, cookies=cookies, data=data,verify=False)
r = requests.get(url, headers=headers, cookies=cookies, data=data)

print(r.status_code)
print(r.cookies)