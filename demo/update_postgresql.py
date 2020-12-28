# -*- coding: utf-8 -*-
import psycopg2

path = r'C:\Users\bench\Desktop\ip.txt'
conn = psycopg2.connect(database="xresmgr_xresmgrdb", user="postgres", password="XWqOwIfq", host="13.38.229.116", port="7017")
cursor = conn.cursor()
# cursor.execute("SELECT VERSION()")
# data = cursor.fetchone()
# print(data)

with open(path, 'r', encoding='utf8') as fr:
    for line in fr.readlines():
        line_list = line.split()
        f_ip = line_list[0]
        f_name = line_list[1]
        sql = "update camera set name = '" + f_name + "' where device_name = '" + f_ip + "';"
        # print(sql)

        try:
            cursor.execute(sql)
            print('ok')
        except Exception as e:
            print(e)

conn.commit()
conn.close()