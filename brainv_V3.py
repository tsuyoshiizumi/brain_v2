from mimetypes import init
import re
import sys
import tkinter 
import cv2
import time
import serial as sl
import threading
import usbdebug2 as ub
import platform

class Model():
    def __init__(self): 
        tk = tkinter.Tk()
        self.gwidth  = tk.winfo_screenwidth()
        self.gheight = tk.winfo_screenheight()
        tk.destroy()
        self.cap = cv2.VideoCapture(r'./video/osaka_mr2021.mp4')
        
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.starttime = 0 
        self.stoptime  = 3 #最初の待機時間
        self.stoptime2 = 3 #動画停止後の待機時間
        self.signal    = 0 #512
        self.sec       = 0 #セクション０待機中　1計測中　２計測終了
        self.inputf    = False #入力受付 True #処理終了False
        self.play      = False
        self.exit      = False
        #
        #cv2.namedWindow('screen', cv2.WINDOW_NORMAL)
        #cv2.setWindowProperty('screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        self.c=0
        #self.init_com()
        #ここから別スレッドで入力を待つ
        self.init_com()
        thread1 = threading.Thread(target=self.thread1)
  
        thread1.start()
        self.reset()
        self.sec_0()    
        
        
    def init_com(self):
    
        os = platform.system() #Windows Darwin Linux
         #脳波計シリアルポート
        if os== 'Darwin': 
            self.comb      = '/dev/tty.usbmodem54260134801'
            #M5
            self.comm5     = '/dev/tty.usbmodem54240333141'
            #nano
            self.comnano   = '/dev/tty.usbserial-130'
        if os== 'Linux':
            self.comb      = ub.port_p('5-1.3')
            #nano
            self.comnano   = ub.port_p('5-1.2')

        self.serial_brain = sl.Serial(
                self.comb, 9600, timeout=0)
       # self.serial_M5    = sl.Serial(
       #        self.comm5 , 115200, timeout=0)
        self.serial_NANO    = sl.Serial(
                self.comnano, 9600, timeout=0)        
    def reset(self):
        self.cuurent_farme = 0
        self.starttime     = 0
        self.frames        = None
        self.sec           = 0
        self.inputf        = False       
    def thread1(self):
       while True:
         if self.signal=='9':
             return   
         t1=time.time()
         line = None
         if(self.serial_brain.is_open):
                    line = self.serial_brain.readline()
                    line = line.strip().decode('utf-8')
                    if line != '':
                      print (line)
                      self.signal = line
         else:
           print('NG')  
           return
         line2 = None
         if(self.serial_NANO.is_open):
                    line2 = self.serial_NANO.readline()
                    line2 = line2.strip().decode('utf-8')
                    if line2 != '':
                      print (line2)
                      self.signal = line2
                      
         else:
            print('NG_m5')  
            return            
         time.sleep(1/100)

    def sec_0(self):
       
        self.reset()
        self.serial_NANO.write(b'a')
        self.sec    = 0
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 1)
        ret, self.frame = self.cap.read()
        
        #cv2.namedWindow('screen',cv2.WINDOW_GUI_NORMAL)
        cv2.namedWindow('screen',cv2.WINDOW_AUTOSIZE)
        cv2.setWindowProperty('screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        #cv2.resizeWindow('screen', self.gwidth, self.gheight)
        
        self.frame = cv2.resize(self.frame,(self.gwidth,self.gheight))
        self.c = self.c+1
        
        print( self.gwidth)
        cv2.imshow("screen", self.frame)
        cv2.waitKey(1)
        if(self.c<2):
           print(self.c) 
           self.sec_0()           
        t1= time.time()
        while(self.cap.isOpened()):
            if(self.signal =='9' ):
              break
            if cv2.waitKey(1) & 0xFF == ord('q'): 
             self.exit_app()
             break
            if t1+ 3 < time.time():
             break
        if self.signal=='9':
            self.signal ='0'
            self.sec_0()        
        self.sec_1()
    def sec_1(self):
        print('計測開始#')
        ret=True
        if (self.cap.isOpened()== False):  
           print("ビデオファイルを開くとエラーが発生しました") 
        while(self.cap.isOpened()):
            #ret, self.frame = self.cap.read()
            if(self.signal =='9' ):
              break        
            if self.signal=='5':
                print('5')
                break
            if ret == True:
                cv2.imshow("screen", self.frame)      
                if cv2.waitKey(1) & 0xFF == ord('q'): 
                   self.exit_app()
                   break
            else:
               break
            time.sleep(1/1000)
        if self.signal=='9':
            self.signal ='0'
            self.sec_0()    
        self.sec_2()    
    def sec_2(self):
        print('動画開始')
        self.starttime= time.time()
        self.signal = 0
        self.play=True
        while(self.cap.isOpened()):
           ret, self.frame = self.cap.read()
           self.serial_NANO.write(b'b')
           ret = self.wait_skip(ret) 
           if ret == True:
                self.frame = cv2.resize(self.frame,(self.gwidth,self.gheight))
                cv2.imshow("screen", self.frame)      
                if self.signal == '2' and self.inputf ==False:
                   self.inputf= True
                   t1= time.time()
                   while time.time()<t1+3:
                        a=1
                   break
                if self.signal == '1' and self.inputf ==False:
                   self.inputf= True      
                   self.serial_NANO.write(b'1')
                if(self.signal =='9' ):
                    self.play   = False
                    self.signal = '0'
                    break 

                if cv2.waitKey(1) & 0xFF == ord('q'):
                   self.exit=True
                   self.play=False
                   break
           else:
               self.play=False
               break
           time.sleep(1/1000)
        print(time.time()-self.starttime)  
        print(self.cap.get(cv2.CAP_PROP_POS_FRAMES))     
        print('終了')
        if self.exit==True:
           self.exit_app()
           return
        else:    
         self.sec_0()
    def wait_skip(self,ret):
      ct =  (time.time() * 1000) - (self.starttime * 1000)
      ft =  (1000 / self.fps)  * self.cap.get(cv2.CAP_PROP_POS_FRAMES) 
      print('ft'+ str(ft))
      print('ct' +str(ct)) 
      if(ft > ct):
         while ft > ct:
             ct = (time.time() * 1000) - (self.starttime * 1000)
             time.sleep(1/1000)
      else:
            ret, self.frame  = self.cap.read()
            
            if ret == False:
                return ret
      return ret          
    def exit_app(self):
            print('exit')
            self.signal='9'
            self.cap.release()
            cv2.waitKey(1)
            cv2.destroyAllWindows()
            cv2.waitKey(1) 
            sys.exit()
            return      
class View():
  def __init__(self,model):
      tk = tkinter.Tk()
      self.gwidth  = tk.winfo_screenwidth()
      self.gheight = tk.winfo_screenheight()


model = Model()
#model.reset()

