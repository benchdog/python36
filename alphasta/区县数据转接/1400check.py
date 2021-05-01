# coding: utf-8
import json
from collections import Iterable, Iterator
import threadpool
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
import base64
import requests
import time
from threadpool import ThreadPool, makeRequests
import logging

#todo 获取t_viid_system表的deviceid和name进行映射kafka message的key
#todo web展示方式-可下载log文件也可web查看: http://ip/minio/智慧-裕华-海康_年月日.log
#todo 支持筛选只校验个别平台数据问题，提高对接效率
#todo minio研究：只打开对象下载和查看权限
#todo 所有函数封装工具包，方便以后工程直接调用
'''
首页：
智慧-裕华-海康数据问题
智慧-桥西-宇视数据问题
        ；；；
点击各区县厂商进入详情页
13019901015111111111 - 未知数据类型 - NotificationID字段不存在
13019901015111111111 - 未知数据类型 - InfoIDs字段长度必须是33
13019901015111111111 - 设备目录 - Latitude字段精度不是6位
13019901015111111111 - 设备目录 - PlaceCode字段长度必须是6(天网设备)或20(智慧社区设备)
13019901015111111111 - 设备目录 - FunctionType字段内容必须是1(车辆设备)或2(人脸设备)

'''
def log_err(k: str, msg: str, type='未知数据类型'):
    print(k + ' - ' + type + ' - ' + msg)

#校验每个字段是否存在和长度
def check_ifexist_len(k: str, k1: str, v1: dict, length:int, type='未知数据类型'):
    check_flag = True
    if k1 in v1.keys():
        if length > 0 and len(str(v1[k1])) != length:
            log_err(k, k1 + '字段长度必须是' + str(length), type=type)
            check_flag = False
        elif length == 0 and len(str(v1[k1])) == length:
            log_err(k, k1 + '字段为必填项', type=type)
            check_flag = False
        elif length == -1:
            pass
        return check_flag
    else:
        log_err(k, k1 + '字段不存在', type=type)
        return False

def check_type(k: str, v: dict):
    type = ['设备目录','卡口目录','人脸数据','车辆数据']
    notification_elements = ["NotificationID","SubscribeID","Title","TriggerTime","InfoIDs","DeviceList","TollgateObjectList","FaceObjectList","MotorVehicleObjectList"]
    check_ifexist_len(k, notification_elements[0], v, 33)
    check_ifexist_len(k, notification_elements[1], v, 33)
    check_ifexist_len(k, notification_elements[2], v, 0)
    check_ifexist_len(k, notification_elements[3], v, 14)
    check_ifexist_len(k, notification_elements[4], v, 33)

    if 'DeviceList' in v.keys():
        ape_elements = ["ApeID","Name","Model","IPAddr","Port","Longitude","Latitude","PlaceCode","OrgCode","IsOnline","UserId","Password","FunctionType"]
        if check_ifexist_len(k, 'APEObject', v['DeviceList'], 0, type=type[0]):
            ape_list = v['DeviceList']['APEObject']
            for ape in ape_list:
                if check_ifexist_len(k, ape_elements[0], ape, 20, type=type[0]):
                    if str(ape[ape_elements[0]])[10:13] != '119':
                        log_err(k,ape_elements[0] + '字段11-13位不是119',type=type[0])
                check_ifexist_len(k, ape_elements[1], ape, 0, type=type[0])
                check_ifexist_len(k, ape_elements[2], ape, 0, type=type[0])
                check_ifexist_len(k, ape_elements[3], ape, 0, type=type[0])
                check_ifexist_len(k, ape_elements[4], ape, 0, type=type[0])
                if check_ifexist_len(k, ape_elements[5], ape, 0, type=type[0]):
                    if len(str(ape[ape_elements[5]]).split('.')[1]) != 6:
                        log_err(k,ape_elements[5] + '字段精度必须是6位',type=type[0])
                if check_ifexist_len(k, ape_elements[6], ape, 0, type=type[0]):
                    if len(str(ape[ape_elements[6]]).split('.')[1]) != 6:
                        log_err(k,ape_elements[6] + '字段精度必须是6位',type=type[0])
                if check_ifexist_len(k, ape_elements[7], ape, 0, type=type[0]):
                    if len(ape[ape_elements[7]]) not in [6,20]:
                        log_err(k, ape_elements[7] + '字段长度必须是6(天网设备)或20(智慧社区设备)', type=type[0])
                check_ifexist_len(k, ape_elements[8], ape, 12, type=type[0])
                check_ifexist_len(k, ape_elements[9], ape, 0, type=type[0])
                check_ifexist_len(k, ape_elements[10], ape, 0, type=type[0])
                check_ifexist_len(k, ape_elements[11], ape, 0, type=type[0])
                if check_ifexist_len(k, ape_elements[12], ape, -1, type=type[0]):
                    if str(ape[ape_elements[12]]) not in ['1','2']:
                        log_err(k, ape_elements[12] + '字段内容必须是1(车辆设备)或2(人脸设备)', type=type[0])

    elif 'TollgateObjectList' in v.keys():
        log_err(k, '卡口OK')

    elif 'FaceObjectList' in v.keys():
        log_err(k, '人脸OK')

    elif 'MotorVehicleObjectList' in v.keys():
        log_err(k, '车辆OK')

    else:
        log_err(k, 'JSON体缺少4种数据标签：[DeviceList, TollgateObjectList, FaceObjectList, MotorVehicleObjectList]')


def check_notification(k: str, v: dict):
    if check_ifexist_len(k, 'SubscribeNotificationListObject', v, 0):
        if check_ifexist_len(k, 'SubscribeNotificationObject', v['SubscribeNotificationListObject'], 0):
            notification_list = v['SubscribeNotificationListObject']['SubscribeNotificationObject']
            for notification in notification_list:
                check_type(k, notification)


def alp_check(message):
    k = str(message.key, encoding="utf-8").split('_')[0]
    v = json.loads(str(message.value.decode()))
    check_notification(k, v)



if __name__ == '__main__':
    poolsize = 10
    topic = "dahua_101"
    # bootstrap_servers = ['tlnode168:9092', 'tlnode169:9092', 'tlnode170:9092', 'tlnode171:9092', 'tlnode172:9092', 'tlnode174:9092', 'tlnode2491:9092', 'tlnode2495:9092', 'tlnode2497:9092', 'tlnode2498:9092']
    bootstrap_servers = ['27.27.27.9:9092', '27.27.27.10:9092', '27.27.27.11:9092', '27.27.27.12:9092',
                         '27.27.27.13:9092', '27.27.27.14:9092', '27.27.27.15:9092', '27.27.27.16:9092']
    groupid = 'alp_check'
    consumer = KafkaConsumer(topic, groupid, bootstrap_servers=bootstrap_servers, auto_offset_reset="latest",
                             enable_auto_commit=True, auto_commit_interval_ms=5000)


    '''
    while consumer:
        print('1')
        pool = ThreadPool(poolsize)
        print('2')
        requests = makeRequests(alp_check, consumer)
        print(3)
        [pool.putRequest(req) for req in requests]
        print(4)
        pool.wait()
        print(5)
    '''

    # print(type(consumer))
    # print(isinstance(consumer,Iterator))
    for message in consumer:
        alp_check(message)