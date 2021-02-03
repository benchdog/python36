# -*- coding: utf-8 -*-

txt_path = r'G:\万方\2020科通数据汇聚\127map.txt'

tables_dict = {}
with open(txt_path, 'r', encoding='utf8') as fr:
    for line in fr.readlines():
        line_list = line.split()
        tables_dict[line_list[0]] = line_list[1]

print(tables_dict)

