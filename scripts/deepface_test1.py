#deepface_test1

import picamera2
import numpy as np
import cv2
import os
from deepface import DeepFace

# Set the path to the directory containing the images of known faces
known_faces_dir = "/home/bounty/main/known_face_dir"

# Load the images of known faces
known_face_images = []
known_face_names = []
for filename in os.listdir(known_faces_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image = cv2.imread(os.path.join(known_faces_dir, filename))
        known_face_images.append(image)
        known_face_names.append(os.path.splitext(filename)[0])

# Initialize the camera and set its resolution
camera = picamera2.Picamera2()
camera.configure(camera.create_preview_configuration())
camera.start()

while True:
    # Capture a frame from the camera
    output = camera.capture_array()

    # Detect all faces in the image
    face_locations = DeepFace.extract_faces(output, detector_backend="mtcnn", enforce_detection=False)
    print(face_locations)
    # Loop through each face in the image and compare it to the known faces
    for face_location in face_locations:
        # Extract the face from the image
        print(face_location)
        x1, y1, x2, y2 = map(int, face_location['facial_area'].values())
        print(x1, y1, x2, y2)
        face = output[y1:y2, x1:x2]
        print(face)

        # Compare the face to all known faces
        results = DeepFace.verify(face, known_face_images, enforce_detection=False)
        verified = results["verified"]
        distances = results["distance"]

        # Find the closest match
        min_distance_index = np.argmin(distances)
        min_distance = distances[min_distance_index]
        name = "Unknown"
        if verified[min_distance_index]:
            name = known_face_names[min_distance_index]

        # Draw a rectangle around the face and put its name above it
        cv2.rectangle(output, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(output, name, (x1 + 6, y1 - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    # Display the result using opencv
    cv2.imshow("Face Recognition", output)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()