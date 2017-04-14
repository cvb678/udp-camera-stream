import cv2
from thread import start_new_thread
from definitions import *
import time

HOST = ''
destHOST = ''
PORT = 11001
PORT2 = 11002

HOST = raw_input("Podaj swoj adres ip")
destHOST = raw_input("Podaj adres ip serwera")
cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
time.sleep(5)
s1 = create_socket(HOST, PORT, 'UDP')
bind_socket(s1, HOST, PORT)
start_new_thread(client_thread_cam, (s1, destHOST, PORT, cap))

s2 = create_socket(HOST, PORT2, 'UDP')
bind_socket(s2, HOST, PORT2)
start_new_thread(client_thread_cam, (s2, destHOST, PORT2, cap2))

while True:
    pass