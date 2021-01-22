import uuid

import requests
from bs4 import BeautifulSoup

response = requests.get(url='http://10.41.77.13/sjmt/login')
# print('编码:',response.apparent_encoding)
# print(response.content) #下载下来的原始内容是字节，需要转换成字符串
response.encoding = 'gbk'  # 若不确定原始什么编码，可用response.encoding=response.apparent_encoding
# print(response.text)
soup = BeautifulSoup(response.text,features='html.parser')  #将html内容转换为对象，features='lxml'是第三方的，需要安装，
# 默认使用python内置的html.parser,lxml比html.parser性能要好，生产环境用

soup_id=soup.find(id="auto-channel-lazyload-article")
# soup_label_li=soup.find('li')  #find(),只找第一个，findall(),找所有的
soup_li_list=soup_id.find_all('li')  #find(),只找第一个，findall(),找所有的,但返回是一个列表对象，而不是soup对象
for li in soup_li_list:
    a = li.find('a')
    if a:
        a_url = 'http:'+ a.attrs.get('href')  # a标签的属性是字典对象，通过get方法获取key为href的value
        print(a_url)
        h3_text = a.find('h3').text  # 获取a标签下h3标签的内容
        print(h3_text)
        img_url = 'http:'+ a.find('img').attrs.get('src') # 获取a标签下img标签的链接
        print(img_url)
        img_response = requests.get(url=img_url)
        img_name = 'E:\\outtest\\' + str(uuid.uuid4()) + '.jpg'
        with open(img_name,'wb') as fw:
            fw.write(img_response.content)  #content是字节类型，视频也是同操作
    # print(type(img_response.text))
    # print(type(img_response.content))