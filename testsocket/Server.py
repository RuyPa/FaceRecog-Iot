import socket
import cv2
import pickle
import struct
import numpy as np
import face_recognition
import os
from datetime import datetime

# Function to find face encodings from a list of images
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# Function to mark attendance or perform action for recognized faces
def markAttendance(name, time):
    with open('Attendance.csv', 'a') as f:
        now = datetime.now()
        dtString = now.strftime('%Y/%m/%d %H:%M:%S')
        f.write(f'{name},{dtString}\n')

# Function to process the image, find faces, and recognize them
def process_image(data, encodeListKnown, classNames):
    nparr = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # print('duy')

    if frame is None:
        return b''  # Skip processing if the frame is empty

    imgS = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if faceDis[matchIndex] < 0.50:
            name = classNames[matchIndex].upper()
            print(name)
            markAttendance(name, 10)  # Set the time statically to 10 seconds
        else:
            name = 'Unknown'

        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    ret, buffer = cv2.imencode('.jpg', frame)
    data = buffer.tobytes()

    return data

# Path to the directory containing face images for recognition
path = '..\ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(os.path.join(path, cl))
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
encodeListKnown = findEncodings(images)
print('Encoding Complete')

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 5555))
server_socket.listen(5)
print("Server is running and waiting for connections...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} has been established.")

    while True:
        try:
            data = b''
            payload_size = struct.calcsize("<L")
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)
                if not packet:
                    break
                data += packet

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("<L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            processed_data = process_image(frame_data, encodeListKnown, classNames)

            size = len(processed_data)
            client_socket.sendall(struct.pack("<L", size) + processed_data)

            # Here, you'll need to modify this part to send the actual recognized name
            # Replace 'name_to_send' with the actual recognized name
            name_data = b"Actual Recognized Name"  # Replace with the actual recognized name
            name_size = len(name_data)
            client_socket.sendall(struct.pack("<L", name_size) + name_data)
        except Exception as e:
            print("Error:", e)
            break

    client_socket.close()

