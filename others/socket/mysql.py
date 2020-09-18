# -*- coding:utf-8 -*-
import pymysql

db = pymysql.connect("localhost","root","666888","test")
cursor = db.cursor()
try:
    cursor.execute("select * from dbtest1")
    info = cursor.fetchall()
#    info.encode('utf-8')
    for row in info:
        id = row[0]
        name = row[1]
        sex = row[2]
        age = row[3]
        date = row[4]
        print("id=%s,name=%s,sex=%s,age=%d,date=%s" % \
        (id, name, sex, age, date))
except:
    print("No Data!")
db.close()
