from mimetypes import init
from signal import signal
import sys
import tkinter as tk
import cv2
import time
import serial as sl
import threading
import usbdebug2 as ub
import platform
import json
from PIL import Image
root = tk.Tk()
root.attributes('-fullscreen', True)
root.bind("<Escape>", root.quitFullScreen)
root.mainloop()