import numpy as np
import socket
import sys
import cv2

def create_socket(host, port, type):
    try:
        if type == 'UDP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        elif type == 'TCP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            return None
        return sock
    except:
        print("Could not create socket.")
        sys.exit(0)

def bind_socket(socket, host, port):
    try:
        socket.bind((host, port))
        print("[-] Socket Bound to port " + str(port))
    except:
        print("Bind Failed")
        sys.exit(0)

def client_thread_cam(s, host, port, cap):
    while True:
        ret, frame = cap.read()
        if(ret==False):
            print 'Nie wykryto kamery, zamykam watek'
            cap.release()
            s.close()
            print "[-] Socket on port " + str(port) + " closed"
            break
        else:
            cv2.imshow('frame'+str(port),frame)
            ret, buff = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
            data = np.array(buff)
            stringData = data.tostring()

            count = 0
            while count < len(stringData):
                if count+65565  > len(stringData):
                    s.sendto(stringData[count:], (host, port))
                else:
                    s.sendto(stringData[count:count+65565], (host, port))
                count += 65565

            if cv2.waitKey(1) & 0xFF == ord('q'):
                s.close()
                cap.release()
                cv2.destroyWindow('frame'+str(port))
                print "[-] Socket on port " + str(port) + " closed"
                break

def server_thread_cam(socket, client_count):
    img_to_read = ''
    img_to_show = ''

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyWindow('cam no ' + str(client_count))
            socket.close()
            print "Thread for camera no. "+str(client_count)+" finished"
            break

        while True:   # oczekujemy na obraz
            strng, addr = socket.recvfrom(65565)
            if len(strng) == 0:  # nie otrzymalismy wiadomosci
                if img_to_read != '':
                    img_to_show = img_to_read
                    img_to_read = ''
                break

            if (len(strng) < 65565) and (len(strng) > 0):
                # ostatnia czesc wiadomosci
                img_to_read += strng
                img_to_show = img_to_read
                img_to_read = '' # obraz zapisany, wychodzimy z petli
                break

            img_to_read += strng

        img_decoded = cv2.imdecode(np.fromstring(img_to_show, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
        if img_decoded != None:
            cv2.imshow('cam no ' + str(client_count), img_decoded)
        else:
            break
