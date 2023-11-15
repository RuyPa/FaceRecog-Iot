import queue

import cv2
import pickle
import socket
import struct
from udp import TestCore

show_receiving = True

def receive_from_client(client_socket):
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

            TestCore.process(frame)

        except struct.error as e:
            print(f"Error: {e}")
            break

    client_socket.close()
    cv2.destroyAllWindows()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host_ip = socket.gethostbyname(socket.gethostname())

    host_ip = '192.168.113.143'

    print('HOST IP:', host_ip)
    port = 806
    socket_address = (host_ip, port)

    server_socket.bind(socket_address)
    server_socket.listen(5)
    print("LISTENING AT:", socket_address)

    while True:
        client_socket, addr = server_socket.accept()
        print('GOT CONNECTION FROM:', addr)

        receive_from_client(client_socket)

    server_socket.close()

server()


