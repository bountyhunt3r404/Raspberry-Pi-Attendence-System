import threading
import picamera2
import libcamera
import cv2
from deepface import DeepFace

picam2 = picamera2.Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)},
                                                     lores={"format": 'YUV420', "size": (320, 240)}, 
                                                     transform=libcamera.Transform(hflip=1),
                                                     display="main"))
picam2.start()
#cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0

reference_img = cv2.imread("/home/bounty/main/database/known_face_dir/spandan.jpg")  # use your own image here

face_match = False


def check_face(frame):
    global face_match
    try:
        if DeepFace.verify(frame, reference_img.copy())['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
        face_match = False


while True:
    frame = cap = picam2.capture_array("main")
    ret = len(frame)>0


    if ret:
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError:
                pass
        counter += 1
        if face_match:
            cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows()