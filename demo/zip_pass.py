# -*- coding:utf-8 -*-
import zipfile
from threading import Thread

def extractFile(zfile,password):
    try:
        zfile.extractall(pwd=password)
    except Exception as e:
        pass

def main():
    zfile = zipfile.ZipFile('E:\pythondoc\zip\suo.zip')
    passfile = open('E:\pythondoc\zip\dic.txt')
    for line in passfile.readlines():
        password = line.strip('\n')
        t = Thread(target = execfile,arg = (zfile,password))

if __name__ == '__main__':
    main()