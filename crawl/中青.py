# -*- coding: utf-8 -*-
import requests


url='https://focu.youth.cn/article/s?signature=KYJBMEDexQprwO0aJjlOmytGkbZptlBVbQZaj5zbg8RLkP9oXd&uid=7853760&phone_code=e13403df4a29721be6f11cc593680de2&scid=33487936&time=1603782182&app_version=1.7.8&sign=c96917f738d2089f99084a85e4f2bdf1'

#手机端微信
phone_headers = {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255'}
#电脑端微信
pc_headers = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat'}
data = {}
cookies=''
response = requests.get(url, headers=pc_headers, cookies=cookies, data=data,verify=False).text
print(response)