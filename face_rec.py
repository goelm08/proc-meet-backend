import base64
import os
import cv2
import face_recognition
import numpy as np
from PIL import Image

known_path = "known_faces"  # Set the path to your known faces folder
unknown_path = "unknown_faces"  # Set the path to your unknown faces folder

encodings = []


def base64_to_numpy_array(base64_string):
    img = Image.open(base64_string.stream)
    img_np = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return img_np


def register_face(name, known_path, image_base64):
    dirOld = os.getcwd()
    global encodings

    # video_capture = cv2.VideoCapture(0)
    # ret, frame = video_capture.read()

    frame = base64_to_numpy_array(image_base64)

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(
        rgb_small_frame, face_locations)

    dir = os.path.join(known_path, name)
    print(dir)
    print(os.getcwd())
    if not os.path.isdir(dir):
        os.mkdir(dir)
    os.chdir(known_path)
    os.chdir(name)
    rand_no = np.random.random_sample()
    cv2.imwrite(f"{rand_no}.jpg", frame)
    # video_capture.release()
    cv2.destroyAllWindows()

    for i in face_encodings:
        encodings.append((name, i))
    os.chdir(dirOld)


def recognize_face(known_path, unknown_path, image_base64):
    dirOld = os.getcwd()
    global encodings

    known_face_encodings = [i[1] for i in encodings]
    known_face_names = [i[0] for i in encodings]

    # video_capture = cv2.VideoCapture(0)
    # ret, frame = video_capture.read()

    frame = base64_to_numpy_array(image_base64)

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(
        rgb_small_frame, face_locations)
    face_names = []

    if not face_encodings:
        msg = "You are unknown first register your self"
    else:
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            if name == "Unknown":
                msg = "You are unknown first register your self"
            else:
                msg = name
            face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)

        os.chdir(unknown_path)
        rand_no = np.random.random_sample()
        cv2.imwrite(f"{rand_no}.jpg", frame)
    os.chdir(dirOld)
    return msg
