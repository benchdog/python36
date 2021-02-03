# __*__ coding: utf-8 __*__

import zipfile

try:
    with zipfile.ZipFile('E:\pythondoc\zip\dic.zip') as zfile:
        zfile.extractall(pwd="123456")
        print("Extract the Zip file successfully!")
except:
    print("Extract the Zip file failed!")