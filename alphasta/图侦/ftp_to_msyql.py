#!coding:utf8
import zipfile
import os
import datetime
import pymysql

today = str(datetime.date.today().replace('-',''))
workpath = os.path.join('C:\\Users\\wf\\Desktop', today)
# imgpath = os.path.join(workpath, 'img')
if not os.path.exists(workpath):
    os.makedirs(workpath)

db = pymysql.connect(
        host='13.32.4.170',
        # host='192.168.23.112',
        port=3306,
        user='root',
        password='wanfang@2001',
        db='db1400',
        # db='ligh',
        charset='utf8'
)

#todo 将ftp中的zip数据搬运到workdir
def copy_from_ftp():
    pass


#txt入mysql，图片入minio
def tomysql(txtfile,db):
    with open(txtfile, 'r', encoding='utf8') as fr:
        params = []
        if str(txtfile).endswith(('_SC.txt','_CX.txt')):
            for line in fr.readlines():
                line = line.strip().split(',')
                # todo 筛选需要的字段
                #todo minio
                params.append(line[0])
            params_tuple = tuple(params)
            sql = "delete from t1 where tid in %s"
            with db.cursor() as cursor:
                cursor.execute(sql,str(params_tuple))
        elif str(txtfile).endswith('_ZL.txt') or '_' not  in str(txtfile):
            if '_' not  in str(txtfile):
                print("全量入库，请确认库表已初始化")
            for line in fr.readlines():
                line = line.strip().split(',')
#                 todo 筛选字段
                params.append(tuple(line[0,1,2,3,4]))
            #todo 考虑插入重复
            sql = "insert into t1() values()"
            with db.cursor() as cursor:
                cursor.execute(sql, params)
        else:print(str(txtfile))


#解压zip包到指定目录
def extract_intodb(zfile,dstpath):
    if os.path.exists(zfile):
        zip = zipfile.ZipFile(zfile, 'r')
        # namelist()方法返回zip文件列表
        print('解压文件个数：' + str(len(zip.namelist())))
        # for file in zip.namelist():
        #     zip.extract(file,dstpath)
        zip.extractall(dstpath, zip.namelist())
        zip.close()

db.close()

if __name__ == '__main__':
    pass