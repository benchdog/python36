import os
import re
import pickle
import json
import yaml

def getallfiles(pathx,pattern):
	# improvements: add ignorecase option for re
	matchedPath = []
	for directory, dirnames,filenames in os.walk(pathx):
		eachDirectoryFiles = [os.path.join(directory,perFile) for perFile
			in filenames if re.search(pattern,perFile)]
		if eachDirectoryFiles:
			matchedPath = matchedPath + eachDirectoryFiles
	return matchedPath

def getfilename(pathx):
	return os.path.splitext(os.path.basename(pathx))[0]


def getParDir(path):
	return os.path.dirname(path)

def loadPkl(path):
	with open(path,'rb') as pf:
		res = pickle.load(pf)
	return res

def dumpPkl(obj,path):
	with open(path,'wb') as pf:
		pickle.dump(obj,pf)

def load(path,fmt=None):
	if fmt:
		fmt = fmt
	else:
		fmt = path.split('.')[-1]
	if fmt == 'pkl':
		with open(path,'rb') as pf:
			res = pickle.load(pf)
		return res
	with open(path,'r') as pf:
		if fmt == 'txt':
			res = pf.read()
		elif fmt == 'json':
			res = json.load(pf)
		elif fmt == 'yaml' or fmt == 'yml':
			res = yaml.load(pf)
	return res

def dump(data_str,path,fmt=None):
	if fmt:
		fmt = fmt
	else:
		fmt = path.split('.')[-1]
	if fmt == 'pkl':
		with open(path,'wb') as pf:
			pickle.dump(data_str,pf)
		return
	with open(path,'w') as pf:
		if fmt == 'txt':
			pf.write(data_str)
		elif fmt == 'json':
			json.dump(data_str,pf)
		elif fmt == 'yaml' or fmt == 'yml':
			yaml.dump(data_str,pf,default_flow_style=False)
		elif fmt =='pkl':
			pickle.dump(data_str,pf)
