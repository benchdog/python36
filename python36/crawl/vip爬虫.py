#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/12 15:55
# @Author  : 善念
# QQ群:790921645
# @File    : vip爬虫.py
# @Software: PyCharm
# pyinstaller -F -w -i
import re
import tkinter as tk
import webbrowser
from tkinter import messagebox

import requests

response = requests.get('http://www.qmaile.com/')

response.encoding=response.apparent_encoding
response=response.text

reg=re.compile('<option value="(.*?)" selected="">')
# *匹配前面出现0次或者无限多次
res=re.findall(reg,response)
one=res[0]
two=res[1]
three=res[2]
four=res[3]
five=res[4]

root = tk.Tk()
root.title('Vip电影播放_学习交流群：790921645')
root.geometry('500x250+100+100')
# 宽*长
l1=tk.Label(root,text='播放接口:',font=("Arial",12),)
# bg='pink'height=3
l1.grid(row=0,column=0)
l2=tk.Label(root,text='播放链接:',font=("Arial",12),)
l2.grid(row=6,column=0)
t1=tk.Entry(root,text='',width=50)
t1.grid(row=6,column=1)

# StringVar是Tk库内部定义的字符串变量类型，在这里用
# 于管理部件上面的字符；不过一般用在按钮button上
# RadioButton控件为用户提供由两个或多个互斥选项组成的选项集。
# 单选按钮
# 当用户选择某单选按钮时，同一组中的其他单选按钮不能同时选定。
# “这里有一组选项，您可以从中选择一个且只能选择一个。
var=tk.StringVar(value=None)
r1=tk.Radiobutton(root,text='播放接口1',variable=var,value=one,)
r1.grid(row=0,column=1,)
var.set(r1)
r2=tk.Radiobutton(root,text='播放接口2',variable=var,value=two,)
r2.grid(row=1,column=1)
r3=tk.Radiobutton(root,text='播放接口3',variable=var,value=three,)
r3.grid(row=2,column=1)
r4=tk.Radiobutton(root,text='播放接口4',variable=var,value=four,)
r4.grid(row=3,column=1)
r5=tk.Radiobutton(root,text='播放接口5',variable=var,value=five,)
r5.grid(row=4,column=1)


def help_menu():
    messagebox.showinfo("帮助信息",message="请把想看的视频链接放到输入框即可！")


def author_info():
    messagebox.showinfo("联系更新",message="Author：善念")


menubar = tk.Menu(root)  # 实例化菜单项
helpmenu = tk.Menu(menubar, tearoff=0)# 在这个菜单上生成子菜单（实例化）
menubar.add_cascade(label='帮助(H)', menu=helpmenu)# 增加一个主菜单选项
helpmenu.add_command(label='帮助文档',command=help_menu)# 把子菜单添加进去
helpmenu.add_command(label='作者信息', command=author_info)
root.config(menu=menubar)# 把菜单配置进去


def play_movie():
    webbrowser.open(var.get()+t1.get())


b1=tk.Button(root,text='播放',font=("Arial",12), width=8,command=play_movie)
b1.grid(row=7,column=1)


def del_text():
    t1.delete(0,'end')


b2=tk.Button(root,text='清除',font=("Arial",12), width=8,command=del_text)
b2.grid(row=8,column=1)

root.mainloop()



