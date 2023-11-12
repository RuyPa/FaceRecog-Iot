import socket
import cv2
import pickle
import struct
import numpy as np

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5555))

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    data = pickle.dumps(frame)

    size = len(data)
    client_socket.sendall(struct.pack("<L", size))

    for i in range(0, size, 4096):
        client_socket.sendall(data[i:i + 4096])

    size_data = b''
    while len(size_data) < 4:
        size_data += client_socket.recv(4 - len(size_data))

    size_to_receive = struct.unpack("<L", size_data)[0]

    frame_data = b''
    while len(frame_data) < size_to_receive:
        packet = client_socket.recv(4 * 1024)
        if not packet:
            break
        frame_data += packet

    if frame_data:
        frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), -1)
        cv2.imshow('Webcam', frame)

    # Receive and display the recognized name from the server
    name_size_data = b''
    while len(name_size_data) < 4:
        name_size_data += client_socket.recv(4 - len(name_size_data))

    name_size = struct.unpack("<L", name_size_data)[0]

    name_data = b''
    while len(name_data) < name_size:
        name_data += client_socket.recv(4 * 1024)

    recognized_name = name_data.decode()
    print("Recognized Name:", recognized_name)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
