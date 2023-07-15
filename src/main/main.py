#Importing Librarires necessary for the program to run.
import picamera2
import face_rec_module as frm
import face_recognition as face
import finger_module as finger
from gpiozero import Button
import numpy as np
import libcamera
import customtkinter as ctk
from PIL import Image, ImageTk
from datetime import datetime
import multiprocessing
import cv2
import csv
import time
import os


#Raspbery Pi camera Confgurations
picam2 = picamera2.Picamera2()
preview_config = picam2.create_preview_configuration(main={"format": 'BGR888', "size": (640, 480)},                                             
                                                    lores={"format": 'YUV420', "size": (320, 240)},
                                                    transform=libcamera.Transform(hflip=1))

capture_config = picam2.create_video_configuration(main={"format": 'BGR888', "size": (640, 480)},
                                                   transform=libcamera.Transform(hflip=1))
                                                    


#Path of directories
known_face_dir = "/home/bounty/main/database/known_face_dir"
known_face_encodings_dir = "/home/bounty/main/database/known_face_encodings"
databse_dir = "/home/bounty/main/database/"


#Global Variables
known_face_encodings = []
known_face_names = []
img_array = np.empty((480, 640, 3), dtype=np.uint8)
counter = 0

#Face Reccognition Variables
tolerance = 0.5

#Finger Print Detection Pin
finger_detect = Button(17, pull_up=False)

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")



#Functions
def start():
    cv2.namedWindow('Preview', cv2.WINDOW_GUI_NORMAL)
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d") 
    f = open(f"{class_id_entry.get()}_{current_date}.csv", "w", newline="")
    lnwriter = csv.writer(f)
    lnwriter.writerow(["Name", "Time"])

    while True:
        start = time.time()
        img_array = picam2.capture_array("main")
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

        #if counter%15 == 0:
        face_locations = face.face_locations(img_array)
        print("Found {} faces in image.".format(len(face_locations)))
        face_encodings = face.face_encodings(img_array, face_locations)

        # for (top, right, bottom, left) in face_locations:
        #                     print(top, right, bottom, left)
        #                     cv2.rectangle(img_array, (left, top), (right, bottom), (0, 0, 255), 2)
        #                     cv2.moveWindow('Preview', 420, 110)
        #                     cv2.imshow('Preview', img_array)
        #                     cv2.resizeWindow('Preview', 500, 370)
        #                     cv2.waitKey(1)
                            
                           #cv2.putText(img_array, name, (left + 6, top - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

        try:
            for i in range(len(face_encodings)):
                #capture_array = picam2.capture_array("main")
                match = face.compare_faces(known_face_encodings, face_encodings[i], tolerance)
                #print(match)
                #print("Names: ", known_face_names)
                #print(known_face_names[i]+"\n")

                if True in match:

                    for j in match:
                        if j == True:
                            print("Found...{}".format(known_face_names[match.index(j)]))
                            current_time = now.strftime("%H:%M:%S")
            
        except:
            pass
    
        for (top, right, bottom, left) in face_locations:
                        print(top, right, bottom, left)
                        cv2.rectangle(img_array, (left, top), (right, bottom), (0, 0, 255), 2)
        
        cv2.moveWindow('Preview', 420, 110)
        cv2.imshow('Preview', img_array)
        cv2.resizeWindow('Preview', 500, 370)
        cv2.waitKey(1)

        end = time.time()
        print("\nTime Taken: ", end-start, end="\n")

        #print(cv2.getWindowProperty('Preview', cv2.WND_PROP_VISIBLE))
        if cv2.getWindowProperty('Preview', cv2.WND_PROP_VISIBLE) < 1:
              f.close()
              break
    
    cv2.destroyAllWindows()
    

#_____MAIN-PROGRAM______#

if __name__ == "__main__":
    print("Starting>>>...")
    print("Creating/Loading faces.....")
    
    #Generating and Loading saved encodings
    known_face_names, known_face_encodings = frm.generate_face_encodings_with_checking(known_face_dir, known_face_encodings_dir)
    print("Names: ", known_face_names)

    print("\nStarting camera...\n")
    picam2.configure(preview_config)
    picam2.start()
    #time.sleep(10)

    window = ctk.CTk()
    window.title("Attendance System")
    window.geometry(f"{1024}x{600}")
    ctk.set_appearance_mode("dark")


    # Label for PICt
    heading_pict = ctk.CTkLabel(window, text="PICT ATTENDANCE SYSTEM", text_color="white", height=50, corner_radius=20,
                        font=("Helvetica", 30, "bold"))
    heading_pict.grid_configure(sticky="ew", ipadx=0, ipady=0, columnspan=3)

    # Frames
    frame1 = ctk.CTkFrame(window, height=450, width=300)
    frame2 = ctk.CTkFrame(window, height=450, width=630)
    frame1.grid(column=1, row=2, padx=30, pady=10)
    frame2.grid(column=2, row=2, padx=10, pady=20)
    frame2.grid_propagate(False)

    #admin_label
    admin_label = ctk.CTkLabel(frame2, text="FOR ADMIN USE ONLY", text_color="white", font=("Helvetica", 25, "bold"))
    admin_label.place(relx=0.5, rely=0.15, anchor="center")

    #Batch_label
    batch_label = ctk.CTkLabel(frame1, text="2C112023", text_color="white", font=("Helvetica", 25, "bold"))
    batch_label.place(relx=0.23, rely=0.6)

    #Image Logo
    logo_img = ctk.CTkImage(light_image=Image.open("/home/bounty/main/assets/Logo.png"), size=(40, 40))
    image_label = ctk.CTkLabel(window, image=logo_img, text="")
    frame2.grid_propagate(False)

    my_img = Image.open('/home/bounty/main/assets/Logo.png').resize((190, 190))
    my_img_tk = ImageTk.PhotoImage(my_img)
    label3 = ctk.CTkLabel(frame1, image=my_img_tk, text="")
    label3.pack()
    label3.place(rely=0.1, relx=0.12)

    #FGP_LOGO
    finger_logo = ctk.CTkImage(light_image=Image.open("/home/bounty/main/assets/next2.jpg"), size=(25, 25))
    image_label = ctk.CTkLabel(frame2, image=finger_logo, text="")
    frame2.grid_propagate(False)
    my_img = Image.open('/home/bounty/main/assets/next2.jpg').resize((165, 165))
    my_img_tk = ImageTk.PhotoImage(my_img)
    label3 = ctk.CTkLabel(frame2, image=my_img_tk, text="")
    label3.pack()
    label3.place(rely=0.45, relx=0.2)

    face_logo = ctk.CTkImage(light_image=Image.open("/home/bounty/main/assets/next1.jpg"), size=(25, 25))
    image_label = ctk.CTkLabel(frame2, image=face_logo, text="")
    frame2.grid_propagate(False)
    my_img = Image.open('/home/bounty/main/assets/next1.jpg').resize((165, 165))
    my_img_tk = ImageTk.PhotoImage(my_img)
    label3 = ctk.CTkLabel(frame2, image=my_img_tk, text="")
    label3.pack()
    label3.place(rely=0.45, relx=0.55)

    # Login ID
    login_id_label = ctk.CTkLabel(frame2, text="CLASS:", text_color="white", font=("Helvetica", 25))
    login_id_label.place(relx=0.26, rely=0.3)
    class_id_entry = ctk.CTkEntry(frame2)
    class_id_entry.place(relx=0.45, rely=0.3)


    #Buttonforstart
    button1 = ctk.CTkButton(frame2, text="FACE RECOGNITION", font=("Helvetica", 15, "bold"), corner_radius=5,
                        border_spacing=7, fg_color="#215fb5",  command=start)
    button1.place(relx=0.52, rely=0.85)

    button2 = ctk.CTkButton(frame2, text="FINGERPRINT", font=("Helvetica", 15, "bold"), corner_radius=5,
                        border_spacing=7, fg_color="#215fb5")
    button2.place(relx=0.191, rely=0.85)

   # f = open(f"{databse_dir}+{class_id_entry.get()}_{current_date}.csv", "w", newline="")
    # f = open(f"test.csv", "w", newline="")
    # lnwriter = csv.writer(f)
    # lnwriter.writerow(["Name", "Time"])

    window.mainloop()