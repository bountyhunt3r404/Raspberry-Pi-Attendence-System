import main.src.face_rec_modules_old as frm
import face_recognition
import cv2
import picamera2
import libcamera
import time


faces_dir_path = '/home/bounty/main/known_face_dir'
face_encodings_dir_path = '/home/bounty/main/known_face_encodings'

#Raspberry Pi camera Initialisation and setup
picam2 = picamera2.Picamera2()

preview_config = picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)},
                                                     lores={"format": 'YUV420', "size": (320, 240)}, 
                                                     transform=libcamera.Transform(),
                                                     display="main")




'''
#print(frm.generate_face_encoding(faces_dir_path))

frm.save_face_encodings(frm.generate_face_encoding(faces_dir_path), face_encodings_dir_path)


spandan_image = face_recognition.load_image_file(faces_dir_path+"/spandan.jpg")
spandan_encoding = face_recognition.face_encodings(spandan_image)[0]

check, arry = frm.check_face_encodings_in_files(spandan_encoding, face_encodings_dir_path)

print("----------Checked array------------------------")
print(check, arry)
print("----------actual array ------------------------")
print(spandan_encoding)
'''

###############################---Main Program--#####################################
picam2.configure(preview_config)
#picam2.start_preview(picamera2.Preview.QT)
#picam2.start_preview(picamera2.Preview.QTGL)
picam2.start()
time.sleep(10)