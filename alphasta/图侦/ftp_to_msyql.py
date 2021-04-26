#coding:utf8
import zipfile
import os
import datetime
import pymysql
from ftplib import FTP
FTP.encoding = 'utf8' #ftplib包里面对encoding设置成了latin-1，需要重设成utf8,解决ftp中文目录报错问题
from minio import Minio

#从ftp下载zip数据到本地
def down_from_ftp(ftp_ip, ftp_user, ftp_passwd, remotepath, localpath):
    ftp = FTP()
    bufsize = 1024
    dowd_res = 0
    try:
        ftp.connect(ftp_ip, 21)
        ftp.login(ftp_user, ftp_passwd)
        if ftp:
            try:
                fp = open(localpath, 'wb')
                ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
                ftp.set_debuglevel(0)
                print('ftp下载成功：' + str(remotepath))
                dowd_res = 1
            except Exception as e:
                print('ftp下载异常：' + str(e))
            finally:
                ftp.close()
    except Exception as e:
        print('ftp登录异常' + str(e))
    finally:
        return dowd_res

#解压zip包到指定目录
def unzip(zfile,dstpath):
    unzip_list = []
    if os.path.exists(zfile):
        try:
            zip = zipfile.ZipFile(zfile, 'r')
            # namelist()方法返回zip文件列表
            # for file in zip.namelist():
            #     zip.extract(file,dstpath)
            zip.extractall(dstpath, zip.namelist())
            unzip_list = zip.namelist()
            print('解压成功：' + str(unzip_list))
        except Exception as e:
            print('解压失败：' + str(e))
        finally:
            zip.close()
            return unzip_list


#解析txt文本数据入mysql，图片入minio
def tomysql(txtfile,db):
    params = []
    append_flag = 0
    # print('更新库：' + str(txtfile))
    with open(txtfile, 'r', encoding='gbk', errors = 'ignore') as fr:
        #增量或全量在逃人员
        if str(txtfile).endswith('_ZL.txt') or '_' not  in str(txtfile):
            if '_' not  in str(txtfile):
                print("全量入库，请确认库表已初始化")
            for line in fr.readlines():
                line = line.strip('\n').replace('"','').split(',')
                # todo minio
                if append_flag:
                    # print(line)
                    params.append(tuple([str(line[1]), str(line[10]), str(line[9]), '在逃人员', str(line[21]), str(line[22]), 'http://minio.pic']))
                append_flag = 1
            #todo 考虑插入重复
            sql = "insert into alp_zdr(zdr_name, zdr_id_num, zdr_address, zdr_type_name, zdr_unit_name, zdr_unit_phone, pic_url) \
            values(%s,%s,%s,%s,%s,%s,%s) on duplicate key update zdr_id_num = values(zdr_id_num)"
            # with db.cursor() as cursor:
            #     cursor.executemany(sql, params)
            try:
                cursor = db.cursor()
                cursor.executemany(sql, params)
                db.commit()
                print('更新成功：' + str(txtfile))
            except Exception as e:
                db.rollback()
                print('更新异常：' + str(txtfile) + str(e))
            finally:
                cursor.close()
        # 删除或撤销在逃人员
        elif str(txtfile).endswith(('_SC.txt', '_CX.txt')):
            for line in fr.readlines():
                line = line.strip('\n').replace('"', '').split(',')
                #todo minio
                if append_flag:
                    params.append(str(line[10]))
                append_flag = 1
            params_tuple = tuple(params)
            sql = "delete from alp_zdr where zdr_id_num in " + str(params_tuple)
            try:
                cursor = db.cursor()
                cursor.execute(sql)
                db.commit()
                print('删除成功：' + str(txtfile))
            except Exception as e:
                db.rollback()
                print('删除异常：' + str(txtfile) + str(e))
            finally:
                cursor.close()
        else:print('未知数据类型：' + str(txtfile))


if __name__ == '__main__':
    today = str(datetime.date.today()).replace('-', '')
    workpath = os.path.join('C:\\Users\\wf\\Desktop\\', today)
    if not os.path.exists(workpath):
        os.makedirs(workpath)
    ftp_ip = '111.61.198.98'
    ftp_user = 'ftpuser'
    ftp_passwd = '6yHN7ujm*IK,'
    ftp_base_remote = '简项数据/' + today
    ftp_base_local = workpath + '/' + today
    db = pymysql.connect(
        host='27.27.27.16', #视频中心智慧社区互联网侧
        port=3306,
        user='alpview',
        password='123456',
        db='db1400',
        charset='utf8'
    )

mc = Minio('27.27.27.14:7000',access_key='minioadmin',secret_key='minioadmin',secure=False)
# mc.make_bucket("onrun") #生成一个bucket，类似文件夹
res = mc.fput_object(bucket_name='test', object_name='1.jpg',file_path='C:\\Users\\wf\\Desktop\\1.jpg',content_type='image/jpeg')
print(res.object_name)

'''
#下载当天照片数据
if down_from_ftp(ftp_ip, ftp_user, ftp_passwd, ftp_base_remote + '_ZP.zip', ftp_base_local + '_ZP.zip'):
    if unzip(ftp_base_local + '_ZP.zip', workpath):
        print('图片数据解压成功')

total_flag = 1
if total_flag:
    #下载当天全量数据
    if down_from_ftp(ftp_ip, ftp_user, ftp_passwd, ftp_base_remote + '.zip', ftp_base_local + '.zip'):
        unzip_list_total = unzip(ftp_base_local + '.zip', workpath)
        if unzip_list_total:
            for txtfile in unzip_list_total:
                tomysql(os.path.join(workpath, txtfile), db)
else:
    #下载当天变量（删除、撤销、增量）数据
    if down_from_ftp(ftp_ip, ftp_user, ftp_passwd, ftp_base_remote + '_ZL.zip', ftp_base_local + '_ZL.zip'):
        unzip_list_chg = unzip(ftp_base_local + '_ZL.zip', workpath)
        if unzip_list_chg:
            for txtfile in unzip_list_chg:
                tomysql(os.path.join(workpath, txtfile), db)
'''

db.close()