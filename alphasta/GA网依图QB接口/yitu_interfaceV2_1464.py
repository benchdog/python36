# -*- coding: utf-8 -*-

import requests
import json
import time
import urllib3
import base64
import cx_Oracle

db = cx_Oracle.connect('LIGH', '123456', '10.25.199.221:1521/orcl')
cursor = db.cursor()

url = 'http://10.25.199.180:9501/face/v1/framework/log/fetch'
pic_url_prefix = 'http://10.25.199.180:11180/business/api/storage/image?uri_base64='
# 后文所有请求（除登录）的 HTTP Header 或 Cookies 中应包含以下字段：
session_id = '749494496@cpu_cluster2'
# 如果在 Cookies 中加上 session_id 仍然不能使用，则在 Cookies 中额外加上以下字段:
yt_cluster_id = session_id.split('@')[1]
# 域名称：表示这个请求所发送的集群(如果空表示本集群)
target_cluster_id = 'cpu_cluster2'
headers = {'session_id':session_id, 'yt_cluster_id':yt_cluster_id, 'target_cluster_id':target_cluster_id}

# response = requests.get(url + 'repository', headers = headers)
# print(response.text)

# "id":"11","name":"一代","face_image_num":7376033,"creator_id":3,"create_time":1507485838,"permission_map":{"0":1,"102":1,"502":1,"601":1,"602":1,"603":1,"604":1,"605":1}
# "id":"13","name":"二代","face_image_num":9754641,"creator_id":3,"create_time":1507521839,"permission_map":{"0":1,"102":1,"502":1,"601":1,"602":1,"603":1,"604":1,"605":1}
# "id":"599","name":"车驾管","face_image_num":13895586,"creator_id":3,"create_time":1537234362,"permission_map":{"0":1,"102":1,"502":1,"601":1,"602":1,"603":1,"604":1,"605":1}

repository_dict = {11:'一代', 13:'二代', 599:'车驾管',1464:'全国在逃'}
repository_id = 1464
offset = 76000
limit = 1525
count_err = 0

while 1:
    data_list = []
    time.sleep(2)
    params_str = {'repository': repository_id, 'offset': offset, 'limit': limit}
    response_dict = json.loads(requests.post(url , headers = headers, data = json.dumps(params_str)).text)
    if response_dict['rtn'] == 0:
        for row in range(len(response_dict['results'])):
            if 'face_image_id' in response_dict['results'][row].keys() and 'face_image_uri' in response_dict['results'][row]['content'].keys() and 'person_id' in response_dict['results'][row]['content'].keys() and 'name' in response_dict['results'][row]['content'].keys():
                face_image_id = response_dict['results'][row]['face_image_id']
                face_image_uri = pic_url_prefix + str(base64.b64encode(response_dict['results'][row]['content']['face_image_uri'].encode('utf8')), encoding='utf8')
                person_id = response_dict['results'][row]['content']['person_id']
                name = response_dict['results'][row]['content']['name']

                # print(face_image_uri,person_id,name)
                data_list.append((face_image_id, face_image_uri, person_id, name))

            else:
                count_err += 1
                print('数据格式错误，' + str(count_err))


        if len(data_list) > 0:
            try:
                # res = cursor.execute('select * from LIGH.YITU')
                # print(res)
                cursor.prepare('insert into LIGH.YITU1464 (image_id, image_url, person_id, uname) values (:1, :2, :3, :4)')
                cursor.executemany(None, data_list)
                db.commit()
                print(str(repository_dict[repository_id]) + '已插入' + str(response_dict['next_offset']) + '条')
            except Exception as e:
                print(e, '<' + str(response_dict['next_offset']) + '>')
            finally:
                if offset < int(response_dict['next_offset']):
                    offset = int(response_dict['next_offset'])
                else:
                    break
                    print(str(repository_dict[repository_id]) + '<' + str(repository_id) + '>数据接入完成')
                    print(str(repository_dict[repository_id]) + '数据格式错误数据量' + str(count_err))

    else:
        print(response_dict['message'], str(offset))


cursor.close()
db.close()
