import face_recognition
import picamera2
import libcamera
import numpy as np
import threading
import cv2

picam2 = picamera2.Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)},
                                                     lores={"format": 'YUV420', "size": (320, 240)}, 
                                                     transform=libcamera.Transform(hflip=1),
                                                     display="main"))
picam2.start()
#picam2.resolution = (320, 240)
output = np.empty((480, 640, 3), dtype=np.uint8)

counter = 0

while True:
    output = picam2.capture_array("main")
    face_locations = face_recognition.face_locations(output)

    if len(face_locations) > 0:
        if counter % 30 == 0:
            print("Found {} faces!".format(len(face_locations)))
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(output, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.imshow('Face Detection', output)
        cv2.waitKey(1)
        
    else:
        cv2.imshow('Face Detection', output)
        cv2.waitKey(1)
    
    counter += 1

cv2.destroyAllWindows()
