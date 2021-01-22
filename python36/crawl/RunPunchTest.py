# -*- coding: utf-8 -*-
import io
import sys
import uuid

import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
post_dict={
    'product':'jsapi','sub_product':'jsapi','v':'2.0','sub_product_v':'2.0','t':'47853013','code':'8000','da_src':'8000','longitude':'114.52208184','latitude':'38.04895831','accuracy':''
}
cookies={
    'BAIDUID':'EEFFF3BE4DE1988293777890CC311026:FG=1','BDORZ':'FFFB88E999055A3F8A630C64834BD6D0','BIDUPSID':'EEFFF3BE4DE19882A87BDA210D15744A','delPer':'0','H_PS_PSSID':'1420_31325_21123_31764_31271_31715_30824_26350_22157','PSINO':'2','PSTM':'1591779410'
}
# response = requests.get(url='http://api.map.baidu.com/images/blank.gif?product=jsapi&sub_product=jsapi&v=2.0&sub_product_v=2.0&t=47853013&code=8000&da_src=8000&longitude=114.52208184&latitude=38.04895831&accuracy=null',data=post_dict)
response = requests.get(url='http://api.map.baidu.com/images/blank.gif',data=post_dict)
# print(response.text)
# cookie_dict = response.cookies.get_dict()
# response.encoding = 'utf8'
# print(response.encoding)
# response.encoding=response.apparent_encoding
# print(response.encoding)
response.encoding = 'gbk'

img_name = 'C:\\Users\\l\\Desktop\\out\\' + str(uuid.uuid4())+ '.gif'
with open(img_name,'wb') as fw:
    # fw.write(response.content)
    fw.write(response.content)
# print(response.headers)
# print(response.text)
print(response.content)
# print('\u77f3\u5bb6\u5e84\u5e02')