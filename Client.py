import socket
import cv2
import pickle
import struct

class FaceRecognitionClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('192.168.71.185', 806))  # Connect to the server

    def send_data(self, data):
        encoded_data = pickle.dumps(data)
        message_size = struct.pack("L", len(encoded_data))
        self.client_socket.sendall(message_size)
        self.client_socket.sendall(encoded_data)

    def start_client(self):
        camera = cv2.VideoCapture(0)
        while True:
            success, frame = camera.read()
            if not success:
                continue
            self.send_data(frame)
        camera.release()
        self.client_socket.close()

if __name__ == "__main__":
    client = FaceRecognitionClient()
    client.start_client()
