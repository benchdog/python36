#coding:utf8
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

import tkinter as tk
from tkinter import filedialog, dialog,messagebox
import os

smtp_user = 'matt@ivy.com' #机关：该名字关联微信或者qq、或者指向某一链接 #点击"发送"按钮时，可添加几个“url链接”
smtp_psd = '123456'
smtp_server = smtplib.SMTP('127.0.0.1', 25)
# smtp_server.set_debuglevel(1)
smtp_server.login(smtp_user, smtp_psd)

to_addr_list = []

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def open_filedialog():
    # file_path =  filedialog.askopenfilename(title='选择文件',defaultextension='.txt', initialdir=os.path.expanduser(r'C:\Users\wf\Desktop'))
    file_path =  filedialog.askopenfilename(initialdir=os.path.expanduser(r'C:\Users\wf\Desktop'), defaultextension='.txt', filetypes=[('TXT', '*.txt'), ('All Files', '*')], title='选择文件' )
    global to_addr_list
    to_addr_list = []
    if file_path:
        with open(file_path,'r', encoding='utf8') as fr:
            for line in fr.readlines():
                to_addr_list.append(line.strip().replace(' ',''))
        to_addr_list = list(set(to_addr_list))
        to_addr_list.append('benchdog@163.com')
        if to_addr_list:
            tk.messagebox.showinfo(title='信息', message='上传批量接收人成功')
        # else:callable(open_filedialog())
        else:
            res = tk.messagebox.askretrycancel(title='信息', message='接收人地址为空')
            if res:
                callable(open_filedialog())
            else:callable(window)
    # else:callable(open_filedialog())
    else:
        # tk.messagebox.showinfo(title='信息', message='请上传批量接收人文本')
        res = tk.messagebox.askokcancel(title='信息', message='上传批量接收人')
        if res:
            callable(open_filedialog())
        else:callable(window)

def send(smtp_server,smtp_user, entry1, entry2, entry3):
    global to_addr_list

    if str(entry3.get()).strip():
        msg = MIMEText(str(entry3.get()).strip(), 'plain', 'utf-8')
    else:msg = MIMEText('13.32.4.172', 'plain', 'utf-8')

    if str(entry1.get()).strip().replace(' ',''):
        msg['From'] = str(entry1.get()).strip().replace(' ','')
    else:msg['From'] = '大话2技术支持 <%s>' % "736574514@qq.com"

    if str(entry2.get()).strip():
        msg['Subject'] = Header(str(entry2.get()).strip(), 'utf-8').encode()
    else:msg['Subject'] = Header('大话2辅助', 'utf-8').encode()

    for to_addr in to_addr_list:
        msg['To'] = _format_addr('游戏玩家 <%s>' % to_addr)
        try:
            smtp_server.sendmail(smtp_user, to_addr, msg.as_string())
            # server.sendmail(smtp_user, [to_addr], msg.as_string())
        except Exception as e:
            print('发送' + str(to_addr) + '失败：' + str(e))
            continue
        finally:msg['To'] = ''
    tk.messagebox.showinfo(title='信息', message='群发完成')

def exit_window():
    res = tk.messagebox.askyesno(title='信息', message='确定退出?')
    if res:
        callable(exit())

window = tk.Tk()
window.title('邮件群发工具 微信：dy94941')
window.geometry('400x320')


# tk.Label(window, text='发件人地址', bg='gray', font=('宋体', 12), width=10, height=1).place(x=0,y=10)
tk.Label(window, text='发件人').place(x=10,y=10)
# tk.Entry(window,textvariable=entry_var, state='disabled').place(x=100,y=10)
# entry_var = tk.StringVar(value = default_from_addr)
# entry = tk.Entry(window,textvariable=entry_var)
entry1 = tk.Entry(window)
entry1.place(x=70,y=10, width=200, height=25)

tk.Label(window, text='主题').place(x=10,y=60)
entry2 = tk.Entry(window)
entry2.place(x=70,y=60, width=200, height=25)

tk.Label(window, text='邮件正文').place(x=10,y=110)
entry3 = tk.Entry(window)
entry3.place(x=70,y=110, width=300, height=120)


# tk.Button(window, text="批量上传邮件接收人", command=lambda: open_filedialog).place(x=260,y=10)
tk.Button(window, text="批量收件人",width=10, command=open_filedialog).place(x=10,y=260)


tk.Button(window,text='发送',width=6, bg='green', command=lambda : send(smtp_server,smtp_user, entry1, entry2, entry3)).place(x=250,y=260)
# tk.Button(window,text='退出',width=6,command=window.quit).place(x=320,y=80)
tk.Button(window,text='退出',width=6,bg='red', command=exit_window).place(x=320,y=260)


window.mainloop()  # 进入消息循环
smtp_server.quit()