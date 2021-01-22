#-*- coding:utf-8 -*-

from pynput.mouse import Button, Controller
import time
import win32api
import win32gui
import win32con
import win32process
import os
import signal
import win32api
import time
import aircv
import cv2 #包名叫做opencv-python
from PIL import ImageGrab

# mouse = Controller()
# time.sleep(3)
# print(mouse.position)
# exit



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
        return match_result

img_profile = r'C:\Users\bench\Desktop\ligh\codes\Python\auto\youdao_singin\files\img_profile.png'
img_checkin = r'C:\Users\bench\Desktop\ligh\codes\Python\auto\youdao_singin\files\img_checkin.png'
img_screenshot = r'C:\Users\bench\Desktop\ligh\codes\Python\auto\youdao_singin\files\img_window.png'

app_name = '有道云笔记'
app_class = ''
app_path = r'C:\Program Files (x86)\Youdao\YoudaoNote\YoudaoNote.exe'
while 1:
    if not win32gui.FindWindow(0, app_name):
        print('打开<' + app_name + '>')
        win32api.ShellExecute(1, 'open', app_path, '', '', 3)
        time.sleep(2)

    else:
        print('窗体标题：',win32gui.GetWindowText(win32gui.FindWindow(0, app_name)))  # 窗体标题
        print('窗体类名:',win32gui.GetClassName(win32gui.FindWindow(0, app_name)))  # 窗体类名
        app_handler = win32gui.FindWindow(0, app_name)

        #窗口置顶(两行代码)
        win32api.keybd_event(35, 0, 0, 0)
        win32gui.SetForegroundWindow(app_handler)

        #窗口最大化
        win32gui.ShowWindow(app_handler, win32con.SW_MAXIMIZE)
        break

time.sleep(3)

# 获取鼠标对象
mouse = Controller()

#全屏截图()
screenshot = ImageGrab.grab()
screenshot.save(img_screenshot)
#头像位置
mouse.position = matchImg('头像', img_profile, img_screenshot)

while 1:
    mouse.click(Button.left, 1) #点击头像
    screenshot = ImageGrab.grab()
    screenshot.save(img_screenshot)
    matchres = matchImg('签到', img_checkin, img_screenshot)
    if matchres:
        mouse.position = matchres
        mouse.click(Button.left, 1) #点击签到
        break
time.sleep(2)

# 关闭软件
# 获取线程和进程ID
thread,pid =win32process.GetWindowThreadProcessId(app_handler)
try:
    os.kill(pid,signal.CTRL_C_EVENT)
    os.kill(pid,signal.CTRL_BREAK_EVENT)
except Exception as e:
    pass

#窗口最小化
# win32gui.PostMessage(app_handler, win32con.WM_CLOSE, 0, 0)

'''
# for index in range(0, 100):
#     # 鼠标移动到指定坐标轴
#     mouse.move(index, -index)
#     print(mouse.position)
#     time.sleep(0.01)

# for index in range(0, 100):
#     # 鼠标移动到指定坐标轴
#     mouse.move(-index, index)
#     print(mouse.position)
#     time.sleep(0.01)

# 鼠标右键按下
# mouse.press(Button.right)

# time.sleep(0.01)

# 鼠标右键抬起
# mouse.release(Button.right)

# 鼠标左键点击
# mouse.click(Button.left, 1)

# 鼠标滚轮滚动距离500
# mouse.scroll(0, -500)
'''
