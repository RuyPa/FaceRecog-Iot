import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime


def addAttendanceTime(id):


    ref = db.reference('FaceID')

    new_attendance_time = str(datetime.now())

    # Get the current data for "BA_DUY" from the database
    data_of_id = ref.child(id).get()

    # Add the new attendance time to the list
    data_of_id["attendance time"].append(new_attendance_time)

    # Update the data in the database for "BA_DUY"
    ref.child(id).update(data_of_id)

