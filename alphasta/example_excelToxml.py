# coding=utf-8
import xlrd
import datetime
import time
import sys
import xml.dom.minidom
import os

print(sys.getdefaultencoding())
# os.reload(sys)  # 就是这么坑爹,否则下面会报错
# sys.setdefaultencoding('utf-8')  # py默认是ascii。。要设成utf8


# excel中 数据格式如下:
# UID         第四天
# 1579880025  10:00-13:30
# 1677982825  10:00-12:00
# 1704410718  10:00-12:00
# 83713892    10:00-12:00
# 1546551561  10:00-12:00
# 1298790776  10:00-12:00


def open_excel(file):
    try:
        data = xlrd.open_workbook(file)  # xlrd 操作excel的外部库
        return data
    except Exception as  e:
        print(str(e))


bgntm = '2017-05-18_'


def get_time_t(stime):
    stime = bgntm + stime + ':00'
    # return time.strptime(stime, '%Y-%m-%d %H:%M:%S')      #将时间转成时间戳
    return stime


def excel_table_byindex(file, colnnameindex=0, by_index=0):
    data = open_excel(file)  # 打开excel

    table = data.sheets()[by_index]

    nrows = table.nrows
    ncols = table.ncols

    doc = xml.dom.minidom.Document()  # 打开xml对象
    xmain = doc.createElement('main')
    doc.appendChild(xmain)

    for nrow in range(0, nrows):  # 遍历每一行
        if nrow == 0:
            continue

        uid = table.cell(nrow, 0).value  # 取值..第一列

        item = doc.createElement('%d' % uid)  # 生成节点
        stime = table.cell(nrow, 1).value  # 第二列的值
        stime = stime.strip()  # 去除空格..excel数据里 经常会无意有蛋疼的多余空格
        listT = stime.split('-')  # 按 -分割字符串

        # sbgn = 'bgn = %d'%time.mktime(get_time_t(listT[0]))
        sbgn = 'bgn = ' + get_time_t(listT[0])
        print
        'uid=%d' % uid
        print
        'bgn:' + sbgn
        send = 'end = ' + get_time_t(listT[1])
        # send = 'end = %d'%time.mktime(get_time_t(listT[1]))
        print
        'end:' + send
        exxbgn = doc.createTextNode(sbgn)  # 纯文本节点
        exxend = doc.createTextNode(send)
        item.appendChild(exxbgn)  # 加入树中
        item.appendChild(exxend)

        # ebgn = doc.createElement('bgn')
        # eend = doc.createElement('bgn')
        # item.appendChild(ebgn)
        # item.appendChild(eend)

        # item.setAttribute('bgn', '%d'%time.mktime(get_time_t(listT[0]))) #设置节点属性
        # item.setAttribute('end', '%d'%time.mktime(get_time_t(listT[1])))
        # for lt in listT:
        # print time.mktime(get_time_t(lt))

        xmain.appendChild(item)

    f = open('C:/Users/think/Desktop/res.xml', 'w')  # xml文件输出路径
    f.write(doc.toprettyxml())
    f.close()


excel_table_byindex('C:/Users/think/Desktop/test.xlsx')  # excel文件路径