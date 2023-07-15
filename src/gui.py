import numpy as np
import face_recognition
import cv2
import csv
from datetime import datetime
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Function to start attendance
# def start_attendance():
#     video_capture = cv2.VideoCapture(0)
#     swikar_image = face_recognition.load_image_file("faces/swikar.jpg")
#     swikar_encoding = face_recognition.face_encodings(swikar_image)[0]

#     shounak_image = face_recognition.load_image_file("faces/shounak.jpg")
#     shounak_encoding = face_recognition.face_encodings(shounak_image)[0]

#     Hitesh_image = face_recognition.load_image_file("faces/hitesh.jpg")
#     Hitesh_encoding = face_recognition.face_encodings(Hitesh_image)[0]

#     known_face_encoding = [swikar_encoding, shounak_encoding, Hitesh_encoding]
#     known_face_names = ["Swikar Jadhav", "Shounak Mulay", "Hitesh Pawar"]
#     students = known_face_names.copy()


#     face_locations = []
#     face_encodings = []

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    f = open(f"{class_id_entry.get()}_{current_date}.csv", "w", newline="")
    lnwriter = csv.writer(f)
    lnwriter.writerow(["Name", "Time"])

#     while True:
#         _, frame = video_capture.read()
#         small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#         rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

#         face_locations = face_recognition.face_locations(rgb_small_frame)
#         face_encodings = face_recognition.face_encodings(rgb_small_frame)

#         for (top, right, bottom, left) in face_locations:
#             top *= 4
#             right *= 4
#             bottom *= 4
#             left *= 4

#             cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

#         for face_encoding in face_encodings:
#             matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
#             face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
#             best_match_index = np.argmin(face_distance)
#             if matches[best_match_index]:
#                 name = known_face_names[best_match_index]

#             if name in known_face_names:
#                 font = cv2.FONT_HERSHEY_SIMPLEX
#                 text = name + " Present"
#                 text_width, text_height = cv2.getTextSize(text, font, fontScale=1, thickness=2)[0]
#                 text_left = left + (right - left) // 2 - text_width // 2
#                 text_top = top - 10
#                 cv2.putText(frame, text, (text_left, text_top), font, fontScale=1, color=(255, 0, 0), thickness=2)

#                 if name in students:
#                     students.remove(name)
#                     current_time = now.strftime("%H:%M:%S")
#                     lnwriter.writerow([name, current_time])

#         cv2.imshow("Attendance", frame)
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break

#     video_capture.release()
#     cv2.destroyAllWindows()
#     f.close()
#     window.quit()  # Close the GUI window


#Creating Gui Window
window = ctk.CTk()
window.title("Attendance System")
window.geometry(f"{1024}x{600}")
ctk.set_appearance_mode("dark")

h = int(365*0.9375)
w = int(200*1.28)

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
logo_img = ctk.CTkImage(light_image=Image.open("Logo.png"), size=(40, 40))
image_label = ctk.CTkLabel(window, image=logo_img, text="")
frame2.grid_propagate(False)

my_img = Image.open('Logo.png').resize((190, 190))
my_img_tk = ImageTk.PhotoImage(my_img)
label3 = ctk.CTkLabel(frame1, image=my_img_tk, text="")
label3.pack()
label3.place(rely=0.1, relx=0.12)

#FGP_LOGO
finger_logo = ctk.CTkImage(light_image=Image.open("next2.jpg"), size=(25, 25))
image_label = ctk.CTkLabel(frame2, image=finger_logo, text="")
frame2.grid_propagate(False)
my_img = Image.open('next2.jpg').resize((165, 165))
my_img_tk = ImageTk.PhotoImage(my_img)
label3 = ctk.CTkLabel(frame2, image=my_img_tk, text="")
label3.pack()
label3.place(rely=0.45, relx=0.2)

face_logo = ctk.CTkImage(light_image=Image.open("next1.jpg"), size=(25, 25))
image_label = ctk.CTkLabel(frame2, image=face_logo, text="")
frame2.grid_propagate(False)
my_img = Image.open('next1.jpg').resize((165, 165))
my_img_tk = ImageTk.PhotoImage(my_img)
label3 = ctk.CTkLabel(frame2, image=my_img_tk, text="")
label3.pack()
label3.place(rely=0.45, relx=0.55)


# Login ID
# login_id_label = ctk.CTkLabel(frame2, text="CLASS ID:", text_color="white", font=("Helvetica", 25))
# login_id_label.grid(row=2, column=1, padx=10, pady=(70, 0), sticky="ew")
# class_id_entry = ctk.CTkEntry(frame2)
# class_id_entry.grid(row=2, column=2, padx=10, pady=(150, 0))

# Login ID
login_id_label = ctk.CTkLabel(frame2, text="CLASS:", text_color="white", font=("Helvetica", 25))
login_id_label.place(relx=0.26, rely=0.3)
class_id_entry = ctk.CTkEntry(frame2)
class_id_entry.place(relx=0.45, rely=0.3)

# Button
#button = ctk.CTkButton(frame2, text="START ATTENDANCE", font=("Helvetica", 15, "bold"), corner_radius=12,
                       #border_spacing=7, fg_color="#215fb5", command=check_credentials)
#button.place(relx=0.5, rely=0.8, anchor="center")

#Buttonforstart
button1 = ctk.CTkButton(frame2, text="FACE RECOGNITION", font=("Helvetica", 15, "bold"), corner_radius=5,
                       border_spacing=7, fg_color="#215fb5")
button1.place(relx=0.52, rely=0.85)

button2 = ctk.CTkButton(frame2, text="FINGERPRINT", font=("Helvetica", 15, "bold"), corner_radius=5,
                       border_spacing=7, fg_color="#215fb5")
button2.place(relx=0.191, rely=0.85)




# combobox
#combobox.set("Select method")
#combobox.place(rely=0.65, relx=0.15)

# Password
# password_label = ctk.CTkLabel(frame2, text="PASSWORD:", text_color="white", font=("Helvetica", 25))
# password_label.grid(row=2, column=1, pady=(30, 0), sticky="ew")
# password_entry = ctk.CTkEntry(frame2, show='*')
# password_entry.grid(row=2, column=2, padx=10, pady=(30, 0))

#login_id_label.place(relx=0.5, rely=0.5)
# password_label.grid_configure(padx=20, pady=(30, 0))

window.mainloop()