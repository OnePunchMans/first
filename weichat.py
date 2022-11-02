import win32api, win32gui, win32con
import win32clipboard as clipboard
import time
import requests
from apscheduler.schedulers.blocking import BlockingScheduler


###############################
#  微信发送
###############################
def send_m(win):
    # 以下为“CTRL+V”组合键,回车发送，（方法一）
    win32api.keybd_event(17, 0, 0, 0)  # 有效，按下CTRL
    time.sleep(0.1)  # 缓冲时间
    win32gui.SendMessage(win, win32con.WM_KEYDOWN, 86, 0)  # V
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)  # 放开CTRL
    time.sleep(0.1)  # 缓冲时间
    win32gui.SendMessage(win, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)  # 回车发送
    return


def txt_ctrl_v(txt_str):
    # 定义文本信息,将信息缓存入剪贴板
    clipboard.EmptyClipboard()
    clipboard.SetClipboardData(win32con.CF_UNICODETEXT, txt_str)
    clipboard.CloseClipboard()
    return


def m_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def get_window(className, titleName):
    win = win32gui.FindWindow(className, titleName)
    # 窗体前端显示
    # win32gui.SetForegroundWindow(win)
    # 使窗体最大化
    win32gui.ShowWindow(win, win32con.SW_MAXIMIZE)
    print("找到句柄：%x" % win)
    if win != 0:
        left, top, right, bottom = win32gui.GetWindowRect(win)
        print(left, top, right, bottom)  # 最小化为负数
        win32gui.SetForegroundWindow(win)  # 获取控制
        time.sleep(0.5)
    else:
        print('请注意：找不到【%s】这个人（或群），请激活窗口！' % className)
    return win


def day_english():  # 获取金山词霸每日一句
    url = 'http://open.iciba.com/dsapi'
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    return content + note


def sendTaskLog():
    # 查找微信小窗口
    win = get_window('WeChatMainWndForPC', '微信')
    # win = get_window('ChatWnd', '文件传输助手')
    # win = get_window('HwndWrapper[happ.exe;;5833e43c-0218-400c-88a5-4e7056f21a9b]', '同花顺远航版')
    # 读取文本
    # file = open(r'F:\debug.log', mode='r', encoding='UTF-8')
    # str1 = file.read()
    m_click(100, 40)
    time.sleep(0.5)
    txt_ctrl_v('扯犊蛋群')
    send_m(win)
    txt_ctrl_v(day_english())
    send_m(win)


scheduler = BlockingScheduler()
scheduler.add_job(sendTaskLog, 'interval', seconds=3, timezone='Asia/Shanghai')
# scheduler.add_job(sendTaskLog, 'cron',day_of_week='mon-fri', hour=7,minute=31,second='10',misfire_grace_time=30)

scheduler.start()
