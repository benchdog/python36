#!/usr/bin/env python
# -*-coding:utf-8-*-
import requests
import time
import random

def get_json(url):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }

    params = {
        'page_size': 10,
        # 'next_offset': str(num),
        'tag': '今日热门',
        'platform': 'pc'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        return response.json()
    except BaseException:
        print('request error')
        pass


def get_stream(url, path, type):
    start = time.time()  # 开始时间
    size = 0
    headers = {
        'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, stream=True)  # stream属性必须带上
        chunk_size = 1024  # 每次下载的数据大小
        content_size = int(response.headers['content-length'])  # 总大小
        if response.status_code == 200:
            print('Size：%0.2f MB，Downloading...' % (content_size / chunk_size / 1024))  # 换算单位
            with open(path, type) as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)  # 已下载的文件大小
            return 1
        else:
            print('\033[31mFailed：%s', str(response.status_code))
            return 0
            # todo m3u下载失败后重新下载
    except Exception as e:
        print('\033[31mException：%s', str(e))
        return 0
        # todo m3u下载失败后重新下载



# type = 'wb'
# path='D:/迅雷下载/' + '阳光灿烂的日子.mp4'
url = 'http://mpvideo.qpic.cn/0bf244abcaaal4aa4rkcg5pvbz6dchtqaeia.f10002.mp4?dis_k=c3953fdbe7d5f461a4b6604b6157f904&dis_t=1618886400&vid=wxv_1486071188425654272&format_id=10002'

type = 'ab+'
path='D:/stream/' + '.ts'

if type == 'wb':
    if get_stream(url, path, type):
        print('\033[32mOK')
elif type == 'ab+':
    count = 0
    with open('C:/Users/wf/Desktop/play.m3u8', 'r') as fr:
        for line in fr.readlines():
            if not line.strip().startswith('#'):
                count += 1
                if get_stream(line.strip(), "" + path, type):
                    print('OK：', str(count))
                    # time.sleep(random.random())
        print('\033[32mOK')

'''

'''