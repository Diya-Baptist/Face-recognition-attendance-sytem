import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

video_capture = cv2.VideoCapture(0)

# load known faces
# encoding means to convert image to number so that its easier to compare
# 0 because photo can have lots of img but we want first image

diya_image = face_recognition.load_image_file("faces/Diya.jpg")
diya_encoding = face_recognition.face_encodings(diya_image)[0]

lisa_image = face_recognition.load_image_file("faces/lisa.jpg")
lisa_encoding = face_recognition.face_encodings(lisa_image)[0]

known_face_encodings = [diya_encoding, lisa_encoding]
known_face_names = ["Diya", "Lisa"]

# list of expected students
students = known_face_names.copy()
face_locations = []
face_encodings = []

# get current date and time

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

# make csv writer
# a+ using to keep the track of all attendance

f = open(f"{current_date}.csv", "a+", newline="")
lnwriter = csv.writer(f)

# first argument underscore in while loop to check if videocapture is successful then second argument frame
while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # covert to rgb
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # recognize face
    face_locations=face_recognition.face_locations(rgb_small_frame)
    # encoding of faces through web cam
    face_encodings=face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        # comapre face encoding to the previously know encodings
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        # tells how much similar are both
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        # min distance therefore most similar
        best_match_index = np.argmin(face_distances)
        #initialise name

        name= None


        if matches[best_match_index]:
            # gives the name to whom its matched
            name = known_face_names[best_match_index]

        # text add if person is present
        if name in known_face_names:
            # Define text properties
            text = f"{name} Present"
            org = (10, 100)
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (180, 105, 255)  # BGR color format
            thickness = 3
            lineType = cv2.LINE_AA

            # Draw text on the frame
            cv2.putText(frame, text, org, font, fontScale, color, thickness, lineType)

            if name in students:
                # remove beacuse alredy marked present
                students.remove(name)
                current_time = now.strftime("%H-%M-%S")
                lnwriter.writerow([name, current_time])



    cv2.imshow('attendance', frame)
    # if i type q on kyeboard the while loop exits
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# free the camera
video_capture.release()
#closes all windows
cv2.destroyAllWindows()
f.close()









