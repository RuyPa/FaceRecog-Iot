import os
import queue

import cv2
import pickle
import socket
import struct

import firebase_admin
import numpy as np
from firebase_admin import credentials, storage
from FAS import anti_spoof


# from udp import TestCore

from udp.TestCore import face_recog
tmp=face_recog()

show_receiving = True

global currentNumberOfBlobs

def receive_from_client(client_socket, currentNumberOfBlobs, app, tmp):
    global show_receiving
    data = b""
    payload_size = struct.calcsize("Q")

    frame_queue = queue.Queue()
    max_queue = 0


    while show_receiving:
        try:
            while len(data) < payload_size:
                packet = client_socket.recv(480)  # 4K
                if not packet:
                    break
                data += packet

                numberOfBlos = checkNumberOfBlob(app)

                # print(numberOfBlos)
                # print(currentNumberOfBlobs)

                if (numberOfBlos != currentNumberOfBlobs):
                    tmp.setMany(app)
                    currentNumberOfBlobs = numberOfBlos


            packed_msg_size = data[:payload_size]
            data = data[payload_size:]

            if len(packed_msg_size) == 0:
                break
                # print(1)
                # continue
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(480)

            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)



            frame1 = np.array(frame)

            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGRA2BGR)


            frame2 = frame
            # name = TestCore.process(frame)

            resultFromDetect = anti_spoof(frame1)

            # resultFromDetect = True



            if resultFromDetect == True:

                name = tmp.process(frame2)

                if name != 'Unknown' or name == '':
                    name_message = pickle.dumps('1')
                    name_length = struct.pack("Q", len(name_message))
                    client_socket.sendall(name_length + name_message)
                if name == 'Unknown':
                    name_message = pickle.dumps('0')
                    name_length = struct.pack("Q", len(name_message))
                    client_socket.sendall(name_length + name_message)
            else:
                name_message = pickle.dumps('Fake')
                name_length = struct.pack("Q", len(name_message))
                client_socket.sendall(name_length + name_message)

        except struct.error as e:
            print(f"Error: {e}")
            break

    client_socket.close()
    cv2.destroyAllWindows()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host_ip = socket.gethostbyname(socket.gethostname())

    host_ip = '192.168.117.143'

    print('HOST IP:', host_ip)
    port = 807
    socket_address = (host_ip, port)

    server_socket.bind(socket_address)
    server_socket.listen(5)
    print("LISTENING AT:", socket_address)

    cred = credentials.Certificate("..\serviceAccountKey.json")
    app = firebase_admin.initialize_app(cred, {
        'databaseURL': "https://ruypa-64600-default-rtdb.asia-southeast1.firebasedatabase.app/",
        'storageBucket': "ruypa-64600.appspot.com"
    })
    currentNumberOfBlobs = checkNumberOfBlob(app)
    tmp.setMany(app)
    print('124')
    while True:
        client_socket, addr = server_socket.accept()
        print('GOT CONNECTION FROM:', addr)

        receive_from_client(client_socket, currentNumberOfBlobs, app, tmp)

    server_socket.close()

def checkNumberOfBlob(app):
    bucket = storage.bucket(app=app)
    folder_path = 'Images'
    blobs = bucket.list_blobs(prefix=folder_path)
    dem = 0
    for blob in blobs:
        dem += 1
    return dem


server()


