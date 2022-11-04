from mimetypes import init
from signal import signal
import sys
import tkinter
import cv2
import time
import serial as sl
import threading
import usbdebug2 as ub
import platform
import json
from PIL import Image


class Model():
    def mouse_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.exit_app()
            print('dbClick')

        if event != 0:
            print()

    def __init__(self):

        # 設定ファイルの読み込み
        json_open = open('./settings.json', 'r')
        self.config = json.load(json_open)

        # 画面の大きさを取得tkinter使用
        tk = tkinter.Tk()
        self.gwidth = tk.winfo_screenwidth()
        self.gheight = tk.winfo_screenheight()
        tk.destroy()
        # 変数設定

        # jsonファイルより
        self.cap = cv2.VideoCapture(r'./video/' + self.config['videofile'])
        self.startframe = self.config['startframe']  # 動画の再生位置
        self.starthand = self.config['starthand']  # ハンドの起動位置
        self.startstop = self.config['startstop']  # 動画停止タイミング
        self.speed = self.config['speed']  # 大きいほど早い　1を基準に100分率
        self.retunstarttime = self.config['retunstarttime']  # 秒数
        self.retrunsignal = self.config['retrunendtime']  # 秒+　-

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.starttime = 0
        self.stoptime = 3  # 最初の待機時間
        self.stoptime2 = 3  # 動画停止後の待機時間
        self.signal = 0  # 512
        self.sec = 0  # セクション０待機中　1計測中　２計測終了
        self.inputf = False  # 入力受付 True #処理終了False
        self.play = False
        self.exit = False

        self.init2()

    def init2(self):

        # osの判別　Linux'＝>thinkerbord Darwin=>mac 'Windows
        os = platform.system()
        if os == 'Linux' or os == 'Windows':
            cv2.namedWindow("MATLAB", cv2.WINDOW_NORMAL)
            cv2.setMouseCallback('MATLAB', self.mouse_click)
            cv2.moveWindow("MATLAB", 0, 0)
            cv2.setWindowProperty(
                "MATLAB", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # 接続機器の確認画面
        self.c = 0
        img = cv2.imread('./sec0.jpg')
        img_resize = cv2.resize(img, dsize=(self.gwidth, self.gheight))
        cv2.imshow("MATLAB", img_resize)
        cv2.setMouseCallback('MATLAB', self.mouse_click)

        # 接続機器が接続されるまで待機
        res = 0
        while True:
            key = cv2.waitKey(1)
            if res == 1:
                cv2.destroyAllWindows()
                break
            if key != -1:
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                sys.exit()
                break
            res = self.init_com()

        # マルチスレッドthread1シリアル信号を受け続ける
        # serial_brain->MATLABからの信号
        # serial_NANO->アルデューノからの信号
        thread1 = threading.Thread(target=self.thread1)
        thread1.start()
        time.sleep(2)
        # 動画を開始タイミングまで戻す
        self.reset()
        # 計測開始sec_0へ
        self.sec_0()
        thread1.join()
        if self.signal != '9':
            self.init2()

    def init_com(self):
        os = platform.system()  # Windows Darwin Linux
        if os == 'Darwin':
            self.comb = '/dev/tty.usbmodem537E0144721'
            # M5
            #self.comm5     = '/dev/tty.usbmodem54240333141'
            # nano
            self.comnano = '/dev/tty.usbserial-0001'
        if os == 'Linux':
            self.comb = '/dev/ttyS0'  # ub.port_p('1.3')
            # nano
            self.comnano = ub.port_p('1.2')
        if os == 'Windows':
            self.comb = 'COM7'
            self.comnano = 'COM6'

        try:
            self.serial_brain = sl.Serial(
                self.comb, 9600, timeout=0)
            self.serial_NANO = sl.Serial(
                self.comnano, 9600, timeout=0)
        except:
            return 0
        return 1

    def reset(self):
        self.starttime = 0
        self.frames = None
        self.sec = 0
        self.inputf = False

    def thread1(self):
        while True:
            # if self.signal=='9':
            #    return
            t1 = time.time()
            line = None
            if(self.serial_brain.is_open):
                line = self.serial_brain.readline()
                line = line.strip().decode('utf-8')
                if line != '':
                    print(line)
                    self.signal = line
            else:
                print('NG')
                return
            line2 = None
            if(self.serial_NANO.is_open):
                line2 = self.serial_NANO.readline()
                line2 = line2.strip().decode('utf-8')
                if line2 != '':
                    print(line2)
                    self.signal = line2

            else:
                print('NG_m5')
                return
            time.sleep(1 / 100)

    def sec_0(self):
        # 動画を開始タイミングまで戻すかぶってる
        self.reset()
        # 3秒空白を入れる　ここはいらないといわれている
        #img = cv2.imread('./sec0_1.jpg')
        #img_resize = cv2.resize(img,dsize=(self.gwidth, self.gheight))
        # cv2.imshow("MATLAB",img_resize)
        #t1= time.time()
        # while True:
        #    key = cv2.waitKey(1)
        #    if time.time()-t1 > 3:
        #      break
        #    if key !=-1 :
        #      break
        #    time.sleep(1/10)
        # ここまで不要

        # 動画再生準備
        time.sleep(self.retrunsignal)
        self.serial_NANO.write(b'a')  # マイコンにaを送る->マイコンは脳波計に信号を送る動画停止中
        self.sec = 0  # 現在のセクション
        self.cap.set(cv2.CAP_PROP_POS_FRAMES,
                     self.startframe)  # 動画のフレームをstart位置に
        ret, self.frame = self.cap.read()

        self.frame = cv2.resize(self.frame, (self.gwidth, self.gheight))
        self.c = self.c + 1
        cv2.imshow("MATLAB", self.frame)
        cv2.setMouseCallback('MATLAB', self.mouse_click)
        cv2.waitKey(1)
        # 三秒待つ
        t1 = time.time()
        while(self.cap.isOpened()):
            if(self.signal == '9'):
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.exit_app()
                break
            if t1 + 3 < time.time():
                break
        if self.signal == '9':  # リセットボタン
            self.signal = '0'
            self.sec_0()
        self.sec_1()  # sec_1計測開始へ

    def sec_1(self):
        print('計測開始#')
        ret = True
        if (self.cap.isOpened() == False):
            print("ビデオファイルを開くとエラーが発生しました")
        while(self.cap.isOpened()):
            #ret, self.frame = self.cap.read()
            if(self.signal == '9'):  # MATLABから5番の信号を待つ->sec_2動画再生開始
                break
            if self.signal == '5':
                print('5')
                break
            if ret == True:
                self.frame = cv2.resize(
                    self.frame, (self.gwidth, self.gheight))
                cv2.imshow("MATLAB", self.frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.exit_app()
                    break
            else:
                break
            time.sleep(1 / 50)
        if self.signal == '9':  # 9番はマイコンからのリセットボタンの信号->self.sec_0へ
            self.signal = '0'
            self.sec_0()
        self.sec_2()

    def sec_2(self):
        print('動画開始')
        self.starttime = time.time()
        self.signal = 0
        self.play = True
        current_frame = self.startframe + 1
        res = 0  # 信号の値
        hand = 0
        while(self.cap.isOpened()):
            ret, self.frame = self.cap.read()
            if(self.starttime + (self.retunstarttime) < time.time()):
                self.serial_NANO.write(b'b')
            ret = self.wait_skip(ret)
            if ret == True:
                self.frame = cv2.resize(
                    self.frame, (self.gwidth, self.gheight))
                cv2.imshow("MATLAB", self.frame)
                if self.signal == '2' and self.inputf == False:
                    self.inputf = True
                    print('2a')
                    res = 2

                if self.signal == '1' and self.inputf == False:
                    self.inputf = True
                    res = 1

                if(self.signal == '9'):
                    self.play = False
                    self.signal = '0'
                    break
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.exit = True
                    self.play = False
                    break
                # 信号の値によってマイコンと動画の動きを制御　指定フレームまでは制御しない

                if res == 2 and current_frame > int(self.startstop):
                    t1 = time.time()
                    print('2b')
                    while time.time() < t1 + 3:
                        a = 2
                    break
                if res == 1 and current_frame > int(self.starthand) and hand == 0:
                    self.serial_NANO.write(b'1')
                    hand = 1
                # print(current_frame)
                current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            else:
                self.play = False
                break
            time.sleep(1 / 100)
        print(time.time() - self.starttime)
        print(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        print('終了')
        if self.exit == True:
            self.exit_app()
            return
        else:
            self.sec_0()
    # 動画の再生スピードの調整

    def wait_skip(self, ret):
        ct = (time.time() * 1000) - (self.starttime * 1000)
        ft = (1000 / (self.fps * self.speed)) * \
            (self.cap.get(cv2.CAP_PROP_POS_FRAMES) - self.startframe)
        #print('ft'+ str(ft))
        #print('ct' +str(ct))
        if(ft > ct):
            while ft > ct:
                ct = (time.time() * 1000) - (self.starttime * 1000)
                time.sleep(1 / 100)
        else:
            while ft < ct:
                ft = (1000 / (self.fps * self.speed)) * \
                    (self.cap.get(cv2.CAP_PROP_POS_FRAMES) - self.startframe)
                ret, self.frame = self.cap.read()
                if ret == False:
                    return ret
        return ret
    # アプリの終了

    def exit_app(self):
        print('exit')
        self.signal = '9'
        self.cap.release()
        cv2.waitKey(1)
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        exit()
        # sys.exit()
        return
    # マウスが押されたとき


model = Model()
# model.reset()
