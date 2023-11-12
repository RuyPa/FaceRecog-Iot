import cv2
import face_recognition
from datetime import datetime
import os
import numpy as np
import sys


class FaceRecognition:
    def __init__(self, path):
        self.path = path
        self.images = []
        self.classNames = []
        self.encodeListKnown = []
        self.myList = []
        self.stime = 0

    def load_images(self):
        self.myList = os.listdir(self.path)
        for cl in self.myList:
            curImg = cv2.imread(f'{self.path}/{cl}')
            self.images.append(curImg)
            self.classNames.append(os.path.splitext(cl)[0])
        self.encodeListKnown = self.find_encodings(self.images)
        print('Encoding Complete')

    def find_encodings(self, images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

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

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)
            if faceDis[matchIndex] < 0.50:
                name = self.classNames[matchIndex].upper()
                if abs(int(etime) - int(self.stime)) >= 10:
                    time = abs(int(etime) - int(self.stime))
                    self.mark_attendance(name, time)
                    stime = etime
            else:
                name = 'Unknown'
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        return img


def main():
    path = 'ImagesAttendance'  # Đường dẫn đến thư mục chứa ảnh
    recognition = FaceRecognition(path)
    recognition.load_images()  # Tải ảnh và mã hóa khuôn mặt

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    if not cap.isOpened():
        sys.exit('Video source not found...')

    while True:
        success, img = cap.read()

        if not success:
            continue

        img = recognition.recognize_faces(img)  # Nhận diện và chấm công

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
