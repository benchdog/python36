import time
import subprocess
# import threading
import aircv
import os
import random

device_name = '127.0.0.1:7555'
adb_path = r"C:\Users\bench\Desktop\ligh\codes\Python\auto\zhongqing\tools\platform-tools-win\adb.exe"
img_local=r"C:\Users\bench\Desktop\ligh\codes\Python\auto\zhongqing\files\\"
img_remote='/storage/emulated/0/Pictures/'
img_src=img_local + 'img_readmore.png'

def matchImg(imgtype, imgsrc, imgobj, confidencevalue=0.7):  # imgsrc=原始图像，imgobj=待查找的图片
    imsrc = aircv.imread(imgsrc)
    imobj = aircv.imread(imgobj)
    # find_template(原始图像imsrc，待查找的图片imobj，最低相似度confidence)
    match_result = aircv.find_template(imsrc, imobj, confidencevalue)
    if match_result is not None:
        print(imgtype + '相似度：',match_result['confidence'])
        # match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 1为长，0为宽
        return (match_result['rectangle'][0][0] + imsrc.shape[1]//2, match_result['rectangle'][0][1] + imsrc.shape[0]//2)
    else:
        print(imgtype + '相似度：0')
        return match_result

# 关闭和启动adb服务(MAC版)
# print('1: ' + str(subprocess.getoutput(adb_path + " kill-server")))
# print('2: ' + str(subprocess.getoutput(adb_path + " start-server")))

# 1.连接mumu模拟器(WIN版)
print('连接设备：' + str(subprocess.getoutput(adb_path + " connect " + device_name)))

# 2.监测连接的设备列表
# print('已连接设备名称：' + str(subprocess.getoutput(adb_path + " devices")))
"""
PKT0220320004379	device #安卓手机
127.0.0.1:7555	device #mumu模拟器
emulator-5554	device #雷电模拟器
"""

while True:
    # 进入热点页第一篇文章
    print('点击进入第一篇文章')
    subprocess.getoutput(adb_path + " shell input tap 89 133")
    time.sleep(random.randint(1,2))

    '''
    #下载图片进行比对
    img_dst_name = str(int(time.time())) + ".png"
    img_dst = img_local + img_dst_name
    #手机截屏保存到手机
    print(subprocess.getoutput(adb_path + " shell screencap -p " + img_remote + img_dst_name))
    # print(subprocess.getoutput(adb_path + " exec-out screencap -p > " + img_dst))
    #手机截屏从手机下载到电脑本地
    print(subprocess.getoutput(adb_path + " pull " + img_remote + img_dst_name + " " + img_local))

    #图片比对
    # res_search = img_match(img_src, img_local + img_dst_name)
    res_search = matchImg('阅读更多', img_src, img_dst)
    if res_search:
        #获取"阅读更多"坐标，并点击打开
        subprocess.getoutput(adb_path + " shell input tap " + str(res_search[0]) + " " + str(res_search[1]))
    #删除手机和电脑比对过的图片
    subprocess.getoutput(adb_path + " shell rm " + img_remote + img_dst_name)
    os.remove(img_dst)
    '''

    # 循环滑动阅读文章
    for i in range(random.randint(12,15)):
        # x = str(random.randint(30,100))
        # subprocess.getoutput(adb_path + " shell input swipe " + x + " " + str(random.randint(200,400)) + " " + x + " " + str(random.randint(50,150)) + " "  + str(random.randint(1000,2000)))
        subprocess.getoutput(adb_path + " shell input swipe 300 200 40 300 2000")

    # 返回热点页
    print('返回热点页')
    subprocess.getoutput(adb_path + " shell input keyevent BACK")
    # time.sleep(0.5)
    # 刷新热点页
    print('刷新热点页')
    subprocess.getoutput(adb_path + " shell input swipe 30 200 30 1000 " + str(random.randint(500,700)))
    time.sleep(random.uniform(2.5,3))





# 5.指定设备，并发发送指令循环执行。
# while True:
#     subprocess.getoutput(f"{adb_path} -s emulator-5554 shell input swipe 311 952 622 444 400")
#     time.sleep(1)
#     subprocess.getoutput(f"{adb_path} -s emulator-5554 shell input tap 1090 992")


# 6.其他更多指令
"""
其他更多指令：
    - 查看手机设备：adb devices
    - 查看设备型号：adb shell getprop ro.product.model
    - 查看电池信息：adb shell dumpsys battery
    - 查看设备ID：adb shell settings get secure android_id
    - 查看设备IMEI：adb shell dumpsys iphonesubinfo
    - 查看Android版本：adb shell getprop ro.build.version.release
    - 查看手机网络信息：adb shell ifconfig
    - 查看设备日志：adb logcat
    - 重启手机设备：adb reboot
    - 安装一个apk：adb install /path/demo.apk
    - 卸载一个apk：adb uninstall <package>
    - 查看系统运行进程：adb shell ps
    - 查看系统磁盘情况：adb shell ls /path/
    - 手机设备截屏：adb shell screencap -p /sdcard/aa.png
    - 手机文件下载到电脑：adb pull /sdcard/aa.png ./
    - 电脑文件上传到手机：adb push aa.png /data/local/
    - 手机设备录像：adb shell screenrecord /sdcard/ab.mp4
    - 手机屏幕分辨率：adb shell wm size
    - 手机屏幕密度：adb shell wm density
    - 手机屏幕点击：adb shell input tap xvalue yvalue
    - 手机屏幕滑动：adb shell input swipe 1000 1500 200 200
    - 手机屏幕带时间滑动：adb shell input swipe 1000 1500 0 0 1000
    - 手机文本输入：adb shell input text xxxxx
    - 手机键盘事件：adb shell input keyevent xx
"""
