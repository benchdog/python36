#!/usr/bin/python3
# -*- coding: utf-8 -*-

import xlrd
import pymysql

conn = pymysql.connect (host="13.32.4.169", port=3306, user = "alpview", passwd = "123456", db = "db1400", charset="utf8")
cursor = conn.cursor()

excel_path= "./dahua.xlsx"
excel_file = xlrd.open_workbook(excel_path)
sheet = excel_file.sheet_by_index(0)

#print(sheet.name)
#print(sheet.row(0))
row_nums=sheet.nrows
col_nums=sheet.ncols
print(row_nums)
print("111111111")


for row in range(1,row_nums):
    #print(type(sheet.row_values(row)))
    #print(sheet.row_values(row))
    #row_values=sheet.row_values(row)
    #sql="insert into ape_test (function_type,ape_id,name,model,ip_addr,ipv6_addr,port,longtitude,latitude,place_code,place,org_code,cap_direction,monitor_direction,monitor_area_desc,is_online,owner_aps_id,user_id,password,data_source) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update ape_id=values(ape_id);"
    sql='insert into ape_test (function_type,ape_id,name,model,ip_addr,ipv6_addr,port,longitude,latitude,place_code,place,org_code,cap_direction,monitor_direction,monitor_area_desc,is_online,owner_aps_id,user_id,password,data_source) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    function_type=str(int(sheet.row_values(row)[1]))
    ape_id=sheet.row_values(row)[2]
    name=sheet.row_values(row)[3]
    model=sheet.row_values(row)[4]
    ip_addr=sheet.row_values(row)[5]
    ipv6_addr=sheet.row_values(row)[6]
    port=sheet.row_values(row)[7]
    longitude=sheet.row_values(row)[8]
    latitude=sheet.row_values(row)[9]
    place_code=sheet.row_values(row)[10]
    place=sheet.row_values(row)[11]
    org_code=sheet.row_values(row)[12]
    try:
        cap_direction=int(sheet.row_values(row)[13])
    except ValueError:
        pass
    finally:
        cap_direction = 0
    try:
        monitor_direction=int(sheet.row_values(row)[14])
    except ValueError:
        pass
    finally:
        monitor_direction = 9
    monitor_area_desc=sheet.row_values(row)[15]
    is_online=int(sheet.row_values(row)[16])
    owner_aps_id=sheet.row_values(row)[17]
    user_id=sheet.row_values(row)[18]
    password=sheet.row_values(row)[19]

    #row_values=[str(int(sheet.row_values(row)[1])),sheet.row_values(row)[2],sheet.row_values(row)[3],sheet.row_values(row)[4],sheet.row_values(row)[5],sheet.row_values(row)[6],sheet.row_values(row)[7],sheet.row_values(row)[8],sheet.row_values(row)[9],sheet.row_values(row)[10],sheet.row_values(row)[11],sheet.row_values(row)[12],sheet.row_values(row)[13],sheet.row_values(row)[14],sheet.row_values(row)[15],int(sheet.row_values(row)[16]),sheet.row_values(row)[17],sheet.row_values(row)[18],sheet.row_values(row)[19],'13012300005030000011']
    row_values=[function_type,ape_id,name,model,ip_addr,ipv6_addr,port,longitude,latitude,place_code,place,org_code,cap_direction,monitor_direction,monitor_area_desc,is_online,owner_aps_id,user_id,password,"13012300005030000011"]
    # print(row_values)
    try:
        res=cursor.execute(sql,row_values)
        conn.commit()
        # print(res)
    except Exception as e:
        conn.rollback()
        print(e)
conn.close()