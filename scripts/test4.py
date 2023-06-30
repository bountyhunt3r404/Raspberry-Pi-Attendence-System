import face_recognition
import picamera2
import numpy as np
import libcamera
import cv2
import os
from concurrent.futures import ProcessPoolExecutor

# Set the path to the directory containing the images of known faces
known_faces_dir = "/home/bounty/main/known_face_dir"

# Load the images of known faces and their encodings
known_face_encodings = []
known_face_names = []
for filename in os.listdir(known_faces_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image = face_recognition.load_image_file(os.path.join(known_faces_dir, filename))
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(os.path.splitext(filename)[0])

# Initialize the camera and set its resolution
camera = picamera2.Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'RGB888', "size": (480, 320)},
                                                     lores={"format": 'YUV420', "size": (320, 240)}, 
                                                     transform=libcamera.Transform(hflip=1),
                                                     display="main"))
camera.start()

# Create a numpy array to store the image data
output = np.empty((240, 320, 3), dtype=np.uint8)


while True:
    # Capture an image from the camera
    output = camera.capture_array("main")

    # Load the image into face_recognition and find all the faces and their encodings in it
    face_locations = face_recognition.face_locations(output)
    face_encodings = face_recognition.face_encodings(output, face_locations)

    # Create a function to compare a face encoding to all known faces
    def compare_faces(face_encoding):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        return name

    # Use parallel processing to compare all faces in the image to all known faces
    with ProcessPoolExecutor() as executor:
        names = list(executor.map(compare_faces, face_encodings))

    # Loop through each face in the image and draw a rectangle around it and put its name above it
    for (top, right, bottom, left), name in zip(face_locations, names):
        cv2.rectangle(output, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(output, name, (left + 6, top - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    # Display the result using opencv
    cv2.imshow("Face Recognition", output)
    cv2.waitKey(1)
    

cv2.destroyAllWindows()
