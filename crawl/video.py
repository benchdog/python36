# #-*- coding:UTF-8 -*-
# import requests,re, json, sys
# from bs4 import BeautifulSoup
# from urllib import request
#
# class video_downloader():
#     def __init__(self, url):
#         self.server = 'http://api.xfsub.com'
#         self.api = 'http://api.xfsub.com/xfsub_api/?url='
#         self.get_url_api = 'http://api.xfsub.com/xfsub_api/url.php'
#         self.url = url.split('#')[0]
#         self.target = self.api + self.url
#         self.s = requests.session()
#
#     """
#     函数说明:获取key、time、url等参数
#     Parameters:
#         无
#     Returns:
#         无
#     Modify:
#         2017-09-18
#     """
#     def get_key(self):
#         req = self.s.get(url=self.target)
#         req.encoding = 'utf-8'
#         self.info = json.loads(re.findall('"url.php",\ (.+),', req.text)[0])    #使用正则表达式匹配结果，将匹配的结果存入info变量中
#
#     """
#     函数说明:获取视频地址
#     Parameters:
#         无
#     Returns:
#         video_url - 视频存放地址
#     Modify:
#         2017-09-18
#     """
#     def get_url(self):
#         data = {'time':self.info['time'],
#             'key':self.info['key'],
#             'url':self.info['url'],
#             'type':''}
#         req = self.s.post(url=self.get_url_api,data=data)
#         url = self.server + json.loads(req.text)['url']
#         req = self.s.get(url)
#         bf = BeautifulSoup(req.text,'xml')                                        #因为文件是xml格式的，所以要进行xml解析。
#         video_url = bf.find('file').string                                        #匹配到视频地址
#         return video_url
#
#     """
#     函数说明:回调函数，打印下载进度
#     Parameters:
#         a b c - 返回信息
#     Returns:
#         无
#     Modify:
#         2017-09-18
#     """
#     def Schedule(self, a, b, c):
#         per = 100.0*a*b/c
#         if per > 100 :
#             per = 1
#         sys.stdout.write("  " + "%.2f%% 已经下载的大小:%ld 文件大小:%ld" % (per,a*b,c) + '\r')
#         sys.stdout.flush()
#
#     """
#     函数说明:视频下载
#     Parameters:
#         url - 视频地址
#         filename - 视频名字
#     Returns:
#         无
#     Modify:
#         2017-09-18
#     """
#     def video_download(self, url, filename):
#         request.urlretrieve(url=url,filename=filename,reporthook=self.Schedule)
#
#
# if __name__ == '__main__':
#     url = 'http://www.iqiyi.com/v_19rr7qhfg0.html#vfrm=19-9-0-1'
#     vd = video_downloader(url)
#     filename = '加勒比海盗5'
#     print('%s下载中:' % filename)
#     vd.get_key()
#     video_url = vd.get_url()
#     print('  获取地址成功:%s' % video_url)
#     vd.video_download(video_url, filename+'.mp4')
#     print('\n下载完成！')












from contextlib import closing

# -*- coding:UTF-8 -*-
import json
import requests
import time


class get_photos(object):

    def __init__(self):
        self.photos_id = []
        self.download_server = 'https://unsplash.com/photos/xxx/download?force=trues'
        self.target = 'http://unsplash.com/napi/feeds/home'
        self.headers = {'authorization':'Client-ID c94869b36aa272dd62dfaeefed769d4115fb3189a9d1ec88ed457207747be626'}

    """
    函数说明:获取图片ID
    Parameters:
        无
    Returns:
        无
    Modify:
        2017-09-13
    """
    def get_ids(self):
        req = requests.get(url=self.target, headers=self.headers, verify=False)
        html = json.loads(req.text)
        next_page = html['next_page']
        for each in html['photos']:
            self.photos_id.append(each['id'])
        time.sleep(1)
        for i in range(5):
            req = requests.get(url=next_page, headers=self.headers, verify=False)
            html = json.loads(req.text)
            next_page = html['next_page']
            for each in html['photos']:
                self.photos_id.append(each['id'])
            time.sleep(1)


    """
    函数说明:图片下载
    Parameters:
        无
    Returns:
        无
    Modify:
        2017-09-13
    """
    def download(self, photo_id, filename):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
        target = self.download_server.replace('xxx', photo_id)
        with closing(requests.get(url=target, stream=True, verify = False, headers = self.headers)) as r:
            with open('%d.jpg' % filename, 'ab+') as f:
                for chunk in r.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()

if __name__ == '__main__':
    gp = get_photos()
    print('获取图片连接中:')
    gp.get_ids()
    print('图片下载中:')
    for i in range(len(gp.photos_id)):
        print('  正在下载第%d张图片' % (i+1))
        gp.download(gp.photos_id[i], (i+1))