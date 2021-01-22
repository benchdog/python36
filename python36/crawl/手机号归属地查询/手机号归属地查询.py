import json
import time

import requests

with open('phone.txt','r') as fr:
    for line in fr:
        time.sleep(1.5)
        phone = line.strip()
        post_data = {'mobile':phone,'operate':'query'}
        response = requests.post(url='https://tool.lu/mobile/ajax.html',data=post_data)
        # response.encoding=response.apparent_encoding
        # print(response.text)
        dic_attrs = json.loads(response.text)['text']
        # print(phone,dic_attrs['province'],dic_attrs['city'])
        res = phone+'\t'+dic_attrs['province']+'-'+dic_attrs['city']+'\r'
        with open('res.txt','a+') as fw:
            fw.write(res)

        # print("\\u5317\\u4eac".encode('utf-8').decode('unicode_escape'))
        #dic_attrs = json.loads(response.text)['text']