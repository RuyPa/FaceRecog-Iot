# import socket
# import cv2
# import pickle
# import struct
# import os
# import sys
# import numpy as np
# from datetime import datetime
# import face_recognition
#
# import socket
# import cv2
# import pickle
# import struct
#
# class FaceRecognitionServer:
#     def __init__(self, path):
#         self.path = path
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server_socket.bind(('localhost', 806))  # Set the server address and port
#         self.server_socket.listen(5)  # Listen for connections
#         self.classNames = []  # Initialize the classNames attribute
#         self.images = []
#         self.encodeListKnown = []
#         self.myList = []
#         self.stime = 0
#
#     def load_images(self):
#         images = []
#         myList = os.listdir(self.path)
#         for cl in myList:
#             curImg = cv2.imread(f'{self.path}/{cl}')
#             images.append(curImg)
#             self.classNames.append(os.path.splitext(cl)[0])  # Populate classNames
#         self.encodeListKnown = self.find_encodings(images)
#         print('Encoding Complete')
#
#     def find_encodings(self, images):
#         encodeList = []
#         for img in images:
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             encode = face_recognition.face_encodings(img)[0]
#             encodeList.append(encode)
#         return encodeList
#
#     def start_server(self):
#         while True:
#             client_socket, addr = self.server_socket.accept()
#             try:
#                 # client_socket, addr = self.server_socket.accept()  # Accept client connection
#                 print('Connection from:', addr)
#
#                 # Receive image data from client
#                 data = b""
#                 payload_size = struct.calcsize("L")
#                 while True:
#                     while len(data) < payload_size:
#                         packet = client_socket.recv(4*1024)  # Increase packet size for larger transmissions
#                         if not packet:
#                             break
#                         data += packet
#                     packed_msg_size = data[:payload_size]
#                     data = data[payload_size:]
#                     msg_size = struct.unpack("L", packed_msg_size)[0]
#                     while len(data) < msg_size:
#                         packet = client_socket.recv(4*1024)  # Receive data in chunks
#                         if not packet:
#                             break
#                         data += packet
#                     frame_data = data[:msg_size]
#                     data = data[msg_size:]
#                     frame = pickle.loads(frame_data)
#                     processed_frame = self.recognize_faces(frame)
#                     self.send_data(processed_frame, client_socket)
#             except ConnectionResetError:
#                 print("Client forcibly disconnected")
#                 continue
#             finally:
#                 client_socket.close()
#
#     def mark_attendance(self, name, time):
#         with open('Attendance.csv', 'r+') as f:
#             myDataList = f.readlines()
#             nameList = [line.split(',')[0] for line in myDataList]
#             if name not in nameList or time >= 10:
#                 now = datetime.now()
#                 dtString = now.strftime('%Y/%M/%D %H:%M:%S')
#                 f.writelines(f'\n{name},{dtString}')
#
#     def recognize_faces(self, img):
#         imgS = cv2.resize(img, (0, 0), None, fx=0.25, fy=0.25)
#         imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
#
#         facesCurFrame = face_recognition.face_locations(imgS)
#         encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
#         etime = datetime.now().strftime('%S')
#
#         processed_img = img  # Create a copy to draw on
#
#         for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
#             matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
#             faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
#             print(faceDis)
#             matchIndex = np.argmin(faceDis)
#             if faceDis[matchIndex] < 0.50:
#                 name = self.classNames[matchIndex].upper()
#                 print(name)
#                 if abs(int(etime) - int(self.stime)) >= 10:
#                     time = abs(int(etime) - int(self.stime))
#                     self.mark_attendance(name, time)
#                     self.stime = etime  # Update the self.stime variable
#             else:
#                 name = 'Unknown'
#             y1, x2, y2, x1 = faceLoc
#             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#             cv2.rectangle(processed_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.rectangle(processed_img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#             cv2.putText(processed_img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
#
#         return processed_img
#
#     def send_data(self, data, socket):
#         encoded_data = pickle.dumps(data)
#         message_size = struct.pack("L", len(encoded_data))
#         socket.sendall(message_size + encoded_data)
#
# if __name__ == "__main__":
#     server = FaceRecognitionServer('ImagesAttendance')  # Provide the path here
#     server.load_images()  # Load known images
#     server.start_server()  # Start the server
#


# import socket
# import cv2
# import pickle
# import struct
# import os
# import sys
# import numpy as np
# from datetime import datetime
# import face_recognition
#
# class FaceRecognitionServer:
#     def __init__(self, path):
#         self.path = path
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server_socket.bind(('localhost', 806))
#         self.server_socket.listen(5)
#         self.classNames = []
#         self.images = []
#         self.encodeListKnown = []
#         self.myList = []
#         self.stime = 0
#
#     def load_images(self):
#         images = []
#         myList = os.listdir(self.path)
#         for cl in myList:
#             curImg = cv2.imread(f'{self.path}/{cl}')
#             images.append(curImg)
#             self.classNames.append(os.path.splitext(cl)[0])
#         self.encodeListKnown = self.find_encodings(images)
#         print('Encoding Complete')
#
#     def find_encodings(self, images):
#         encodeList = []
#         for img in images:
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             encode = face_recognition.face_encodings(img)[0]
#             encodeList.append(encode)
#         return encodeList
#
#     def start_server(self):
#         cv2.namedWindow('Server Feed', cv2.WINDOW_NORMAL)
#         while True:
#             client_socket, addr = self.server_socket.accept()
#             try:
#                 print('Connection from:', addr)
#                 data = b""
#                 payload_size = struct.calcsize("L")
#                 while True:
#                     while len(data) < payload_size:
#                         packet = client_socket.recv(4*1024)
#                         if not packet:
#                             break
#                         data += packet
#                     packed_msg_size = data[:payload_size]
#                     data = data[payload_size:]
#                     msg_size = struct.unpack("L", packed_msg_size)[0]
#                     while len(data) < msg_size:
#                         packet = client_socket.recv(4*1024)
#                         if not packet:
#                             break
#                         data += packet
#                     frame_data = data[:msg_size]
#                     data = data[msg_size:]
#                     frame = pickle.loads(frame_data)
#                     processed_frame, recognized_names = self.recognize_faces(frame)
#                     cv2.imshow('Server Feed', processed_frame)
#                     if cv2.waitKey(1) & 0xFF == ord('q'):
#                         break
#                     self.send_data(processed_frame, client_socket)
#             except ConnectionResetError:
#                 print("Client forcibly disconnected")
#                 continue
#             finally:
#                 cv2.destroyAllWindows()
#                 client_socket.close()
#
#     def mark_attendance(self, name, time):
#         with open('Attendance.csv', 'r+') as f:
#             myDataList = f.readlines()
#             nameList = [line.split(',')[0] for line in myDataList]
#             if name not in nameList or time >= 10:
#                 now = datetime.now()
#                 dtString = now.strftime('%Y/%M/%D %H:%M:%S')
#                 f.writelines(f'\n{name},{dtString}')
#
#     def recognize_faces(self, img):
#         imgS = cv2.resize(img, (0, 0), None, fx=0.25, fy=0.25)
#         imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
#
#         facesCurFrame = face_recognition.face_locations(imgS)
#         encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
#         etime = datetime.now().strftime('%S')
#
#         processed_img = img
#
#         recognized_names = []
#         for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
#             matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
#             faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
#             print(faceDis)
#             matchIndex = np.argmin(faceDis)
#             if faceDis[matchIndex] < 0.50:
#                 name = self.classNames[matchIndex].upper()
#                 print(name)
#                 if abs(int(etime) - int(self.stime)) >= 10:
#                     time = abs(int(etime) - int(self.stime))
#                     self.mark_attendance(name, time)
#                     self.stime = etime
#             else:
#                 name = 'Unknown'
#
#             recognized_names.append(name)
#
#             y1, x2, y2, x1 = faceLoc
#             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#             cv2.rectangle(processed_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.rectangle(processed_img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#             cv2.putText(processed_img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
#
#         return processed_img, recognized_names
#
#     def send_data(self, data, socket):
#         encoded_data = pickle.dumps(data)
#         message_size = struct.pack("L", len(encoded_data))
#         socket.sendall(message_size + encoded_data)
#
# if __name__ == "__main__":
#     server = FaceRecognitionServer('ImagesAttendance')
#     server.load_images()
#     server.start_server()

import socket
import cv2
import pickle
import struct
import os
import sys
import numpy as np
from datetime import datetime
import face_recognition


class FaceRecognitionServer:
    def __init__(self, path):
        self.path = path
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 806))
        # self.server_socket.listen(5)
        self.classNames = []
        self.images = []
        self.encodeListKnown = []
        self.myList = []
        self.stime = 0
        self.client_connected = False


    def load_images(self):
        images = []
        myList = os.listdir(self.path)
        for cl in myList:
            curImg = cv2.imread(f'{self.path}/{cl}')
            images.append(curImg)
            self.classNames.append(os.path.splitext(cl)[0])
        self.encodeListKnown = self.find_encodings(images)
        print('Encoding Complete')

    def find_encodings(self, images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def start_server(self):

        while True:
            client_socket, addr = self.server_socket.accept()
            self.client_connected = True
            server_feed_window = cv2.namedWindow('Server Feed', cv2.WINDOW_NORMAL)
            try:
                print('Connection from:', addr)
                data = b""
                payload_size = struct.calcsize("L")

                while self.client_connected:
                    while len(data) < payload_size:
                        packet = client_socket.recv(4 * 1024)
                        if not packet:
                            break
                        data += packet
                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("L", packed_msg_size)[0]
                    while len(data) < msg_size:
                        packet = client_socket.recv(4 * 1024)
                        if not packet:
                            break
                        data += packet
                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    frame = pickle.loads(frame_data)
                    processed_frame, recognized_names = self.recognize_faces(frame)
                    cv2.imshow('Server Feed', processed_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    self.send_data(processed_frame, client_socket)
            except ConnectionResetError:
                print("Client forcibly disconnected")
                self.client_connected = False
                cv2.destroyWindow('Server Feed')

            finally:
                cv2.destroyAllWindows()
                client_socket.close()

    def mark_attendance(self, name, time):
        with open('Attendance.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = [line.split(',')[0] for line in myDataList]
            if name not in nameList or time >= 10:
                now = datetime.now()
                dtString = now.strftime('%Y/%M/%D %H:%M:%S')
                f.writelines(f'\n{name},{dtString}')

    def recognize_faces(self, img):
        imgS = cv2.resize(img, (0, 0), None, fx=0.25, fy=0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        etime = datetime.now().strftime('%S')

        processed_img = img

        recognized_names = []
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)
            if faceDis[matchIndex] < 0.50:
                name = self.classNames[matchIndex].upper()
                print(name)
                if abs(int(etime) - int(self.stime)) >= 10:
                    time = abs(int(etime) - int(self.stime))
                    self.mark_attendance(name, time)
                    self.stime = etime
            else:
                name = 'Unknown'

            recognized_names.append(name)

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(processed_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(processed_img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(processed_img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        return processed_img, recognized_names

    def send_data(self, data, socket):
        encoded_data = pickle.dumps(data)
        message_size = struct.pack("L", len(encoded_data))
        socket.sendall(message_size + encoded_data)


if __name__ == "__main__":
    server = FaceRecognitionServer('ImagesAttendance')
    server.load_images()
    server.start_server()
