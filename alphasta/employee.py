import sys #导入sys模块
import time #导入time模块　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　

dic_account = {}
normoal_file = "whitelist" #白名单文件，存放用户名与密码的本地文件
lock_file = "lock"  #黑名单
with open(normoal_file) as norm_f: #打开文件
    for line in norm_f.readlines(): #for循环，一次性读取所有行
        usr,pawd = line.strip().split()
        dic_usr_pawd = {usr:pawd}
        dic_account.update(dic_usr_pawd)

def deny_accout(usrname):
    print('\033[1;31;40m')  # 下一目标输出背景为黑色，颜色红色高亮显示
    print('*' * 50)
    print('\033[7;31m错误次数超限，用户已被永久锁定，请联系管理员！\033[1;31;40m')  # 字体颜色红色反白处理
    print('*' * 50)
    print('\033[0m')
    with open(lock_file,'a') as deny_f:
        deny_f.write('\n')
        deny_f.write(usrname)

def main():
    NumOfInput = 0
    SetTo = 'whole'
    while SetTo == 'whole':
        usrname = input('\033[1;32m请输入您的用户名:\033[0m')
        if list(dic_account.keys()).count(usrname) == 0:
            if len(usrname.strip()) == 0:
                print('\033[1;31m用户名不能为空，请重新输入')
                continue
            else:
                with open(lock_file) as lock_f:
                    for line in lock_f.readlines():
                        if usrname == line.strip():
                            sys.exit('WA_SOURCE_0090_1[1;32m用户%s已锁定，请联系管理员。\033[0m' % usrname)
                usr_list = []
                u_list = usr_list.append(usrname)
                redo_num = usr_list.count(usrname)
                if NumOfInput < 5:
                    NumOfInput += 1
                    if redo_num < 3:
                        print("\033[1;31m出错了，用户名：%s没有找到，请重新输入：" % usrname)
                    else:
                        deny_accout(usrname)
                else:
                    print('\033[1;33m用户名错误次数超限，请3秒钟后再试')
                    print('1s。。。。。')
                    time.sleep(1)
                    print('2s。。。。。')
                    time.sleep(1)
                    print('3s。。。。。')
                    time.sleep(1)
        else:
            NumOfInput = 0
            while NumOfInput < 3:
                passwd = input('\033[1;32m请输入用户%s密码：\033[0m' % usrname)
                if passwd == str(dic_account[usrname]):
                    print('\033[1;36m登陆成功。您的所有操作有可能会被记录！')
                    SetTo = 'q'
                    break
                if len(passwd.strip()) == 0:
                    print('\033[1;33m密码不能为空，请重新输入,您还有%d次机会。'% (2-NumOfInput))
                    NumOfInput += 1
                else:
                    print('\033[1;33m密码错误，请重新输入，您还有%d次机会。'% (2-NumOfInput))
                    NumOfInput += 1
            else:
                print('\033[1;31m输入次数超限，请3s后再试')
                time.sleep(3)
    if SetTo == 'q':
        # print("\033[7;47mEnter 'q': quit                               'b':back       " )
        while True:
            match_yes = 0
            InfoOfEmTab_file = open("../files/employee_info", 'r', encoding='utf-8')
            sch_input = input("\033[1;34;42mPlease enter what the information you need to search: ")
            while True:
                line = InfoOfEmTab_file.readline()
                if len(line) == 0:
                    break
                if sch_input.strip() in line:
                    if sch_input.strip() == '':
                        # print("\033[1;31mThere was no character input, please check if the input was corrected!\n ")
                        match_yes = 1
                    else:
                        print("\033[1;31mMarch Item: \033[1;36m%s" % line)
                        match_yes = 2
            if match_yes == 0:
                print("\033[1;31mNo match items had found!Please check it and try again.\n")
            if match_yes == 1:
                print("\033[1;31mThere was no character input, please check if the input was corrected!\n ")
if __name__ == '__main__':
    main()