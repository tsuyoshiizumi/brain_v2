
import cv2
import numpy as np
def draw_circle(event,x,y,flags,param):
   if event == cv2.EVENT_LBUTTONDBLCLK:
     print('dbClick')
   if event != 0:
    print()
    #global PLAYFLG
    #PLAYFLG=False
    
# Change here
WIDTH = 1920
HEIGHT = 1080
PLAYFLG = True
# For secondary monitor,
LEFT = 0
TOP = 0

screen = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
cv2.namedWindow('screen') #,cv2.WINDOW_NORMAL) #cv2.WINDOW_NORMAL
cv2.setMouseCallback('screen',draw_circle)
cv2.moveWindow('screen', LEFT, TOP)
cv2.setWindowProperty('screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    cv2.imshow('screen', screen)
    if  PLAYFLG==False:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cv2.destroyAllWindows()    