# -*- coding: utf-8 -*-
import random
import time

import requests
from bs4 import BeautifulSoup
# from fdfs_client.client import Fdfs_client,get_tracker_conf
# import pymysql
from elasticsearch6 import Elasticsearch

# print('\u8266')

# 解决Python3下打印 utf-8 字符串出现 UnicodeEncodeError 错误
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 关闭无SSL认证的警告
requests.packages.urllib3.disable_warnings()


poster_storage = 'F:\\films\\poster\\'
torrent_storage = 'F:\\films\\torrent\\'
# es = Elasticsearch(['13.32.4.172:9201'])
es = Elasticsearch(['127.0.0.1:9200'])

env = 'sj'
if env == 'alp':
    # 公司研发环境
    fdfs_server = 'http://192.168.23.113:/'
    fdfs_conf = 'F:\\Codes\\Python\\alphasta\\conf\\fdfs_client_alp.conf'
    mysql_host = '192.168.23.113'
    # es = Elasticsearch(['192.168.23.116:9200', '192.168.23.117:9200'])
elif env == 'sj':
    # 市局环境
    mysql_host = '13.32.4.170'
    fdfs_server = 'http://13.32.4.170:/'
    fdfs_conf = 'F:\\Codes\\Python\\alphasta\\conf\\fdfs_client_sj.conf'
    # es = Elasticsearch(['13.32.4.169:9200', '13.32.4.170:9200', '13.32.4.171:9200'])

userAgent = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Wind    ows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"]

'''
# 建立FastDFS连接，存入海报和种子
def fdfs_upload(content,suffix):
    tracker_conf = get_tracker_conf(fdfs_conf)  # 绝对路径
    fdfs_client = Fdfs_client(tracker_conf)
    try:
        upload_status = fdfs_client.upload_by_buffer(content, suffix)
        if upload_status.get('Status') == "Upload successed.":
            # print('fdfs上传成功')
            return bytes.decode(upload_status.get('Remote file_id'))
        else:
            print('fdfs上传失败')
    except Exception as e:
        print('fdfs上传异常' + '：' + str(e))
'''
#海报和种子存入本地文件系统
def local_upload(type,content,path):
    try:
        with open(path, 'wb') as fw:
            fw.write(content)
            # print(type + ' ok')
    except Exception as e:
        print(type + ' error:', str(e))

CBK = '3a92d243ea2dd7780ad5bba129cafdf5b' + str(time.time()).replace('.','_')

# www.415.net
# http://647.net
# http://www.7btjia.com/
headers = {"Connection":"close",'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}
cookies = {}
# cookies = {'bbs_sid': '1b13b2dcd679fd08', 'bbs_page': '1',
#            'bbs_auth': 'klNQP7uYal3tg708DYugb9sAL3wS9gaRO9nGilKJV9KXjCnfM6bhpOM6dsZVvopR2gvWeuDYPfCx%252BJg432ED%25252Fg%253D%253D',
#            'bbs_lastonlineupdate': '1595251915', 'bbs_lastday': '1595237713', 'cck_lasttime': '1595237714048',
#            'cck_count':'0', 'timeoffset': '%2B08'}
# cookies = 'bbs_sid=1b13b2dcd679fd08; bbs_page=1; bbs_auth=klNQP7uYal3tg708DYugb9sAL3wS9gaRO9nGilKJV9KXjCnfM6bhpOM6dsZVvopR2gvWeuDYPfCx%252BJg432ED%25252Fg%253D%253D; bbs_lastonlineupdate=1595251915; bbs_lastday=1595237713; cck_lasttime=1595237714048; cck_count=0; timeoffset=%2B08Cookie'
data = {}
payload = {}
for page in range(1,790):
    url = 'http://www.7btjia.com/forum-index-fid-1-page-' + str(page) + '.htm'
    # url = 'http://www.3btjia.com/forum-index-fid-1-page-2.htm'
    try:
        cur_page = url.split('-')[-1].split('.')[0]
        print('最新电影页：', cur_page)
        response = requests.get(url, headers=headers, cookies=cookies, data=data, params=payload,verify=False).text.replace('\u25b6','').replace('\u25c0','')
        soup = BeautifulSoup(response, features='lxml')
        # print(soup.prettify())
        # print(soup.title.string)
        # print(soup.select('td[class="subject"]'))
        #最新电影标签http://www.3btjia.com/forum-index-fid-1.htm中取出所有电影
        # for film in soup.find_all('a', class_="subject_link thread-new"):
        for film in soup.find_all('a', class_="subject_link"):
            # print(film.attrs['href'])
            # print(film.text) #string
            # print(film.contents) #list

            # torrent_storage_path = '' # 种子存储fastdfs路径
            # poster_storage_path = ''  # 海报存储fastdfs路径

            film_url = film.attrs['href']
            # film_url = 'http://www.3btjia.com/thread-index-fid-1-tid-43871.htm'
            if film_url in ['http://www.3btjia.com/thread-index-fid-6-tid-7.htm', 'http://www.3btjia.com/thread-index-fid-1-tid-6.htm', 'http://www.3btjia.com/thread-index-fid-1-tid-12848.htm']:
                continue
            # 请求每部电影的链接
            try:
                print('电影 ', film_url)
                film_response = requests.get(film_url, headers=headers, cookies=cookies, data=data, params=payload,verify=False).text
                film_soup = BeautifulSoup(film_response, features='lxml').find('td', class_="post_td")
                # print(film_soup.prettify())

                # 电影id
                film_id = film_url.split('-')[-1].split('.')[0]
                # print(film_id)
                # print(type(film_id))
                # 电影名字和电影属性(年代、产地、类型)
                film_info = film_soup.find('h2').text.strip().replace('\t', '').split('\n')
                if film_info and len(film_info) >= 2:
                    film_name = film_info[1].strip()
                    film_attr = film_info[0].strip()
                else:
                    print('此电影链接不可用')
                    continue


                # 电影详细介绍(导演、主演、类型、剧情介绍等)
                film_desc = ''
                for p in film_soup.find_all('p')[:-1]:
                    # print('p：',p.text.replace('\xa0', ''))
                    film_desc = film_desc + p.text.replace('\xa0', '').replace('\b','').replace('\000','').replace('\u25c0','').replace('\ubabb','').replace('\ub9d0','') + '<br>'

                # 入库时间
                intime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                # print(film_id,film_name,film_attr)
                # print('电影描述：', film_desc)
                # 存储film_id、film_name、film_attr、film_desc到MySQL or ES

                # 电影海报、电影种子保存到FastDFS or 本地路径，路径映射到MySQL：poster_path、torrent_path
                # 电影海报(第一张是海报，剩余是电影截图)
                # print('海报 start')
                film_posters_list = film_soup.select('img')
                for poster_counter in range(len(film_posters_list)):
                    film_poster_url = film_posters_list[poster_counter]['src']
                    # print('海报URL：', film_poster_url)
                    if not film_poster_url.endswith('torrent.gif'):
                        try:
                            film_poster_response = requests.get(film_poster_url, headers=headers,verify=False).content

                            #海报存入fastdfs
                            # upload_res = fdfs_upload(film_poster_response,'jpg')
                            # poster_storage_path = poster_storage_path + ',' + fdfs_server + upload_res

                            #海报存入本地
                            poster_storage_path = poster_storage + film_id + '_' + str(poster_counter) + '.jpg'
                            local_upload('海报',film_poster_response,poster_storage_path)
                        except Exception as e:
                            print('请求单张海报异常：' + film_poster_url + '：' + str(e))
                            continue
                # poster_storage_path = poster_storage_path.strip(',')
                print('海报 ok')

                '''                 
                    # 下载图片
                    fdfs_download_res = fdfs_client.download_to_file('', file_id)
                    print(fdfs_download_res)
                    # 删除图片 注:file_id为bytes类型
                    file_id = fdfs_upload_res['Remote file_id']
                    fdfs_delete_res = fdfs_client.delete_file(file_id)
                    print(fdfs_delete_res)
                '''

                # 电影种子
                # print('种子 start')
                torrent_counter = 0
                for film_torrent_ajax in film_soup.find_all('a', class_="ajaxdialog"):
                    film_torrent_ajax_url = film_torrent_ajax['href']
                    # print(film_torrent_ajax_url)
                    try:
                        film_torrent_ajax_response = requests.get(film_torrent_ajax_url, headers=headers,verify=False).text.encode('utf-8').decode('unicode_escape')
                        # print(type(film_torrent_ajax_response))
                        film_torrent_ajax_soup = BeautifulSoup(film_torrent_ajax_response, features='lxml')
                        # 获取电影种子名称，保存到本地时才需要此变量
                        # film_torrent_name = film_torrent_ajax_soup.find('dd').text.replace('\n', '').replace('\t', '')
                        # 获取电影种子下载链接
                        film_torrent_url = film_torrent_ajax_soup.find('a', target='_blank').attrs['href'].replace('\\', '')
                        # print(film_torrent_url)
                        # 下载、保存电影种子
                        try:
                            # print(film_torrent_url)
                            # print(film_torrent_storage)
                            # response.text是string类型，response.content是字节bytes类型，此处用字节类型
                            film_torrent_url_response = requests.get(film_torrent_url, headers=headers).content
                            # print('5')

                            # 存入fastdfs
                            # upload_res = fdfs_upload(film_torrent_url_response, 'torrent')
                            # torrent_storage_path = torrent_storage_path + ',' + fdfs_server + upload_res

                            # 存入本地
                            torrent_storage_path = torrent_storage + film_id + '_' + str(torrent_counter) + '.torrent'
                            local_upload('种子', film_torrent_url_response, torrent_storage_path)
                            torrent_counter += 1
                        except Exception as e:
                            print('请求种子异常：' + film_torrent_url + '：' + str(e))
                            continue
                    except Exception as e:
                        print('请求torrent Ajax异常：' + film_torrent_ajax_url + '：' + str(e))
                        continue
                # torrent_storage_path = torrent_storage_path.strip(',')
                # print(torrent_fdfs_path)
                print('种子 ok')

                # print('film_id',film_id)
                # print('film_name',film_name)
                # print('film_attr',film_attr)
                # print('film_desc',film_desc)
                # print('poster_fdfs_path',poster_fdfs_path)
                # print('torrent_fdfs_path',torrent_fdfs_path)

                '''
                # 结构化字段存入MySQL
                conn = pymysql.connect(
                    host=mysql_host,
                    port=3306,
                    user='alpview',
                    password='123456',
                    db='test',
                    charset='utf8'
                )
                cursor = conn.cursor()
                sql = """INSERT INTO film_info (film_id,film_name, film_attr, film_desc, torrent_path, poster_path) VALUES (%s, %s, %s, %s, %s, %s) on duplicate key update intime=CURRENT_TIMESTAMP()"""
                try:
                    print('插入MySQL ing')
                    cursor.execute(sql, [film_id, film_name, film_attr, film_desc, torrent_storage_path, poster_storage_path])
                    # print("提交MySQL")
                    conn.commit()
                    print('插入MySQL ok')
                except Exception as e:
                    print("插入MySQL异常:" + film_id, film_name, film_attr, film_desc, poster_storage_path,
                          torrent_storage_path + '\n' + str(e))
                    conn.rollback()
                    # print('插入MySQL异常222')
                finally:
                    conn.close()
                    # print('关闭MySQL连接')
                '''
                # 结构化字段存入ES
                film_body = {'film_name':film_name,'film_attr':film_attr,'film_desc':film_desc, 'intime':intime}
                es_res = es.index(index='films', doc_type='basic_info', id=film_id,body=film_body)
                print('ES ', es_res['result'])

            except Exception as e:
                print('电影异常 ' + film_id, film_name, film_attr, film_desc, intime + '\n' + str(e))
                continue
            finally:
                time.sleep(random.random())
                # exit()
    except Exception as e:
        print('最新电影页异常 ', str(e))


    '''
CREATE TABLE `film_info` (
`film_id`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`film_name`  varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`film_attr`  varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`film_desc`  text CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`torrent_path`  text CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`poster_path`  text CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`intime`  timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
PRIMARY KEY (`film_id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
ROW_FORMAT=COMPACT
;
    '''