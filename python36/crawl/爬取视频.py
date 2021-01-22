import hashlib
import re
import time

import requests


def get_page(url):
    print('GET %s' %url)
    try:
        response=requests.get(url)
        if response.status_code == 200:
            return response.content
    except Exception:
        pass

def parse_index(res):
    obj=re.compile('class="items.*?<a href="(.*?)"',re.S)
    detail_urls=obj.findall(res.decode('gbk'))
    for detail_url in detail_urls:
        if not detail_url.startswith('http'):
            detail_url='http://www.xiaohuar.com'+detail_url
        yield detail_url

def parse_detail(res):
    obj=re.compile('id="media".*?src="(.*?)"',re.S)
    res=obj.findall(res.decode('gbk'))
    if len(res) > 0:
        movie_url=res[0]
        return movie_url


def save(movie_url):
    response=requests.get(movie_url,stream=False)
    if response.status_code == 200:
        m=hashlib.md5()
        m.update(('%s%s.mp4' %(movie_url,time.time())).encode('utf-8'))
        filename=m.hexdigest()
        with open(r'./movies/%s.mp4' %filename,'wb') as f:
            f.write(response.content)
            f.flush()


def main():
    index_url='http://www.xiaohuar.com/list-3-{0}.html'
    for i in range(5):
        print('*'*50,i)
        #爬取主页面
        index_page=get_page(index_url.format(i,))
        #解析主页面,拿到视频所在的地址列表
        detail_urls=parse_index(index_page)
        #循环爬取视频页
        for detail_url in detail_urls:
            #爬取视频页
            detail_page=get_page(detail_url)
            #拿到视频的url
            movie_url=parse_detail(detail_page)
            if movie_url:
                #保存视频
                save(movie_url)


if __name__ == '__main__':
    main()



# 爬取校花网视频