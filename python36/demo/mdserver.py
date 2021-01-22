#!/bin/env python
# -*- coding: utf_8 -*-
import os
import sys
import time
import commands
import copy
import pdb

IMOS_Config_Path='/usr/local/imosconfig'
IMOSROOT='/usr/local/svconfig'
LOG_Root_Path='/var/log/imoslog'
Script_Root_Path='/usr/local/sbin/services'
SepLen = 50
PdtList = []

def SyncOutput(info, NewLine):
	if True == NewLine:
		print info
	else:
		print info,
	sys.stdout.flush()

def ShellCmd(cmd):
	#return os.system(cmd)
	(status, output) = commands.getstatusoutput(cmd)
	return status, output
	
def WriteLog(log):
	f = open(logfile, 'a')
	f.write(log)
	f.close

def GetPdts():
	pdts_ = []
	pdts_inner = os.listdir(Script_Root_Path)
	if 'vm' in pdts_inner:
		pdts_inner.remove('vm')
		pdts_inner.insert(0,'vm')
	for pdt in pdts_inner:
		pdts_.append(ClassProduct(pdt))
	return pdts_

def ProcessStatus(pname):
	cmd = 'pidof ' + pname
	(status, output) = ShellCmd(cmd)
	if ''==output:
		return False
	else:
		return True
	
#服务类，对应一个产品中的一个进程
class ClassService:
	def __init__(self, pdtname, service_script_name, enable_flag = True):
		self.name = service_script_name.split('.')[0]
		
		self.script_name = service_script_name
		
		self.enable = enable_flag
		
		if 'sh' == service_script_name.split('.')[1]:
			self.level = 'default'
		else:
			self.level = service_script_name.split('.')[1]

#产品类，服务的管理操作均在此类中实现
class ClassProduct:
	def __init__(self, pdtname):
			self.name = pdtname
			try:
				self.VerInfos = self.GetVerInfos(pdtname)
				self.Enable_Services, self.Service_info_dict = self.GetServices()
				self.DaemonTemp = []
				self.GenerateDaemonCfg()
			except:
				pass
	def Usage(self):
		cmd = self.VerInfos['Name'].lower() + 'server.py'
		format = '%s\n         %s\n'
		print format % (cmd + ' start', '--- Start my own serivces')
		print format % (cmd + ' stop', '--- Stop my own serivces')
		print format % (cmd + ' restart', '--- Restart my own serivces')
		print format % (cmd + ' status', '--- Display my own services\' status')
		print format % (cmd + ' version', '--- Display my version')
		print format % (cmd + ' startall', '--- Start all servers\' serivces')
		print format % (cmd + ' stopall', '--- Stop all servers\' serivces')
		print format % (cmd + ' restartall', '--- Restart  all servers\' serivces')
		print format % (cmd + ' allstatus', '--- Display all servers\' status')
		print format % (cmd + ' allversion', '--- Display all servers\' version')
		print format % (cmd + ' service-list', '--- List my own services')
		print format % (cmd + ' ServiceName enable', '--- Enable service')
		print format % (cmd + ' ServiceName disable', '--- Disable service')
		print format % (cmd + ' ServiceName start/stop/restart', '--- Start/Stop/Restart a single service')

	#Get informations from product abbr. such as 'VM' 'ms' 'Dm'
	def GetVerInfos(self,pdtname):
		try:
			info_dict={}
			info_dict['Name'] = pdtname.upper()
			f_path=IMOS_Config_Path + '/' + info_dict['Name'].lower() + 'conf/' + info_dict['Name'].lower() + 'sys.conf'
			f = open(f_path, 'r')
			configs=f.readlines()
			f.close()
			for config in configs:
				try:
					info_dict[config.split('=')[0]] = config.split('=')[1].replace('\n','')
				except:
					continue
			info_dict['Version_V'] = info_dict['HCVERI'].split('.')[0][0] + '00'
			info_dict['Version_R'] = "%03d" % int(info_dict['HCVERI'].split('.')[0][1])
			
			info_dict['Version_B'] = "%02d" % int(info_dict['HCVERI'].split('.')[1])
			info_dict['Version_D'] = "%03d" % int(info_dict['HCVERI'].split('.')[2])
			info_dict['Version_PATCH'] = info_dict['HCVERI'].split('.')[3]
			info_dict['Serial']=info_dict['HCVERO'].split('-')[0].replace(info_dict['Name'], '',1)
			info_dict['FullName'] = info_dict['HCVERO'].split('-')[0]
			info_dict['PublishVersion'] = info_dict['HCVERO'].split('-')[2]
			return info_dict
		except Exception, e:
			return info_dict
			
	def GetServices(self):
		try:
			Services_inner=[]
			Services_inner_reverse=[]
			Enable_Services_list=[]
			Service_info_dict_inner={}
			
			#scan enabled services
			files = os.listdir(Script_Root_Path + '/' + self.VerInfos['Name'].lower())
			for file in files:
				if os.path.isdir(Script_Root_Path + '/' + self.VerInfos['Name'].lower() + '/' + file):
					continue
				
				script_name = file
				if '.sh' not in script_name:
					continue
				service = ClassService(self.name, script_name, True)
				if 'default' == service.level:
					while True:
						try:
							Services_inner[0].append(service)
							Service_info_dict_inner[service.name] = service
							break
						except IndexError:
							Services_inner.append([])
				else:
					if -1 == service.level.find('r'):
						while True:
							try:
								Services_inner[int(service.level)].append(service)
								Service_info_dict_inner[service.name] = service
								break
							except IndexError:
								Services_inner.append([])
								
					else:
						while True:
							try:
								Services_inner_reverse[int(service.level.replace('r',''))].append(service)
								Service_info_dict_inner[service.name] = service
								break
							except IndexError:
								Services_inner_reverse.append([])
	
			#scan disabled services
			files = os.listdir(Script_Root_Path + '/' + self.VerInfos['Name'].lower() + '/disabled')
			for file in files:
				if os.path.isdir(Script_Root_Path + '/' + self.VerInfos['Name'].lower() + '/disabled/' + file):
					continue
				
				script_name = file
				if '.sh' not in script_name:
					continue
				service = ClassService(self.name, script_name, False)
				Service_info_dict_inner[service.name] = service
			
			#Sort service by level
			for index in range(1, len(Services_inner)):
				if 0 != len(Services_inner[index]):
					for index_2 in range(0, len(Services_inner[index])):
						Enable_Services_list.append(Services_inner[index][index_2])
					
			for index_3 in range(0, len(Services_inner[0])):
				Enable_Services_list.append(Services_inner[0][index_3])
				
			for index in range(len(Services_inner_reverse) - 1, -1, -1):
				if 0 != len(Services_inner_reverse[index]):
					for index_2 in range(0, len(Services_inner_reverse[index])):
						Enable_Services_list.append(Services_inner_reverse[index][index_2])
			
			return Enable_Services_list, Service_info_dict_inner
		except Exception, e:
			pass

	def SkipIt(self, servicename):
		for pdt in PdtList:
			if pdt.name.lower() == self.name.lower():
				continue
			else:
				try:
					for service in pdt.Enable_Services:
						if servicename.lower() == service.name.lower() and ProcessStatus(pdt.name.lower() + 'daemon'):
							return True
				except:
					continue
		return False

	def start(self):
		try:
			mylen = SepLen - len('START ' + self.VerInfos['FullName']) - 2
			if mylen % 2 != 0:
				print '%s%s%s' % ('='*(mylen/2) + ' ', 'START ' + self.VerInfos['FullName'], ' ' + '='*(mylen/2 + 1))
			else:
				print '%s%s%s' % ('='*(mylen/2) + ' ', 'START ' + self.VerInfos['FullName'], ' ' + '='*(mylen/2))
		except Exception, e:
			WriteLog(str(e))
		format = '%%-%ds' % (SepLen - 14)
		for index in range(0, len(self.Enable_Services)):
			SyncOutput( format % ('Start service[' + self.Enable_Services[index].name + ']'),False)
			(status, output) = ShellCmd('sh ' + Script_Root_Path + '/' + self.VerInfos['Name'].lower() + '/'+ self.Enable_Services[index].script_name + ' start >/dev/null 2>&1')
			if 0 == status:
				SyncOutput('\33[32m\33[1m[ Succeeded ]\33[0m',True)
			elif 512 == status:
				SyncOutput('\33[32m\33[1m[  Running  ]\33[0m',True)
			elif 256 == status:
				SyncOutput('\33[31m\33[1m\33[5m[  Failed!  ]\33[0m', True)
			else:
				SyncOutput('\33[31m\33[1m\33[5m[ Unknow error:'+ str(status) + ' ]\33[0m', True)
			
	def status(self):
		try:
			mylen = SepLen - len(self.VerInfos['FullName']+ ' STATUS') - 2
			if mylen % 2 != 0:
				print '%s%s%s' % ('='*(mylen/2) + ' ', self.VerInfos['FullName'] + ' STATUS', ' ' + '='*(mylen/2 + 1))
			else:
				print '%s%s%s' % ('='*(mylen/2) + ' ', self.VerInfos['FullName'] + ' STATUS', ' ' + '='*(mylen/2))
		except Exception, e:
			WriteLog(str(e))
		format = '%%-%ds' % (SepLen - 12)
		for index in range(0, len(self.Enable_Services)):
			SyncOutput(format % ('Service[' + self.Enable_Services[index].name + ']'), False)
			(status, output) = ShellCmd(Script_Root_Path + '/' + self.VerInfos['Name'].lower() + '/'+ self.Enable_Services[index].script_name + ' status >> ' + '/dev/null 2>&1')
			if 256 == status:
				SyncOutput('\33[32m\33[1m[ Running ]\33[0m', True)
			elif 0 == status:
				SyncOutput('\33[31m\33[1m\33[5m[ Stopped ]\33[0m', True)
			else:
				SyncOutput('\33[31m\33[1m\33[5m[ Unknow error:'+ str(status) + ' ]\33[0m', True)
			
	def stop(self, op=''):
		try:
			mylen = SepLen - len('STOP ' + self.VerInfos['FullName']) - 2
			if mylen % 2 != 0:
				print '%s%s%s' % ('='*(mylen/2) + ' ', 'STOP ' + self.VerInfos['FullName'], ' ' + '='*(mylen/2 + 1))
			else:
				print '%s%s%s' % ('='*(mylen/2) + ' ', 'STOP ' + self.VerInfos['FullName'], ' ' + '='*(mylen/2))
		except Exception, e:
			WriteLog(str(e))
		format = '%%-%ds' % (SepLen - 14)
		for index in range(len(self.Enable_Services) - 1, -1, -1):
			if 'httpd' == self.Enable_Services[index].name:
				if 'NotHttpd' == op:
					continue
			#check public processes and skip it when other pdt which shares public processes is running
			if self.SkipIt(self.Enable_Services[index].name):
				continue
			SyncOutput( format % ('Stop service[' + self.Enable_Services[index].name + ']'),False)
			(status, output) = ShellCmd(Script_Root_Path + '/' + self.VerInfos['Name'].lower() + '/'+ self.Enable_Services[index].script_name + ' stop >/dev/null 2>&1')
			if 0 == status:
				SyncOutput('\33[32m\33[1m[ Succeeded ]\33[0m',True)
			elif 512 == status:
				SyncOutput('\33[32m\33[1m[  Stopped  ]\33[0m',True)
			elif 256 == status:
				SyncOutput('\33[31m\33[1m\33[5m[  Failed!  ]\33[0m', True)
			else:
				SyncOutput('\33[31m\33[1m\33[5m[ Unknow error:'+ str(status) + ' ]\33[0m', True)
			
	def restart(self):
		self.stop()
		time.sleep(1)
		self.start()		

	def restart_ByUI(self):
		self.stop('NotHttpd')
		time.sleep(1)
		self.start()

	def stop_ByUI(self):
		self.stop('NotHttpd')
		
	def ReadDaemonTemp(self):
		daemon_config_template_file = IMOSROOT + '/' + self.name.lower() + 'conf/' + self.name.lower() + '_daemon.cfg.template'
		try:
			template = {}
			f = open(daemon_config_template_file, 'r')
			lines = f.readlines()
			f.close()
			
			key = ''
			Catch_One = False
			for line in lines:
				line=line.replace('\n','')
				if True == Catch_One:
					Catch_One = False
					key = line
					template[key] = ''
			
				if '#GORGEOUS MARK' == line:
					Catch_One = True
					continue
					
				if '' == key:
					continue
				else:
					line += '\n'
					template[key] += line
					
			return template
			
		except Exception, e:
			print e
			
	def RefreshDaemonConfig(self):
		self.DaemonTemp = self.ReadDaemonTemp()
		conf_file = IMOSROOT + '/' + self.name.lower() + 'conf/' + self.name.lower() + '_daemon.cfg'
		try:
			lines = []
			for service in self.Enable_Services:
				if service.name == 'postgresql':
					ServiceName = 'postmaster'
				elif 'daemon' in service.name:
					continue
				else:
					ServiceName = service.name
					
				
				try:
					lines.append(self.DaemonTemp[ServiceName])
				except :
					print '\33[31mERROR: No daemon template for ' + ServiceName[:-1] + '!\33[0m'
					exit()
			f = open(conf_file, 'w')
			f.writelines(lines)
			f.close()
			
		except Exception, e:
			print e
			exit()
			
	def GenerateDaemonCfg(self):
		daemon_config_file = IMOSROOT + '/' + self.name.lower() + 'conf/' + self.name.lower() + '_daemon.cfg'
		if os.path.exists(daemon_config_file):
			return
		else:
			self.RefreshDaemonConfig()

	def startall(self):
		for pdt in PdtList:
			os.system(Script_Root_Path + '/../' + pdt.name.lower() + 'server.py start')
			
	def stopall(self):
		pdts_r = PdtList[:]
		pdts_r.reverse()
		for pdt in pdts_r:
			os.system(Script_Root_Path + '/../' + pdt.name.lower() + 'server.py stop')
	def stopall_ByUI(self):
		pdts_r = PdtList[:]
		pdts_r.reverse()
		for pdt in pdts_r:
			os.system(Script_Root_Path + '/../' + pdt.name.lower() + 'server.py stop_ByUI')
	
	def restartall(self):
		self.stopall()
		time.sleep(1)
		self.startall()
		
	def allstatus(self):
		for pdt in PdtList:
			os.system(Script_Root_Path + '/../' + pdt.name.lower() + 'server.py status')
			
	def info(self, info_name=''):
		for key, value in self.VerInfos.items():
			print key + ': ' + value
	
	def printServices(self):
		line = '+============================+========+========+\n'
		format = '%s%s%-28s%s%8s%s%8s%s'
		print format % (line, '|' , 'ServiceName', '|' , 'Level' , '|', 'Enable', '|')
		for key in self.Service_info_dict:
			print format % (line, '|' , self.Service_info_dict[key].name, '|' , self.Service_info_dict[key].level, '|', self.Service_info_dict[key].enable,'|')
		print line
	
	#do a single service
	def do_single(self, service, action):
		if 'enable' == action or 'disable' == action:
			if ProcessStatus(self.name.lower() + 'daemon'):
				print 'Could\'t load or unload module when ' + self.name.upper() + ' is running, please stop it first!'
				return
		try:
			if service not in self.Service_info_dict:
				raise Exception
			
			if 'restart' == action:
				cmd = Script_Root_Path + '/' + self.name + '/' + self.Service_info_dict[service].script_name + ' stop'
				os.system(cmd)
				time.sleep(0.5)
				cmd = Script_Root_Path + '/' + self.name + '/' + self.Service_info_dict[service].script_name + ' start'
				os.system(cmd)
				
			elif 'enable' == action:
				#pdb.set_trace()
				if os.path.exists(Script_Root_Path + '/' + self.name + '/' + self.Service_info_dict[service].script_name):
					print service + ' is already enabled'
					exit()
				else:
					if not os.path.exists(Script_Root_Path + '/' + self.name + '/disabled/' + self.Service_info_dict[service].script_name):
						print 'missing script: ' + self.Service_info_dict[service].script_name
						exit()
			
					cmd = 'mv -f ' + Script_Root_Path + '/' + self.name + '/disabled/' + self.Service_info_dict[service].script_name + ' ' + Script_Root_Path + '/' + self.name + '/'
					os.system(cmd)
					self.Enable_Services.append(self.Service_info_dict[service])
					self.RefreshDaemonConfig()
					cmd = Script_Root_Path + '/' + self.name + '/' + self.Service_info_dict[service].script_name + ' enable > /dev/null 2>&1'
					os.system(cmd)
					
					print 'Success to enable ' + service
					pdtname = self.name
					try:
						pdtname = self.VerInfos['FullName']
					except:
						pass
			
			elif 'disable' == action:
				if not os.path.exists(Script_Root_Path + '/' + self.name + '/' + self.Service_info_dict[service].script_name):
					print service + ' is already disabled'
					if not os.path.exists(Script_Root_Path + '/' + self.name + '/disabled/' + self.Service_info_dict[service].script_name):
						print 'But, We lost script: ' + self.Service_info_dict[service].script_name
					exit()
			
				else:
					cmd = 'mv -f ' + Script_Root_Path + '/' + self.name + '/' + self.Service_info_dict[service].script_name + ' ' + Script_Root_Path + '/' + self.name + '/disabled/'
					os.system(cmd)
					self.Enable_Services.remove(self.Service_info_dict[service])
					self.RefreshDaemonConfig()
					cmd = Script_Root_Path + '/' + self.name + '/disabled/' + self.Service_info_dict[service].script_name + ' disable > /dev/null 2>&1'
					os.system(cmd)
					
					print 'Success to disable ' + service
					pdtname = self.name
					try:
						pdtname = self.VerInfos['FullName']
					except:
						pass
			else:
				if self.Service_info_dict[service] in self.Enable_Services:
					cmd = self.Service_info_dict[service].script_name + ' ' + action
					os.system(Script_Root_Path + '/' + self.name + '/' + cmd)
				else:
					print self.Service_info_dict[service].name + ' is disabled!'
		except Exception ,e:
			print 'unrecognized service: ' + service
			print e
			exit()
			
	def printVersion(self):
		try:
			if '0' == self.VerInfos['Version_PATCH']:
				patch_inner=''
			else:
				patch_inner='SP' + self.VerInfos['Version_PATCH']
			print ('%-16s' % 'Interior version') + ':' + self.VerInfos['HCVERM']
			print ('%-16s' % 'Exterior version') + ':' + self.VerInfos['HCVERO']
			print ('%-16s' % 'BUILDTIME')+ ':' + self.VerInfos['BUILDTIME'].replace('@',' ')
		except Exception, e:
			print e
			exit()
	def printAllVersion(self):
		for pdt in PdtList:
			os.system(Script_Root_Path + '/../' + pdt.name.lower() + 'server.py version')
			print ''

#Entrance 执行入口#
ScriptName = sys.argv[0].split('/')[-1]
logfile = LOG_Root_Path + '/' + ScriptName + '.log'
os.system("mkdir -p " + LOG_Root_Path)

#根据脚本名称创建一个产品类(ClassProduct)的实例
pdt = ClassProduct(ScriptName.split('server')[0].lower())

#获取合一安装的其他产品（从目录Script_Root_Path中读取其他产品列表）
PdtList = GetPdts()

if 3 == len(sys.argv):
	Action = sys.argv[2]
	service = sys.argv[1]
	pdt.do_single(service, Action)
elif 2 == len(sys.argv):
	Action = sys.argv[1]
	if 'start' == Action:
		pdt.start()
	elif 'stop' == Action:
		pdt.stop()
	elif 'restart' == Action:
		pdt.restart()
	elif 'restart_ByUI' == Action:
		pdt.restart_ByUI()
	elif 'stop_ByUI' == Action:
		pdt.stop_ByUI()
	elif 'status' == Action:
		pdt.status()
	elif 'startall' == Action:
		pdt.startall()
	elif 'stopall' == Action:
		pdt.stopall()
	elif 'stopall_ByUI' == Action:
		pdt.stopall_ByUI()
	elif 'restartall' == Action:
		pdt.restartall()
	elif 'allstatus' == Action:
		pdt.allstatus()
	elif 'info' == Action:
		pdt.info()
	elif 'service-list' == Action:
		pdt.printServices()
	elif 'version' == Action:
		pdt.printVersion()
	elif 'allversion' == Action:
		pdt.printAllVersion()
	else:
		pdt.Usage()
else:
	pdt.Usage()