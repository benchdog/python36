#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
import json
import pymysql
import re
import datetime
def prem(db):
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s " % data)  # 结果表明已经连接成功
def reviewdata_insert(db):
    with open('/home/tempo/jz/jz_05140528/all.json', encoding='utf-8') as f:
    #with open('/home/tempo/jz/j_test.json', encoding='utf-8') as f:
        i = 0
        for line in f:
            try:
                i += 1
                #review_text = json.loads(line)
                #result = []
                if '\\r\\nimei:' in line:
                    imei = line.split('\\r\\nimei:')[1].split('\\r\\n')[0].strip()
                elif '&IMEI=' in line:
                    imei = line.split('&IMEI=')[1].split('&')[0].split(' ')[0].split('"')[0].strip()
                elif '&imei=' in line:
                    imei = line.split('&imei=')[1].split('&')[0].split(' ')[0].split('"')[0].strip()
                elif '"imei":"' in line:
                    imei = line.split('"imei":"')[1].split('"')[0].strip()
                elif '\\"id_imei\\":\\"' in line:
                    imei = line.split('\\"id_imei\\":\\"')[1].split('\\"')[0].strip()
                elif '\\r\\nHalley-IMEI:' in line:
                    imei = line.split('\\r\\nHalley-IMEI:')[1].split('\\r\\n')[0].strip()
                elif '&opt_imei=' in line:
                    imei = line.split('&opt_imei=')[1].split('&')[0].split(' ')[0].split('"')[0].strip()
                else:
                    imei = ''
                if '\\r\\nImsi:' in line:
                    imsi = line.split('\\r\\nImsi:')[1].split('\\r\\n')[0].strip()
                elif '&imsi=' in line:
                    imsi = line.split('&imsi=')[1].split('&')[0].split(' ')[0].split('"')[0].split('\\r\\n')[0].strip()
                elif '\\"id_imsi\\":\\"' in line:
                    imsi = line.split('\\"id_imsi\\":\\"')[1].split('\\"')[0].strip()
                elif '&opt_imsi=' in line:
                    imsi = line.split('&opt_imsi=')[1].split('&')[0].split(' ')[0].split('"')[0].strip()
                else:
                    imsi = ''
                if '\\r\\nPhoneNmbers:' in line:
                    phone_num = line.split('\\r\\nPhoneNmbers:')[1].split('\\r\\n')[0].strip().strip('+86')
                elif re.findall(r"&p=1[35678]\d{9}\D",line):
                    phone_num = re.findall(r"&p=1[35678]\d{9}",line)[0].strip('&p=')
                else:
                    phone_num = ''
                if '"wechat_num":"' in line:
                    virtual_num = line.split('"wechat_num":"')[1].split('"')[0].strip()
                elif '"qq_num":"' in line:
                    virtual_num = line.split('"qq_num":"')[1].split('"')[0].strip()
                elif '"appId":0,' in line and 'wxuin=' in line:
                    virtual_num = line.split('wxuin=')[1].split(';')[0].split('&')[0].split('"')[0].split(' ')[0].strip()
                elif '"appId":0,' in line and '?uin=' in line:
                    virtual_num = line.split('?uin=')[1].split('&')[0].split(';')[0].split('"')[0].split(' ')[0].strip()
                elif '"appId":0,' in line and '&uin=' in line:
                    virtual_num = line.split('&uin=')[1].split('&')[0].split(';')[0].split('"')[0].split(' ')[0].strip()
                elif '"appId":1,' in line and '&vuin=' in line:
                    virtual_num = line.split('&vuin=')[1].split('&')[0].split(';')[0].split('"')[0].split(' ')[0].strip()
                elif '"appId":1,' in line and '?vuin=' in line:
                    virtual_num = line.split('?vuin=')[1].split('&')[0].split(';')[0].split('"')[0].split(' ')[0].strip()
                elif '&weibo_uid=' in line:
                    virtual_num = line.split('&weibo_uid=')[1].split('&')[0].split(' ')[0].split('"')[0].strip()
                elif '"weibo_uid":"' in line:
                    virtual_num = line.split('"weibo_uid":"')[1].split('"')[0].split(' ')[0].split('&')[0].strip()
                elif '"qqmusic_guid":"' in line:
                    virtual_num = line.split('"qqmusic_guid":"')[1].split('"')[0].split(';')[0].split(' ')[0].split('&')[0].strip()
                elif '"toutiao_device_id":"' in line:
                    virtual_num = line.split('"toutiao_device_id":"')[1].split('"')[0].split(';')[0].split(' ')[0].split('&')[0].strip()
                elif '"tencentnews_devid":"' in line:
                    virtual_num = line.split('"tencentnews_devid":"')[1].split('"')[0].split(';')[0].split(' ')[0].split('&')[0].strip()
                elif '"kuaishou_ud":"' in line:
                    virtual_num = line.split('"kuaishou_ud":"')[1].split('"')[0].split(';')[0].split(' ')[0].split('&')[0].strip()
                elif '&uuid=' in line:
                    virtual_num = line.split('&uuid=')[1].split('&')[0].split(' ')[0].split('"')[0].strip()
                elif '"uuid":"' in line:
                    virtual_num = line.split('"uuid":"')[1].split('"')[0].split('&')[0].split(' ')[0].strip()
                elif '&openudid=' in line:
                    virtual_num = line.split('&openudid=')[1].split('&')[0].split('"')[0].split(' ')[0].strip()
                elif '\\"openudid\\":\\"' in line:
                    virtual_num = line.split('\\"openudid\\":\\"')[1].split('\\"')[0].split('"')[0].split(' ')[0].strip()
                elif '?openudid=' in line:
                    virtual_num = line.split('?openudid=')[1].split('&')[0].split('"')[0].split(' ')[0].strip()                
                elif '\\"openudid\\" : \\"' in line:
                    virtual_num = line.split('\\"openudid\\" : \\"')[1].split('\\"')[0].split('"')[0].split(' ')[0].strip()
                elif '&gsopenudid=' in line:
                    virtual_num = line.split('&gsopenudid=')[1].split('&')[0].split('"')[0].split(' ')[0].strip()
                elif '&udid=' in line:
                    virtual_num = line.split('&udid=')[1].split('&')[0].split('"')[0].split(' ')[0].strip()
                elif '\\r\\nudid: ' in line:
                    virtual_num = line.split('\\r\\nudid: ')[1].split('\\r\\n')[0].split('"')[0].split(' ')[0].strip()
                elif '&fudid=' in line:
                    virtual_num = line.split('&fudid=')[1].split('&')[0].split('"')[0].split(' ')[0].strip()
                elif '\\"udid\\":\\"' in line:
                    virtual_num = line.split('\\"udid\\":\\"')[1].split('\\"')[0].split('"')[0].split(' ')[0].strip()
                elif 'tvfe_boss_uuid' in line:
                    virtual_num = line.split('tvfe_boss_uuid')[1].split(';')[0].split('&')[0].split(' ')[0].split('"')[0].strip()
                elif '&cuuid=' in line:
                    virtual_num = line.split('&cuuid=')[1].split('&')[0].split(';')[0].split(' ')[0].split('"')[0].strip()
                elif '&suuid=' in line:
                    virtual_num = line.split('&suuid=')[1].split('&')[0].split(';')[0].split(' ')[0].split('"')[0].strip()
                elif ' vuserid=' in line:
                    virtual_num = line.split(' vuserid=')[1].split(';')[0].split('"')[0].split(' ')[0].split('&')[0].strip()
                elif '"vuserid=' in line:
                    virtual_num = line.split('"vuserid=')[1].split(';')[0].split('"')[0].split(' ')[0].split('&')[0].strip()
                elif '&vuserid=' in line:
                    virtual_num = line.split('&vuserid=')[1].split('&')[0].split('"')[0].split(' ')[0].split(';')[0].strip()
                elif ';vuserid=' in line:
                    virtual_num = line.split(';vuserid=')[1].split(';')[0].split('"')[0].split(' ')[0].split('&')[0].strip()
                elif '&userid=' in line:
                    virtual_num = line.split('&userid=')[1].split('&')[0].split('"')[0].split(' ')[0].split(';')[0].strip()
                elif '; sd_userid=' in line:
                    virtual_num = line.split('; sd_userid=')[1].split(';')[0].split('"')[0].split(' ')[0].split('&')[0].strip()
                elif '&ups_userid=' in line:
                    virtual_num = line.split('&ups_userid=')[1].split('&')[0].split('"')[0].split(' ')[0].split(';')[0].strip()
                elif '"sd_userid=' in line:
                    virtual_num = line.split('"sd_userid=')[1].split(';')[0].split('"')[0].split(' ')[0].split('&')[0].strip()
                elif '\\"userid\\":' in line:
                    virtual_num = line.split('\\"userid\\":')[1].split(',')[0].split('"')[0].split('&')[0].split(';')[0].strip()
                elif '; userid=' in line:
                    virtual_num = line.split('; userid=')[1].split('\\r\\n')[0].split('"')[0].split(' ')[0].split(';')[0].strip()
                elif '&tqt_userid=' in line:
                    virtual_num = line.split('&tqt_userid=')[1].split('&')[0].split('"')[0].split(' ')[0].split(';')[0].strip()
                elif ' userid/' in line:
                    virtual_num = line.split(' userid/')[1].split('\\r\\n')[0].split('"')[0].split(' ')[0].split(';')[0].strip()
                elif '&aduserid=' in line:
                    virtual_num = line.split('&aduserid=')[1].split('&')[0].split('"')[0].split(' ')[0].split(';')[0].strip()
                elif 'uid=\\"' in line:
                    virtual_num = line.split('uid=\\"')[1].split('\\"')[0].split(';')[0].split(' ')[0].split('&')[0].strip()
                elif '; uid=' in line:
                    virtual_num = line.split('; uid=')[1].split(';')[0].split('"')[0].split(' ')[0].split('&')[0].strip()
                elif '?uid=' in line:
                    virtual_num = line.split('?uid=')[1].split(';')[0].split(' ')[0].split('&')[0].split('"')[0].strip() 
                elif '&uid=' in line:
                    virtual_num = line.split('&uid=')[1].split('&')[0].split(' ')[0].split(';')[0].split('"')[0].strip()
                elif '\\"uid\\":\\"' in line:
                    virtual_num = line.split('\\"uid\\":\\"')[1].split('\\"')[0].split(' ')[0].split(';')[0].split('&')[0].strip()
                elif 'gdt_uid=' in line:
                    virtual_num = line.split('gdt_uid=')[1].split('"')[0].split(' ')[0].split(';')[0].split('&')[0].strip()
                else:
                    virtual_num = ''
                review_text = json.loads(line)
                result = []
                if 'addTs' not in review_text['_source']['allUserAttr'].keys():
                    #review_text['_source']['allUserAttr']['addTs'] = ''
                    addTs = ''
                else:
                    addTs_std = time.localtime(int(review_text['_source']['allUserAttr']['addTs']))
                    addTs = time.strftime("%Y-%m-%d %H:%M:%S",addTs_std)
                if 'lastTs' not in review_text['_source']['allUserAttr'].keys():
                    #review_text['_source']['allUserAttr']['lastTs'] = ''
                    lastTs = ''
                else:
                    lastTs_std = time.localtime(int(review_text['_source']['allUserAttr']['lastTs']))
                    lastTs = time.strftime("%Y-%m-%d %H:%M:%S",lastTs_std)
                if 'brand' not in review_text['_source']['allUserAttr'].keys():
                    review_text['_source']['allUserAttr']['brand'] = ''
                if 'model' not in review_text['_source']['allUserAttr'].keys():
                    review_text['_source']['allUserAttr']['model'] = ''
                if 'os_type' not in review_text['_source']['allUserAttr'].keys():
                    review_text['_source']['allUserAttr']['os_type'] = ''
                if 'os_version' not in review_text['_source']['allUserAttr'].keys():
                    review_text['_source']['allUserAttr']['os_version'] = ''
                if 'personasId' not in review_text['_source']['allUserAttr'].keys():
                    review_text['_source']['allUserAttr']['personasId'] = ''
                if 'appUserId' not in review_text['_source'].keys():
                    review_text['_source']['appUserId'] = ''
                if 'host' not in review_text['_source'].keys():
                    review_text['_source']['host'] = ''
                if 'behaviorId' not in review_text['_source'].keys():
                    review_text['_source']['behaviorId'] = ''
                
                ws_std = time.localtime(int(str(review_text['_source']['ws'])[:-3]))
                ws = time.strftime("%Y-%m-%d %H:%M:%S",ws_std)
                
                ts_std = time.localtime(int(review_text['_source']['ts']))
                ts = time.strftime("%Y-%m-%d %H:%M:%S",ts_std)
                result.append((review_text['_id'],review_text['_source']['dMac'],review_text['_source']['ns'],review_text['_source']['sMac'],review_text['_source']['dip'],addTs,review_text['_source']['allUserAttr']['os_type'],review_text['_source']['allUserAttr']['os_version'],review_text['_source']['allUserAttr']['model'],review_text['_source']['allUserAttr']['personasId'],review_text['_source']['allUserAttr']['brand'],lastTs,review_text['_source']['dArea'],review_text['_source']['sArea'],review_text['_source']['sCountry'],review_text['_source']['appId'],review_text['_source']['dCountry'],review_text['_source']['host'],review_text['_source']['sip'],ws,review_text['_source']['appUserId'],ts,review_text['_source']['behaviorId'],imei,imsi,phone_num,virtual_num))
                inesrt_re = "insert into jz_05140528(_id,dMac,ns,sMac,dip,addTs,os_type,os_version,model,personasId,brand,lastTs,dArea,sArea,sCountry,appId,dCountry,host,sip,ws,appUserId,ts,behaviorId,imei,imsi,phone_num,virtual_num) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor = db.cursor()
                cursor.executemany(inesrt_re, result)
                db.commit()
                print(u'第s%条数据插入MySQL成功' % i)
                print(u'\n')
            except Exception as e:
                db.rollback()
                print(e)
            '''
            finally:
                print(i)
                print("imei:",imei)
                print("imsi:",imsi)
                print("手机号:",phone_num)
                print("虚拟账号:",virtual_num) 
            '''
if __name__ == "__main__":  # 起到一个初始化或者调用函数的作用
    starttime = datetime.datetime.now()
    db = pymysql.connect("10.41.77.13", "midbase", "123456", "midbase", charset='utf8')
    cursor = db.cursor()
    prem(db)
    reviewdata_insert(db)
    cursor.close()
    endtime = datetime.datetime.now()
    print (endtime - starttime)
