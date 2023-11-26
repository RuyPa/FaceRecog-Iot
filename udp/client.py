import cv2
import pickle
import socket
import struct
from picamera2 import Picamera2
from gpiozero import AngularServo
import time

# servo = AngularServo(18, min_pulse_width = 0.0005, max_pulse_width = 0.0025)
# servo.angle = 0

picam2 = Picamera2()
cv2.startWindowThread()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', 'size': (640, 480)}))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.117.143'
port = 807
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

try:
    client_socket.connect((host_ip, port))
    picam2.start()

    while True:
        frame = picam2.capture_array()

        cv2.imshow('TRANSMITTING VIDEO', frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            # Extract the face region from the frame

            # Serialize the face_roi and send it to the server
            face_data = pickle.dumps(frame)
            face_message = struct.pack("Q", len(face_data)) + face_data
            client_socket.sendall(face_message)

            # Draw a rectangle around the detected face
            name_length_data = client_socket.recv(8)

            if len(name_length_data) < 8:
                print("Error: Unable to receive name length data.")
                break

            name_length = struct.unpack("Q", name_length_data)[0]

            if name_length == 0:
                print("Error: Invalid name length received.")
                break

            name_data = client_socket.recv(name_length)

            if len(name_data) < name_length:
                print("Error: Unable to receive complete name data.")
                break

            name = pickle.loads(name_data)
            print(name)
            if name == '1':
                servo = AngularServo(18, min_pulse_width=0.0005, max_pulse_width=0.0025)
                servo.angle = 90
                time.sleep(2)
                servo.close()
                time.sleep(5)
                servo = AngularServo(18, min_pulse_width=0.0005, max_pulse_width=0.0025)
                servo.angle = 0
                time.sleep(2)
                servo.close()

        # Display the frame with face detection

        # ---------------------------------------------------
        # Receive the name from the server

        # name_length = struct.unpack("Q", client_socket.recv(8))[0]
        # name_message = client_socket.recv(name_length)
        # name = pickle.loads(name_message)
        # print("Received name:", name)
        # ------------------------------------------------------------
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

except KeyboardInterrupt:
    pass

finally:
    client_socket.close()
    cv2.destroyAllWindows()
