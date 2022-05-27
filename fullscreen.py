import cv2
import numpy as np

# Change here
WIDTH = 1920
HEIGHT = 1080

# For secondary monitor,
LEFT = 0
TOP = 0

screen = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
cv2.namedWindow('screen', cv2.WINDOW_NORMAL)
cv2.moveWindow('screen', LEFT, TOP)
cv2.setWindowProperty('screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cv2.imshow('screen', screen)

cv2.waitKey(0)