from flask import Flask, render_template, request, Response
import cv2
import os
import numpy as np
import os
import mysql.connector as connector
import training as tr
import numpy as np
from PIL import Image
from datetime import datetime


app = Flask(__name__)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()

detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


def getImagesAndLabels(path):

    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    faceSamples = []

    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L')

        img_numpy = np.array(PIL_img, 'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])

        faces = detector.detectMultiScale(img_numpy)

        for (x, y, w, h) in faces:

            faceSamples.append(img_numpy[y:y+h, x:x+w])

            ids.append(id)

    return faceSamples, ids


def fetchdata(Id):
    connection = connector.connect(
        host="localhost", user="root", password="Atharva@100", database="edicp")
    cursor = connection.cursor()
    sql_select_query = """select * from details where iddetails = %s"""
    cursor.execute(sql_select_query, (Id,))
    record = cursor.fetchall()
    return record


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def id():
    connection = connector.connect(
        host="localhost", user="root", password="Atharva@100", database="edicp")
    cursor = connection.cursor()
    sql_select_query = """select MAX(iddetails) from details"""
    cursor.execute(sql_select_query, ())
    id1 = cursor.fetchall()
    value = id1[0][0]
    return value


def insert(face_id, firstname, lastname, username, dob, adhaar, phone):
    connection = connector.connect(
        host="localhost", user="root", password="Atharva@100", database="edicp")
    cursor = connection.cursor()
    sql_insert_query = "INSERT INTO details (iddetails, fname, lname, usern, dob, aadhar, phone) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (face_id, firstname, lastname, username, dob, adhaar, phone)
    cursor.execute(sql_insert_query, values)
    connection.commit()
    cursor.close()
    connection.close()


def generate_frames():

    video_capture = cv2.VideoCapture(0)

    while True:

        ret, frame = video_capture.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    video_capture.release()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/register', methods=['POST'])
def capture():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cam = cv2.VideoCapture(0)
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x - 20, y - 20),
                          (x + w + 20, y + h + 20), (0, 255, 0), 4)
            Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            cv2.rectangle(im, (x - 22, y - 90),
                          (x + w + 22, y - 22), (0, 255, 0), -1)
            cv2.putText(im, str(Id), (x, y - 40), font, 1, (255, 255, 255), 3)

        cv2.imshow('im', im)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    temp = fetchdata(Id)
    firstname = temp[0][1]
    lastname = temp[0][2]
    username = temp[0][3]
    dob = temp[0][4]
    adhaar = temp[0][5]
    phone = temp[0][6]
    cam.release()
    cv2.destroyAllWindows()

    return render_template('result.html', firstname=firstname, lastname=lastname, username=username,  dob=dob,  adhaar=adhaar, phone=phone)


@app.route("/register2", methods=['POST'])
def face_g():
    face_id = int(id())+1
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    username = request.form["username"]
    dob1 = request.form["dob"]
    adhaar = request.form["adhaar"]
    phone = request.form["phone"]
    dob_date = datetime.strptime(dob1, '%Y-%m-%d')
    dob = dob_date.strftime('%Y-%m-%d')
    insert(face_id, firstname, lastname, username, dob, adhaar, phone)
    vid_cam = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier(
        "C:/Users/Atharva/Desktop/EDI2/haarcascade_frontalface_default.xml")
    count = 0
    while (True):
        _, image_frame = vid_cam.read()
        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(image_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            count += 1
            cv2.imwrite("dataset/User." + str(face_id) + '.' +
                        str(count) + ".jpg", gray[y:y+h, x:x+w])
            cv2.imshow('frame', image_frame)

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

        elif count > 20:
            break

    faces, ids = getImagesAndLabels('dataset')

    recognizer.train(faces, np.array(ids))

    assure_path_exists('trainer/')
    recognizer.save('trainer/trainer.yml')
    return render_template('result2.html')


if __name__ == '__main__':
    app.run(debug=True)
