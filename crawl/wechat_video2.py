#!/usr/bin/env python
# -*-coding:utf-8-*-
import requests
import time
import random
import threading


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




type = 'wb'
path='D:/迅雷下载/' + '1.mp4'
url = 'http://mpvideo.qpic.cn/0bf24yeu2aajwqalgp4ndrpvtzwdjxtastia.f10003.mp4?dis_k=cd5430691504bc5762d1e183831028bd&dis_t=1618469455&vid=wxv_1559595028379926529&format_id=10003'
path2='D:/迅雷下载/' + '2.mp4'
url2 = 'http://mpvideo.qpic.cn/0bf2uyaneaaaeqaf7kcq6bpvbjwd2ktabuqa.f10002.mp4?dis_k=fd8e1e921da4b8570e3e50249cdea51e&dis_t=1618469583&vid=wxv_1501935899885027330&format_id=10002'


# type = 'ab+'
# path='D:/stream/' + '.ts'

threads = []
if type == 'wb':
    # if get_stream(url, path, type):
    #     print('\033[32mOK')
    t1 = threading.Thread(target=get_stream, args=[url, path, type])
    threads.append(t1)
    t2 = threading.Thread(target=get_stream, args=[url2, path2, type])
    threads.append(t2)
elif type == 'ab+':
    count = 0
    with open('C:/Users/wf/Desktop/play2.m3u8', 'r') as fr:
        for line in fr.readlines():
            if not line.strip().startswith('#'):
                count += 1
                if get_stream(line.strip(), "" + path, type):
                    print('OK：', str(count))
                    # time.sleep(random.random())
        print('\033[32mOK')

for t in threads:
    t.setDaemon(True)
    t.start()

for t in threads:
    t.join()

print('done')