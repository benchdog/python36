from xlwt import *
import os

excel_file = Workbook(encoding = 'utf-8')
root_dir='C:/Users/user/Desktop/数据维度字段预调研/to_out'
for dirpath,dirnames,filenames in os.walk(root_dir):
    for filename in filenames:
        sheet = excel_file.add_sheet(filename)
        file=os.path.join(dirpath,filename)
        print(file)
        with open(file,'r',encoding='utf-8')  as fr:
            row = 1
            sheet.write(0, 0, '编号')
            sheet.write(0, 1, '字段编码')
            sheet.write(0, 2, '字段名称')
            for line in fr:
                field=line.strip().split('\t')
                try:
                    sheet.write(row,0,row)
                    sheet.write(row, 1, field[0])
                    sheet.write(row, 2, field[1])
                except Exception as e:
                    print(e)
                finally:
                    row += 1
excel_file.save('stat_res.xls')