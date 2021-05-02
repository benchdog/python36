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

#todo 多线程消费kafka
#todo 日志加日期时间
#todo 获取t_viid_system表的deviceid和name进行映射kafka message的key
#todo web展示方式-可下载log文件也可web查看: http://ip/minio/智慧-裕华-海康_年月日.log
#todo 支持筛选只校验个别平台数据问题，提高对接效率
#todo minio研究：只打开对象下载和查看权限
#todo 所有函数封装工具包，方便以后工程直接调用
#todo shell脚本扫ftp json到1400-api
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
13019901015111111111 - 设备目录 - FunctionType字段取值必须是1(车辆设备)或2(人脸设备)

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
    subimg_elements = ['ImageID', 'EventSort', 'DeviceID', 'StoragePath', 'Type', 'FileFormat', 'ShotTime', 'Width','Height', 'Data']
    notification_elements = ["NotificationID","SubscribeID","Title","TriggerTime","InfoIDs","DeviceList","TollgateObjectList","FaceObjectList","MotorVehicleObjectList"]
    check_ifexist_len(k, notification_elements[0], v, 33)
    check_ifexist_len(k, notification_elements[1], v, 33)
    check_ifexist_len(k, notification_elements[2], v, 0)
    check_ifexist_len(k, notification_elements[3], v, 14)
    check_ifexist_len(k, notification_elements[4], v, 0)

    if 'DeviceList' in v.keys():
        ape_elements = ["ApeID","Name","Model","IPAddr","Port","Longitude","Latitude","PlaceCode","OrgCode","IsOnline","UserId","Password","FunctionType"]
        if check_ifexist_len(k, 'APEObject', v['DeviceList'], 0, type=type[0]):
            ape_list = v['DeviceList']['APEObject']
            for ape in ape_list:
                if check_ifexist_len(k, ape_elements[0], ape, 20, type=type[0]):
                    if str(ape[ape_elements[0]])[10:13] != '119':
                        log_err(k,ape_elements[0] + '字段11-13位必须是119',type=type[0])
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
                        log_err(k, ape_elements[12] + '字段取值范围：[1-车辆设备；2-人脸设备]', type=type[0])

    elif 'TollgateObjectList' in v.keys():
        tollgate_elements = ["TollgateID","Name","Longitude","Latitude","PlaceCode","OrgCode","Status","TollgateCat","LaneNum","TollgateUsage"]
        if check_ifexist_len(k, 'TollgateObject', v['TollgateObjectList'], 0, type=type[1]):
            tollgate_list = v['TollgateObjectList']['TollgateObject']
            for tollgate in tollgate_list:
                if check_ifexist_len(k, tollgate_elements[0], tollgate, 20, type=type[1]):
                    if str(tollgate[tollgate_elements[0]])[10:13] != '121':
                        log_err(k,tollgate_elements[0] + '字段11-13位必须是121',type=type[1])
                check_ifexist_len(k, tollgate_elements[1], tollgate, 0, type=type[1])
                if check_ifexist_len(k, tollgate_elements[2], tollgate, 0, type=type[1]):
                    if len(str(tollgate[tollgate_elements[2]]).split('.')[1]) != 6:
                        log_err(k,tollgate_elements[2] + '字段精度必须是6位',type=type[1])
                if check_ifexist_len(k, tollgate_elements[3], tollgate, 0, type=type[1]):
                    if len(str(tollgate[tollgate_elements[3]]).split('.')[1]) != 6:
                        log_err(k,tollgate_elements[3] + '字段精度必须是6位',type=type[1])
                if check_ifexist_len(k, tollgate_elements[4], tollgate, 0, type=type[1]):
                    if len(tollgate[tollgate_elements[4]]) not in [6,20]:
                        log_err(k, tollgate_elements[4] + '字段长度必须是6(天网设备)或20(智慧社区设备)', type=type[0])
                check_ifexist_len(k, tollgate_elements[5], tollgate, 12, type=type[1])
                check_ifexist_len(k, tollgate_elements[6], tollgate, 1, type=type[1])
                if check_ifexist_len(k, tollgate_elements[7], tollgate, 0, type=type[1]):
                    if str(tollgate[tollgate_elements[7]]) not in ['10','20','30','31','40','41','99']:
                        log_err(k, tollgate_elements[7] + '字段取值范围：[10-国际；20-省际；30-市际；31-市区；40-县际；41-县区；99-其他]', type=type[1])
                check_ifexist_len(k, tollgate_elements[8], tollgate, 0, type=type[1])
                if check_ifexist_len(k, tollgate_elements[9], tollgate, 0, type=type[1]):
                    if str(tollgate[tollgate_elements[9]]) not in ['80','81','82']:
                        log_err(k, tollgate_elements[9] + '字段取值范围：[80-治安卡口；81-交通卡口；82-其他]', type=type[1])

    elif 'FaceObjectList' in v.keys():
        face_elements = ['FaceID','InfoKind','SourceID','DeviceID','LeftTopX','LeftTopY','RightBtmX','RightBtmY','IsDriver','IsForeigner','IsSuspectedTerrorist','IsCriminalInvolved','IsDetainees','IsVictim','IsSuspiciousPerson','SubImageList']
        if check_ifexist_len(k, 'FaceObject', v['FaceObjectList'], 0, type=type[2]):
            face_list = v['FaceObjectList']['FaceObject']
            for face in face_list:
                check_ifexist_len(k, face_elements[0], face, 48, type=type[2])
                if check_ifexist_len(k, face_elements[1], face, 0, type=type[2]):
                    if str(face[face_elements[1]]) not in ['0','1','2']:
                        log_err(k, face_elements[1] + '字段取值范围：[0-其他；1-自动采集；2-人工采集]', type=type[2])
                check_ifexist_len(k, face_elements[2], face, 41, type=type[2])
                check_ifexist_len(k, face_elements[3], face, 20, type=type[2])
                check_ifexist_len(k, face_elements[4], face, -1, type=type[2])
                check_ifexist_len(k, face_elements[5], face, -1, type=type[2])
                check_ifexist_len(k, face_elements[6], face, -1, type=type[2])
                check_ifexist_len(k, face_elements[7], face, -1, type=type[2])
                for e in face_elements[8:15]:
                    if check_ifexist_len(k, e, face, 0, type=type[2]):
                        if str(face[e]) not in ['0','1','2']:
                            log_err(k, e + '字段取值范围：[0-否；1-是；2-不确定]', type=type[2])
                if check_ifexist_len(k, face_elements[15], face, 0, type=type[2]):
                    if check_ifexist_len(k, 'SubImageInfoObject', face[face_elements[15]], 0, type=type[2]):
                        subimg_list = face[face_elements[15]]['SubImageInfoObject']
                        subimg_type = []
                        for subimg in subimg_list:
                            check_ifexist_len(k, subimg_elements[0], subimg, 41, type=type[2])
                            check_ifexist_len(k, subimg_elements[1], subimg, -1, type=type[2])
                            check_ifexist_len(k, subimg_elements[2], subimg, 20, type=type[2])
                            check_ifexist_len(k, subimg_elements[3], subimg, -1, type=type[2])
                            if check_ifexist_len(k, subimg_elements[4], subimg, 0, type=type[2]):
                                if str(subimg[subimg_elements[4]]) in ['11','14']:
                                    subimg_type.append(str(subimg[subimg_elements[4]]))
                                else:
                                    log_err(k, "大小图类型Type取值范围：[11-人脸小图；14-人脸大图]",type=type[2])
                            check_ifexist_len(k, subimg_elements[5], subimg, 0, type=type[2])
                            check_ifexist_len(k, subimg_elements[6], subimg, 14, type=type[2])
                            check_ifexist_len(k, subimg_elements[7], subimg, 0, type=type[2])
                            check_ifexist_len(k, subimg_elements[8], subimg, 0, type=type[2])
                            check_ifexist_len(k, subimg_elements[9], subimg, 0, type=type[2])
                        if '11' not in subimg_type and '14' not in subimg_type:
                            log_err(k, '无大小图', type=type[2])
                        elif '11' not in subimg_type and '14' in subimg_type:
                            log_err(k, '有大图，无小图', type=type[2])
                        elif '11' in subimg_type and '14'not in subimg_type:
                            log_err(k, '有小图，无大图', type=type[2])

    elif 'MotorVehicleObjectList' in v.keys():
        motor_elements = ['MotorVehicleID','InfoKind','SourceID','TollgateID','DeviceID','StorageUrl1','LeftTopX','LeftTopY','RightBtmX','RightBtmY','LaneNo','HasPlate','PlateClass','PlateColor','PlateNo','VehicleColor','SubImageList']
        if check_ifexist_len(k, 'MotorVehicleObject', v['MotorVehicleObjectList'], 0, type=type[3]):
            motor_list = v['MotorVehicleObjectList']['MotorVehicleObject']
            for motor in motor_list:
                check_ifexist_len(k, motor_elements[0], motor, 48, type=type[3])
                if check_ifexist_len(k, motor_elements[1], motor, 0, type=type[3]):
                    if str(motor[motor_elements[1]]) not in ['0','1','2']:
                        log_err(k, motor_elements[1] + '字段取值范围：[0-其他；1-自动采集；2-人工采集]', type=type[3])
                check_ifexist_len(k, motor_elements[2], motor, 41, type=type[3])
                check_ifexist_len(k, motor_elements[3], motor, 20, type=type[3])
                check_ifexist_len(k, motor_elements[4], motor, 20, type=type[3])
                for e in motor_elements[5:16]:
                    check_ifexist_len(k, e, motor, 0, type=type[3])
                if check_ifexist_len(k, motor_elements[15], motor, 0, type=type[3]):
                    if check_ifexist_len(k, 'SubImageInfoObject', motor[motor_elements[16]], 0, type=type[3]):
                        subimg_list = motor[motor_elements[16]]['SubImageInfoObject']
                        subimg_type = []
                        for subimg in subimg_list:
                            check_ifexist_len(k, subimg_elements[0], subimg, 41, type=type[3])
                            check_ifexist_len(k, subimg_elements[1], subimg, -1, type=type[3])
                            check_ifexist_len(k, subimg_elements[2], subimg, 20, type=type[3])
                            check_ifexist_len(k, subimg_elements[3], subimg, -1, type=type[3])
                            if check_ifexist_len(k, subimg_elements[4], subimg, 0, type=type[3]):
                                if str(subimg[subimg_elements[4]]) in ['01','02']:
                                    subimg_type.append(str(subimg[subimg_elements[4]]))
                                else:
                                    log_err(k, "大小图类型Type取值范围：[02-车辆小图；01-车辆大图]",type=type[3])
                            check_ifexist_len(k, subimg_elements[5], subimg, 0, type=type[3])
                            check_ifexist_len(k, subimg_elements[6], subimg, 14, type=type[3])
                            check_ifexist_len(k, subimg_elements[7], subimg, 0, type=type[3])
                            check_ifexist_len(k, subimg_elements[8], subimg, 0, type=type[3])
                            check_ifexist_len(k, subimg_elements[9], subimg, 0, type=type[3])
                        if '02' not in subimg_type and '01' not in subimg_type:
                            log_err(k, '无大小图', type=type[3])
                        elif '02' not in subimg_type and '01' in subimg_type:
                            log_err(k, '有大图，无小图', type=type[3])
                        elif '02' in subimg_type and '01'not in subimg_type:
                            log_err(k, '有小图，无大图', type=type[3])

    else:
        log_err(k, 'JSON体必须至少包含以下1种字段：[DeviceList, TollgateObjectList, FaceObjectList, MotorVehicleObjectList]')

def check_notification(k: str, v: dict):
    if check_ifexist_len(k, 'SubscribeNotificationListObject', v, 0):
        if check_ifexist_len(k, 'SubscribeNotificationObject', v['SubscribeNotificationListObject'], 0):
            notification_list = v['SubscribeNotificationListObject']['SubscribeNotificationObject']
            for notification in notification_list:
                check_type(k, notification)


def alp_check(message, viid_filter: list, viid_dict: dict):
    k_id = str(message.key, encoding="utf-8").split('_')[0]
    if k_id in viid_filter:
        k = lambda k_id: viid_dict[k_id] if k_id in viid_dict.keys() else k_id
        v = json.loads(str(message.value.decode()))
        check_notification(k, v)

if __name__ == '__main__':
    poolsize = 10
    # bootstrap_servers = ['tlnode168:9092', 'tlnode169:9092', 'tlnode170:9092', 'tlnode171:9092', 'tlnode172:9092', 'tlnode174:9092', 'tlnode2491:9092', 'tlnode2495:9092', 'tlnode2497:9092', 'tlnode2498:9092']
    bootstrap_servers = ['27.27.27.9:9092', '27.27.27.10:9092', '27.27.27.11:9092', '27.27.27.12:9092', '27.27.27.13:9092', '27.27.27.14:9092', '27.27.27.15:9092', '27.27.27.16:9092']
    topic = "dahua_101"
    groupid = 'alp_check'
    consumer = KafkaConsumer(topic, groupid, bootstrap_servers=bootstrap_servers, auto_offset_reset="latest", enable_auto_commit=True, auto_commit_interval_ms=5000)
    viid_dict = {}
    viid_filter = []
    for message in consumer:
        alp_check(message, viid_filter, viid_dict)