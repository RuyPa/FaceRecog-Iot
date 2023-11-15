import cv2
import pickle
import socket
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.137.1'  # Địa chỉ IP của server
port = 806

try:
    client_socket.connect((host_ip, port))
    vid = cv2.VideoCapture(0)  # Mở webcam

    while True:
        ret, frame = vid.read()
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        client_socket.sendall(message)

        cv2.imshow('TRANSMITTING VIDEO', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

except KeyboardInterrupt:
    pass

finally:
    client_socket.close()
    cv2.destroyAllWindows()
