import sys
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

from firebase_admin import storage

from service import AddAttendanceTime


class face_recog():
    def __int__(self):

        # self.path = '..\ImagesAttendance'
        self.images = None
        self.classNames = []
        self.stime = 0
        self.encodeListKnown = None
        # myList = os.listdir(path)

    def setMany(self, app):
        bucket = storage.bucket(app=app)
        folder_path = 'Images'
        blobs = bucket.list_blobs(prefix=folder_path)

        images = []
        class_names = []

        for blob in blobs:
            # Download the image from Firebase Storage
            blob_data = blob.download_as_bytes()
            image = cv2.imdecode(np.frombuffer(blob_data, np.uint8), -1)

            # Append the image and its class name to the lists

            images.append(image)
            self.images = images
            class_names.append((os.path.splitext(blob.name.split('/')[-1])[0]).upper())
            self.classNames = class_names

        encot = self.findEncodings(images=self.images)
        self.encodeListKnown = encot
        print('Encoding Complete')

    def findEncodings(self, images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def setEncode(self):

        self.encodeListKnown = self.findEncodings(images=self.images)

    def process(self, img):
        
        # if self.encodeListKnown == None:
        #     self.setEncode()
        
        # global stime
        # stime = self.stime
        # while True:
        imgS = cv2.resize(img, (0, 0), None, fx=0.25, fy=0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        etime = datetime.now().strftime('%S')

        name = ''

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)
            if faceDis[matchIndex] < 0.50:
                name = self.classNames[matchIndex].upper()
                # if abs(int(etime) - int(stime)) >= 10:
                #     time = abs(int(etime) - int(stime))
                #     # markAttendance(name, time)
                #     stime = etime
            else:
                name = 'Unknown'

            if name != 'Unknown':
                AddAttendanceTime.addAttendanceTime(name)

            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Webcam', img)
        cv2.waitKey(1)

        return name





# path = '..\ImagesAttendance'
# images = []
# classNames = []
# stime = 0
# myList = os.listdir(path)
# print(myList)
# for cl in myList:
#     curImg = cv2.imread(f'{path}/{cl}')
#     images.append(curImg)
#     classNames.append(os.path.splitext(cl)[0])
# print(classNames)
#
#
# def findEncodings(images):
#     encodeList = []
#     for img in images:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodeList.append(encode)
#     return encodeList
#
# encodeListKnown = findEncodings(images)
# print('Encoding Complete')
#
# def markAttendance(name, time):
#     with open('../Attendance.csv', 'r+') as f:
#         myDataList = f.readlines()
#         nameList = []
#         for line in myDataList:
#             entry = line.split(',')
#             nameList.append(entry[0])
#         if name not in nameList or time >= 10:
#             now = datetime.now()
#             dtString = now.strftime('%Y/%M/%D %H:%M:%S')
#             f.writelines(f'\n{name},{dtString}')
#
#
# def process(img):
#     global stime
#     # while True:
#     imgS = cv2.resize(img, (0, 0), None, fx=0.25, fy=0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
#
#     facesCurFrame = face_recognition.face_locations(imgS)
#     encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
#
#     etime = datetime.now().strftime('%S')
#
#     name = ''
#
#     for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
#         matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
#         faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
#         print(faceDis)
#         matchIndex = np.argmin(faceDis)
#         if faceDis[matchIndex] < 0.50:
#             name = classNames[matchIndex].upper()
#             if abs(int(etime) - int(stime)) >= 10:
#                 time = abs(int(etime) - int(stime))
#                 markAttendance(name, time)
#                 stime = etime
#         else:
#             name = 'Unknown'
#
#         if name != 'Unknown':
#             AddAttendanceTime.addAttendanceTime(name)
#
#         print(name)
#         y1, x2, y2, x1 = faceLoc
#         y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#         cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#         cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
#
#     cv2.imshow('Webcam', img)
#     cv2.waitKey(1)
#
#     return name
#
