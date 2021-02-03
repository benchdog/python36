# {error_type:[code,msg]}
import re

'''
thumbnail_pcs.go:
1.错误名称：以大小写字母开头，中间可包含下划线
3.errMsg中错误描述：可包含以大小写字母开头，中间可包含空格和英文逗号，全部内容由英文双引号包含,以逗号结尾
eg：API_UNSUPPORTED = pcsError(3) #等号两边至少各一个空格
'''
'''
thumbnail_pcs = {}
pattern1 = re.compile(r'((^[A-Z|a-z][_|A-Z|a-z]*)=====pcsError\(([0-9]*)\))|((^[A-Z|a-z][_|A-Z|a-z]*)=====([a-z|A-Z][a-z|A-Z|\s|,]*?",))')
with open('conf/thumbnail_pcs.go','r',encoding='utf8') as fr1:
    for line1 in fr1:
        line1 = re.sub(r'([\s]*=[\s]*)|(:.*?")', '=====', line1.strip())
        line1 = re.findall(pattern1,line1)
        if line1:
            if line1[0][0]:
                thumbnail_pcs[line1[0][1]] = [line1[0][2]]
            else:
                thumbnail_pcs[line1[0][4]].append(line1[0][5])
    print(thumbnail_pcs)
'''

'''
poms-meta-errors.go：
1.错误名称：大小写字母开头，可包含数字
2.错误代码：数字或减号（'-'）开头，后续只能接数字
3.错误描述（可为空）：大小字母开头，中间可包含数字、空格、下划线、减号、等于号、冒号、逗号、句点、正斜杠，全部内容由英文双引号包含
eg:ErrParamInvalidXService = PomsmetaError{400, -12299, "Invalid param x-service"} #等号两边至少各一个空格
'''
'''
poms_meta_errors = {}
with open('conf/poms-meta-errors.go','r',encoding='utf8') as fr2:
    for line2 in fr2:
        line2 = line2.strip()
        pattern2 = re.compile(r'(^[a-z|A-Z]\w*)\s+=\s+PomsmetaError\{\d+,\s+([-|\d]*),[\s]+"(([\w|\s|-|,|\'|:|=|\.|\/].*)|())"\}')
        line2 = re.findall(pattern2, line2)
        if line2:
            # print(line2[0][0:3])
            poms_meta_errors[line2[0][0]] = line2[0][1:3]
    print(poms_meta_errors)
'''

'''
streaming_error.go：
1.错误名称：以大小写字母开头，包含下划线
2.错误代码：略
3.错误描述：大小写字母开头，包含逗号，全部内容由英文双引号包含，以逗号结尾
eg: ERROR_STREAMING_AUTH_FAILED : "transcoding system erro", #冒号两边空格随意
'''
'''
streaming_error = {}
with open('conf/streaming_error.go','r',encoding='utf8') as fr3:
    for line3 in fr3:
        line3 = line3.strip()
        pattern3 = re.compile(r'(^([A-Z][A-Z|a-z|_]*)\s+=\s+(\d+))|(^([A-Z][A-Z|a-z|_]+)\s*:\s*"([A-Z|a-z|,].*)",)')
        line3 = re.findall(pattern3, line3)
        if line3:
            if line3[0][0]:
                streaming_error[line3[0][1]] = [line3[0][2]]
            else:
                streaming_error[line3[0][4]].append(line3[0][5])
    print(streaming_error)
'''


'''
themis_error.go：
1.错误名称：以大小写字母开头，包含下划线
2.错误代码：略
3.错误描述：大小写字母开头，包含逗号，全部内容由英文双引号包含，以逗号结尾
eg: ERROR_ACCOUNT_NOT_AUTHORIZE: "user is not authorized", #冒号两边空格随意
'''
'''
themis_error = {}
with open('conf/themis_error.go','r',encoding='utf8') as fr4:
    for line4 in fr4:
        line4 = line4.strip()
        pattern4 = re.compile(r'(^([A-Z][A-Z|a-z|_]*)\s+=\s+(\d+))|(^([A-Z][A-Z|a-z|_]+)\s*:\s*"([A-Z|a-z|,].*)",)')
        line4 = re.findall(pattern4, line4)
        if line4:
            if line4[0][0]:
                themis_error[line4[0][1]] = [line4[0][2]]
            else:
                themis_error[line4[0][4]].append(line4[0][5])
    print(themis_error)
'''