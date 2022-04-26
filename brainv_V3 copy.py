import cv2
import time
cap = cv2.VideoCapture(r'./video/osaka_fl2021.mp4')

ret, frame = cap.read()

cv2.namedWindow('screen', cv2.WINDOW_NORMAL)
cv2.imshow("screen", frame)
time.sleep(10)

if (cap.isOpened()== False):  
  print("ビデオファイルを開くとエラーが発生しました") 

while(cap.isOpened()):
    
    #ret, frame = cap.read()
   
    if ret == True:
        cv2.namedWindow('screen', cv2.WINDOW_NORMAL)
       
        cv2.imshow("screen", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    
    else:
        break

cap.release()

cv2.destroyAllWindows()