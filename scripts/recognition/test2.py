import face_recognition
import picamera2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

# Initialize the camera and set its resolution
camera = picamera2.Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'RGB888', "size": (320, 240)}))
camera.start()

# Create a numpy array to store the image data
output = np.empty((240, 320, 3), dtype=np.uint8)

# Capture an image from the camera
output = camera.capture_array("main")

# Load the image into face_recognition and find all the faces in it
face_locations = face_recognition.face_locations(output)

# Create a Tkinter window to display the result
root = Tk()
root.title("Face Recognition")

# Convert the image data to a PIL Image and display it in the window
image = Image.fromarray(output)
photo = ImageTk.PhotoImage(image)
label = Label(root, image=photo)
label.pack()

# Draw rectangles around each face in the image
for top, right, bottom, left in face_locations:
    canvas = Canvas(root, width=right-left, height=bottom-top)
    canvas.pack()
    canvas.create_rectangle(0, 0, right-left, bottom-top, outline="red", width=2)

root.mainloop()
