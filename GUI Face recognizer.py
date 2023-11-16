#importing Libraries
import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import os 
import mysql.connector as connector
import training as tr
import numpy as np
from PIL import Image


#GUI Framework
window = tk.Tk()
window.title("Face Recognition system")

l1 = tk.Label(window, text="First Name", font=("Times New Roman",20))
l1.grid(column=0, row=0)
t1 = tk.Entry(window, width=50, bd=5)
t1.grid(column=1, row=0)

l2 = tk.Label(window, text="Last Name", font=("Times New Roman",20))
l2.grid(column=0, row=1)
t2 = tk.Entry(window, width=50, bd=5)
t2.grid(column=1, row=1)

l3 = tk.Label(window, text="Gender ", font=("Times New Roman",20))
l3.grid(column=0, row=2)
t3 = tk.Entry(window, width=50, bd=5)
t3.grid(column=1, row=2)

l4 = tk.Label(window, text="DOB ", font=("Times New Roman",20))
l4.grid(column=0, row=3)
t4 = tk.Entry(window, width=50, bd=5)
t4.grid(column=1, row=3)

#Fetch Data from MySQL

def fetchdata(Id):
    connection = connector.connect(host="localhost",user="root",password="Atharva@100",database="oopcp")
    cursor = connection.cursor()
    sql_select_query = """select * from details where iddetails = %s"""    
    cursor.execute(sql_select_query, (Id,))
    record = cursor.fetchall()
    x = Id-1
    t1.insert(x,record[0][1])   
    t2.insert(x,record[0][2])
    t3.insert(x,record[0][3])
    t4.insert(x,record[0][4])


def train_classifier():
    data_dir = "C:\\Users\\Atharva\\Desktop\\OOP CP\\dataset"
    path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
    faces = []
    ids = []
    for image in path:
        img = Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(os.path.split(image)[1].split(".")[1])
        
        faces.append(imageNp)
        ids.append(id)
        
    ids = np.array(ids)
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces,ids)
    clf.write("classifier.xml")
    
    messagebox.showinfo('Result','Training dataset completed successfully')    

b1 = tk.Button(window, text="Training", font=("Times New Roman",20),bg="orange",fg="red",command=train_classifier)
b1.grid(column=0, row=5)

def face_recognition():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cam = cv2.VideoCapture(0)
    while True:
        ret, im =cam.read()
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2,5)
        for(x,y,w,h) in faces:
            cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)
            Id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
            cv2.putText(im, str(Id), (x,y-40), font, 1, (255,255,255), 3)

        
        cv2.imshow('im',im) 
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    fetchdata(Id)
    cv2.destroyAllWindows()

   
b2 = tk.Button(window, text="Detect the faces", font=("Times New Roman",20), bg="green", fg="orange", command=face_recognition)
b2.grid(column=1, row=5)

def generate_dataset():
    vid_cam = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier("C:/Users/Atharva/Desktop/Atharva/OOP CP/haarcascade_frontalface_default.xml")
    face_id = input("Enter your id")
    count = 0
    while(True):
        _, image_frame = vid_cam.read()
        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(image_frame, (x,y), (x+w,y+h), (255,0,0), 2)
            count += 1
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            cv2.imshow('frame', image_frame)

        
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

        
        elif count>100:
            break


    vid_cam.release()
    cv2.destroyAllWindows()

b3 = tk.Button(window, text="Generate dataset", font=("Times New Roman",20), bg="pink", fg="black", command=generate_dataset)
b3.grid(column=2, row=5)

window.geometry("800x200")
window.mainloop()